# onedim.py
# Simon Hulse
# simon.hulse@chem.ox.ac.uk
# Last Edited: Sun 19 Jun 2022 23:54:33 BST

from __future__ import annotations
import copy
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple, Union

import numpy as np
import matplotlib.pyplot as plt

from nmr_sims.experiments.pa import PulseAcquireSimulation
from nmr_sims.nuclei import Nucleus
from nmr_sims.spin_system import SpinSystem

from nmrespy import ExpInfo, sig
from nmrespy._colors import RED, GRE, END, USE_COLORAMA
from nmrespy._files import check_existent_dir

from nmrespy._sanity import (
    sanity_check,
    funcs as sfuncs,
)
from nmrespy.freqfilter import Filter
from nmrespy.load import load_bruker
from nmrespy.mpm import MatrixPencil
from nmrespy.nlp import NonlinearProgramming
from nmrespy.plot import ResultPlotter

from . import logger, Estimator, Result


if USE_COLORAMA:
    import colorama
    colorama.init()


class Estimator1D(Estimator):
    """Estimator class for 1D data.

    .. note::

        To create an instance of ``Estimator1D``, you should use one of the following
        methods:

        * :py:meth:`new_bruker`
        * :py:meth:`new_synthetic_from_parameters`
        * :py:meth:`new_synthetic_from_simulation`
        * :py:meth:`from_pickle` (re-loads a previously saved estimator).
    """

    def __init__(
        self,
        data: np.ndarray,
        expinfo: ExpInfo,
        datapath: Optional[Path] = None,
    ) -> None:
        """
        Parameters
        ----------
        data
            Time-domain data to estimate.

        expinfo
            Experiment information.

        datapath
            If applicable, the path that the data was derived from.
        """
        super().__init__(data, expinfo, datapath)

    @classmethod
    def new_bruker(
        cls,
        directory: Union[str, Path],
        ask_convdta: bool = True,
    ) -> Estimator1D:
        """Create a new instance from Bruker-formatted data.

        Parameters
        ----------
        directory
            Absolute path to data directory.

        ask_convdta
            If ``True``, the user will be warned that the data should have its
            digitial filter removed prior to importing if the data to be impoprted
            is from an ``fid`` or ``ser`` file. If ``False``, the user is not
            warned.

        Notes
        -----
        **Directory Requirements**

        There are certain file paths expected to be found relative to ``directory``
        which contain the data and parameter files. Here is an extensive list of
        the paths expected to exist, for different data types:

        * Raw FID

          + ``directory/fid``
          + ``directory/acqus``

        * Processed data

          + ``directory/1r``
          + ``directory/../../acqus``
          + ``directory/procs``

        **Digital Filters**

        If you are importing raw FID data, make sure the path specified
        corresponds to an ``fid`` file which has had its group delay artefact
        removed. To do this, open the data you wish to analyse in TopSpin, and
        enter ``convdta`` in the bottom-left command line. You will be prompted
        to enter a value for the new data directory. It is this value you
        should use in ``directory``, not the one corresponding to the original
        (uncorrected) signal.
        """
        sanity_check(
            ("directory", directory, check_existent_dir),
            ("ask_convdta", ask_convdta, sfuncs.check_bool),
        )

        directory = Path(directory).expanduser()
        data, expinfo = load_bruker(directory, ask_convdta=ask_convdta)

        if data.ndim != 1:
            raise ValueError(f"{RED}Data dimension should be 1.{END}")

        if directory.parent.name == "pdata":
            slice_ = slice(0, data.shape[0] // 2)
            data = (2 * sig.ift(data))[slice_]

        return cls(data, expinfo, directory)

    @classmethod
    def new_synthetic_from_parameters(
        cls,
        params: np.ndarray,
        pts: int,
        sw: float,
        offset: float = 0.0,
        sfo: Optional[float] = None,
        snr: float = 30.0,
    ) -> Estimator1D:
        """Generate an estimator instance from an array of oscillator parameters.

        Parameters
        ----------
        params
            Parameter array with the following structure:

              .. code:: python

                 params = numpy.array([
                    [a_1, φ_1, f_1, η_1],
                    [a_2, φ_2, f_2, η_2],
                    ...,
                    [a_m, φ_m, f_m, η_m],
                 ])

        pts
            The number of points the signal comprises.

        sw
            The sweep width of the signal (Hz).

        offset
            The transmitter offset (Hz).

        sfo
            The transmitter frequency (MHz).

        snr
            The signal-to-noise ratio. If ``None`` then no noise will be added
            to the FID.
        """
        sanity_check(
            ("params", params, sfuncs.check_ndarray, (), {"dim": 2, "shape": [(1, 4)]}),
            ("pts", pts, sfuncs.check_int, (), {"min_value": 1}),
            ("sw", sw, sfuncs.check_float, (), {"greater_than_zero": True}),
            ("offset", offset, sfuncs.check_float, (), {}, True),
            ("sfo", sfo, sfuncs.check_float, (), {"greater_than_zero": True}, True),
            ("snr", snr, sfuncs.check_float, (), {"greater_than_zero": True}, True),
        )

        expinfo = ExpInfo(
            dim=1,
            sw=sw,
            offset=offset,
            sfo=sfo,
            default_pts=pts,
        )

        data = expinfo.make_fid(params, snr=snr)
        return cls(data, expinfo)

    @classmethod
    def new_synthetic_from_simulation(
        cls,
        spin_system: SpinSystem,
        sw: float,
        offset: float,
        pts: int,
        freq_unit: str = "hz",
        channel: Union[str, Nucleus] = "1H",
        snr: Optional[float] = 30.0,
    ) -> Estimator1D:
        """Generate an estimator with data derived from a pulse-aquire experiment
        simulation.

        Simulations are performed using the
        `nmr_sims.experiments.pa.PulseAcquireSimulation
        <https://foroozandehgroup.github.io/nmr_sims/content/references/experiments/
        pa.html#nmr_sims.experiments.pa.PulseAcquireSimulation>`_
        class.

        Parameters
        ----------
        spin_system
            Specification of the spin system to run simulations on.
            `See here <https://foroozandehgroup.github.io/nmr_sims/content/
            references/spin_system.html#nmr_sims.spin_system.SpinSystem.__init__>`_
            for more details. **N.B. the transmitter frequency (sfo) will
            be determined by** ``spin_system.field``.

        sw
            The sweep width in Hz.

        offset
            The transmitter offset frequency in Hz.

        pts
            The number of points sampled.

        freq_unit
            The unit that ``sw`` and ``offset`` are expressed in. Should
            be either ``"hz"`` or ``"ppm"``.

        channel
            Nucleus targeted in the experiment simulation. ¹H is set as the default.
            `See here <https://foroozandehgroup.github.io/nmr_sims/content/
            references/nuclei.html>`__ for more information.

        snr
            The signal-to-noise ratio of the resulting signal, in decibels. ``None``
            produces a noiseless signal.
        """
        sanity_check(
            ("spin_system", spin_system, sfuncs.check_spin_system),
            ("sw", sw, sfuncs.check_float, (), {"greater_than_zero": True}),
            ("offset", offset, sfuncs.check_float),
            ("pts", pts, sfuncs.check_positive_int),
            ("freq_unit", freq_unit, sfuncs.check_one_of, ("hz", "ppm")),
            ("channel", channel, sfuncs.check_nmrsims_nucleus),
            ("snr", snr, sfuncs.check_float, (), {}, True),
        )

        sw = f"{sw}{freq_unit}"
        offset = f"{offset}{freq_unit}"
        sim = PulseAcquireSimulation(
            spin_system, pts, sw, offset=offset, channel=channel,
        )
        sim.simulate()
        _, data, _ = sim.fid()
        if snr is not None:
            data += sig._make_noise(data, snr)

        expinfo = ExpInfo(
            dim=1,
            sw=sim.sweep_widths[0],
            offset=sim.offsets[0],
            sfo=sim.sfo[0],
            nuclei=channel,
            default_pts=data.shape,
        )

        return cls(data, expinfo)

    @property
    def spectrum(self) -> np.ndarray:
        """Return the spectrum corresponding to ``self.data``"""
        data = copy.deepcopy(self.data)
        data[0] /= 2
        return sig.ft(data)

    def phase_data(
        self,
        p0: float = 0.0,
        p1: float = 0.0,
        pivot: int = 0,
    ) -> None:
        """Apply first-order phae correction to the estimator's data.

        Parameters
        ----------
        p0
            Zero-order phase correction, in radians.

        p1
            First-order phase correction, in radians.

        pivot
            Index of the pivot.
        """
        sanity_check(
            ("p0", p0, sfuncs.check_float),
            ("p1", p1, sfuncs.check_float),
            ("pivot", pivot, sfuncs.check_index, (self._data.size,)),
        )
        self._data = sig.phase(self._data, [p0], [p1], [pivot])

    def view_data(
        self,
        domain: str = "freq",
        components: str = "real",
        freq_unit: str = "hz",
    ) -> None:
        """View the data.

        Parameters
        ----------
        domain
            Must be ``"freq"`` or ``"time"``.

        components
            Must be ``"real"``, ``"imag"``, or ``"both"``.

        freq_unit
            Must be ``"hz"`` or ``"ppm"``.
        """
        sanity_check(
            ("domain", domain, sfuncs.check_one_of, ("freq", "time")),
            ("components", components, sfuncs.check_one_of, ("real", "imag", "both")),
            ("freq_unit", freq_unit, sfuncs.check_frequency_unit, (self.hz_ppm_valid,)),
        )

        fig = plt.figure()
        ax = fig.add_subplot()
        y = copy.deepcopy(self._data)

        if domain == "freq":
            x = self.get_shifts(unit=freq_unit)[0]
            y[0] /= 2
            y = sig.ft(y)
            label = f"$\\omega$ ({freq_unit.replace('h', 'H')})"
        elif domain == "time":
            x = self.get_timepoints()[0]
            label = "$t$ (s)"

        if components in ["real", "both"]:
            ax.plot(x, y.real, color="k")
        if components in ["imag", "both"]:
            ax.plot(x, y.imag, color="#808080")

        ax.set_xlabel(label)
        ax.set_xlim((x[0], x[-1]))

        plt.show()

    @logger
    def estimate(
        self,
        region: Optional[Tuple[float, float]] = None,
        noise_region: Optional[Tuple[float, float]] = None,
        region_unit: str = "hz",
        initial_guess: Optional[Union[np.ndarray, int]] = None,
        method: str = "gauss-newton",
        phase_variance: bool = True,
        max_iterations: Optional[int] = None,
        cut_ratio: Optional[float] = 1.1,
        mpm_trim: Optional[int] = 4096,
        nlp_trim: Optional[int] = None,
        strict_region_order: bool = False,
        fprint: bool = True,
        _log: bool = True,
    ) -> None:
        r"""Estimate a specified region of the signal.

        The basic steps that this method carries out are:

        * (Optional, but highly advised) Generate a frequency-filtered signal
          corresponding to the specified region.
        * (Optional) Generate an inital guess using the Matrix Pencil Method (MPM).
        * Apply numerical optimisation to determine a final estimate of the signal
          parameters

        Parameters
        ----------
        region
            The frequency range of interest. Should be of the form ``[left, right]``
            where ``left`` and ``right`` are the left and right bounds of the region
            of interest. If ``None``, the full signal will be considered, though
            for sufficently large and complex signals it is probable that poor and
            slow performance will be achieved.

        noise_region
            If ``region`` is not ``None``, this must be of the form ``[left, right]``
            too. This should specify a frequency range where no noticeable signals
            reside, i.e. only noise exists.

        region_unit
            One of ``"hz"`` or ``"ppm"`` Specifies the units that ``region``
            and ``noise_region`` have been given as.

        initial_guess
            If ``None``, an initial guess will be generated using the MPM,
            with the Minimum Descritpion Length being used to estimate the
            number of oscilltors present. If and int, the MPM will be used to
            compute the initial guess with the value given being the number of
            oscillators. If a NumPy array, this array will be used as the initial
            guess.

        method
            Specifies the optimisation method.

            * ``"exact"`` Uses SciPy's
              `trust-constr routine <https://docs.scipy.org/doc/scipy/reference/
              optimize.minimize-trustconstr.html\#optimize-minimize-trustconstr>`_
              The Hessian will be exact.
            * ``"gauss-newton"`` Uses SciPy's
              `trust-constr routine <https://docs.scipy.org/doc/scipy/reference/
              optimize.minimize-trustconstr.html\#optimize-minimize-trustconstr>`_
              The Hessian will be approximated based on the
              `Gauss-Newton method <https://en.wikipedia.org/wiki/
              Gauss%E2%80%93Newton_algorithm>`_
            * ``"lbfgs"`` Uses SciPy's
              `L-BFGS-B routine <https://docs.scipy.org/doc/scipy/reference/
              optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb>`_.

        phase_variance
            Whether or not to include the variance of oscillator phases in the cost
            function. This should be set to ``True`` in cases where the signal being
            considered is derived from well-phased data.

        max_iterations
            A value specifiying the number of iterations the routine may run
            through before it is terminated. If ``None``, the default number
            of maximum iterations is set (``100`` if ``method`` is
            ``"exact"`` or ``"gauss-newton"``, and ``500`` if ``"method"`` is
            ``"lbfgs"``).

        mpm_trim
            Specifies the maximal size allowed for the filtered signal when
            undergoing the Matrix Pencil. If ``None``, no trimming is applied
            to the signal. If an int, and the filtered signal has a size
            greater than ``mpm_trim``, this signal will be set as
            ``signal[:mpm_trim]``.

        nlp_trim
            Specifies the maximal size allowed for the filtered signal when undergoing
            nonlinear programming. By default (``None``), no trimming is applied to
            the signal. If an int, and the filtered signal has a size greater than
            ``nlp_trim``, this signal will be set as ``signal[:nlp_trim]``.

        strict_region_order
            If `True`, the first elements of ``region`` and ``noise_region`` will
            be taken as the left bounds and the second elements will be taken
            as the right bounds, even if this leads to selecting a signal which
            wraps around itself. If ``False``, the ordering of the elements is
            irrelevant, the higher frequency bound will be taken as the left bound,
            and the lower frequency will be taken as the right bound of the region.

        fprint
            Whether of not to output information to the terminal.

        _log
            Ignore this!
        """
        sanity_check(
            (
                "region_unit", region_unit, sfuncs.check_frequency_unit,
                (self.hz_ppm_valid,),
            ),
            (
                "initial_guess", initial_guess, sfuncs.check_initial_guess,
                (self.dim,), {}, True
            ),
            ("method", method, sfuncs.check_one_of, ("lbfgs", "gauss-newton", "exact")),
            ("phase_variance", phase_variance, sfuncs.check_bool),
            (
                "max_iterations", max_iterations, sfuncs.check_int, (),
                {"min_value": 1}, True,
            ),
            ("fprint", fprint, sfuncs.check_bool),
            ("mpm_trim", mpm_trim, sfuncs.check_int, (), {"min_value": 1}, True),
            ("nlp_trim", nlp_trim, sfuncs.check_int, (), {"min_value": 1}, True),
            (
                "cut_ratio", cut_ratio, sfuncs.check_float, (),
                {"greater_than_one": True}, True,
            ),
            ("strict_region_order", strict_region_order, sfuncs.check_bool),
        )

        sanity_check(
            (
                "region", region, sfuncs.check_region,
                (self.sw(region_unit), self.offset(region_unit)), {}, True,
            ),
            (
                "noise_region", noise_region, sfuncs.check_region,
                (self.sw(region_unit), self.offset(region_unit)), {}, True,
            ),
        )

        # The plan of action:
        # --> Derive filtered signals (both cut and uncut)
        # --> Run the MDL followed by MPM for an initial guess on cut signal
        # --> Run Optimiser on cut signal
        # --> Run Optimiser on uncut signal
        if region is None:
            region = self.convert(
                ((0, self._data.size - 1),), "idx->hz",
            )
            noise_region = None

            signal = self._data
            if (mpm_trim is None) or (mpm_trim > signal.size):
                mpm_trim = signal.size
            if (nlp_trim is None) or (nlp_trim > signal.size):
                nlp_trim = signal.size

            expinfo = ExpInfo(1, self.sw(), self.offset(), self.sfo)

            if isinstance(initial_guess, np.ndarray):
                x0 = initial_guess
            else:
                oscillators = initial_guess if isinstance(initial_guess, int) else 0
                x0 = MatrixPencil(
                    expinfo,
                    signal[:mpm_trim],
                    oscillators=oscillators,
                    fprint=fprint,
                ).get_params()
                if x0.size == 0:
                    return self._results.append(
                        Result(
                            np.array([[]]),
                            np.array([[]]),
                            region,
                            noise_region,
                            self.sfo,
                        )
                    )

            final_result = NonlinearProgramming(
                expinfo,
                signal[:nlp_trim],
                x0,
                phase_variance=phase_variance,
                method=method,
                max_iterations=max_iterations,
                fprint=fprint,
            )

        else:
            filt = Filter(
                self._data,
                ExpInfo(1, self.sw(), self.offset(), self.sfo),
                region,
                noise_region,
                region_unit=region_unit,
                strict_region_order=strict_region_order,
            )

            cut_signal, cut_expinfo = filt.get_filtered_fid()
            uncut_signal, uncut_expinfo = filt.get_filtered_fid(cut_ratio=None)
            region = filt.get_region()
            noise_region = filt.get_noise_region()

            cut_size = cut_signal.size
            uncut_size = uncut_signal.size
            if (mpm_trim is None) or (mpm_trim > cut_size):
                mpm_trim = cut_size
            if (nlp_trim is None) or (nlp_trim > uncut_size):
                nlp_trim = uncut_size

            if isinstance(initial_guess, np.ndarray):
                x0 = initial_guess
            else:
                oscillators = initial_guess if isinstance(initial_guess, int) else 0
                x0 = MatrixPencil(
                    cut_expinfo,
                    cut_signal[:mpm_trim],
                    oscillators=oscillators,
                    fprint=fprint,
                ).get_params()

                if x0.size == 0:
                    return self._results.append(
                        Result(
                            np.array([[]]),
                            np.array([[]]),
                            region,
                            noise_region,
                            self.sfo,
                        )
                    )

            cut_result = NonlinearProgramming(
                cut_expinfo,
                cut_signal[:mpm_trim],
                x0,
                phase_variance=phase_variance,
                method=method,
                max_iterations=max_iterations,
                fprint=fprint,
            ).get_params()

            final_result = NonlinearProgramming(
                uncut_expinfo,
                uncut_signal[:nlp_trim],
                cut_result,
                phase_variance=phase_variance,
                method=method,
                max_iterations=max_iterations,
                fprint=fprint,
            )

        self._results.append(
            Result(
                final_result.get_params(),
                final_result.get_errors(),
                region,
                noise_region,
                self.sfo,
            )
        )

    @logger
    def subband_estimate(
        self,
        noise_region: Tuple[float, float],
        noise_region_unit: str = "hz",
        nsubbands: Optional[int] = None,
        method: str = "gauss-newton",
        phase_variance: bool = True,
        max_iterations: Optional[int] = None,
        cut_ratio: Optional[float] = 1.1,
        mpm_trim: Optional[int] = 4096,
        nlp_trim: Optional[int] = None,
        fprint: bool = True,
        _log: bool = True,
    ) -> None:
        r"""Perform estiamtion on the entire signal via estimation of frequency-filtered
        sub-bands.

        This method splits the signal up into ``nsubbands`` equally-sized region
        and extracts parameters from each region before finally concatenating all
        the results together.

        Parameters
        ----------
        noise_region
            Specifies a frequency range where no noticeable signals reside, i.e. only
            noise exists.

        noise_region_unit
            One of ``"hz"`` or ``"ppm"``. Specifies the units that ``noise_region``
            have been given in.

        subbands
            The number of sub-bands to break the signal into. If ``None``, the number
            will be set as the nearest integer to the data size divided by 500.

        method
            Specifies the optimisation method.

            * ``"exact"`` Uses SciPy's
              `trust-constr routine <https://docs.scipy.org/doc/scipy/reference/
              optimize.minimize-trustconstr.html\#optimize-minimize-trustconstr>`_
              The Hessian will be exact.
            * ``"gauss-newton"`` Uses SciPy's
              `trust-constr routine <https://docs.scipy.org/doc/scipy/reference/
              optimize.minimize-trustconstr.html\#optimize-minimize-trustconstr>`_
              The Hessian will be approximated based on the
              `Gauss-Newton method <https://en.wikipedia.org/wiki/
              Gauss%E2%80%93Newton_algorithm>`_
            * ``"lbfgs"`` Uses SciPy's
              `L-BFGS-B routine <https://docs.scipy.org/doc/scipy/reference/
              optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb>`_.

        phase_variance
            Whether or not to include the variance of oscillator phases in the cost
            function. This should be set to ``True`` in cases where the signal being
            considered is derived from well-phased data.

        max_iterations
            A value specifiying the number of iterations the routine may run
            through before it is terminated. If ``None``, the default number
            of maximum iterations is set (``100`` if ``method`` is
            ``"exact"`` or ``"gauss-newton"``, and ``500`` if ``"method"`` is
            ``"lbfgs"``).

        mpm_trim
            Specifies the maximal size allowed for the filtered signal when
            undergoing the Matrix Pencil. If ``None``, no trimming is applied
            to the signal. If an int, and the filtered signal has a size
            greater than ``mpm_trim``, this signal will be set as
            ``signal[:mpm_trim]``.

        nlp_trim
            Specifies the maximal size allowed for the filtered signal when undergoing
            nonlinear programming. By default (``None``), no trimming is applied to
            the signal. If an int, and the filtered signal has a size greater than
            ``nlp_trim``, this signal will be set as ``signal[:nlp_trim]``.

        strict_region_order
            If `True`, the first elements of ``region`` and ``noise_region`` will
            be taken as the left bounds and the second elements will be taken
            as the right bounds, even if this leads to selecting a signal which
            wraps around itself. If ``False``, the ordering of the elements is
            irrelevant, the higher frequency bound will be taken as the left bound,
            and the lower frequency will be taken as the right bound of the region.

        fprint
            Whether of not to output information to the terminal.
        """
        sanity_check(
            (
                "noise_region_unit", noise_region_unit, sfuncs.check_frequency_unit,
                (self.hz_ppm_valid,),
            ),
            ("nsubbands", nsubbands, sfuncs.check_int, (), {"min_value": 1}, True),
            ("method", method, sfuncs.check_one_of, ("lbfgs", "gauss-newton", "exact")),
            ("phase_variance", phase_variance, sfuncs.check_bool),
            (
                "max_iterations", max_iterations, sfuncs.check_int, (),
                {"min_value": 1}, True,
            ),
            ("fprint", fprint, sfuncs.check_bool),
            ("mpm_trim", mpm_trim, sfuncs.check_int, (), {"min_value": 1}, True),
            ("nlp_trim", nlp_trim, sfuncs.check_int, (), {"min_value": 1}, True),
            (
                "cut_ratio", cut_ratio, sfuncs.check_float, (),
                {"greater_than_one": True}, True,
            ),
        )

        sanity_check(
            (
                "noise_region", noise_region, sfuncs.check_region,
                (self.sw(noise_region_unit), self.offset(noise_region_unit)), {}, True,
            ),
        )

        if nsubbands is None:
            nsubbands = int(np.ceil(self.data.size / 500))

        noise_region = self.convert([noise_region], f"{noise_region_unit}->hz")

        idxs, mid_idxs = self._get_subband_indices(nsubbands)
        shifts, = self.get_shifts()
        regions = [(shifts[idx[0]], shifts[idx[1]]) for idx in idxs]
        mid_regions = [(shifts[mid_idx[0]], shifts[mid_idx[1]]) for mid_idx in mid_idxs]

        if fprint:
            print(f"Starting sub-band estimation using {nsubbands} sub-bands:")

        params = None
        errors = None
        for i, (region, mid_region) in enumerate(zip(regions, mid_regions), start=1):
            if fprint:
                msg = (
                    f"--> Estimating region #{i}: "
                    f"{mid_region[0]:.2f} - {mid_region[1]:.2f}Hz"
                )
                if self.hz_ppm_valid:
                    mid_region_ppm = self.convert([mid_region], "hz->ppm")[0]
                    msg += f" ({mid_region_ppm[0]:.3f} - {mid_region_ppm[1]:.3f}ppm)"
                print(msg)

            self.estimate(
                region, noise_region, region_unit="hz", method=method,
                phase_variance=phase_variance, max_iterations=max_iterations,
                cut_ratio=cut_ratio, mpm_trim=mpm_trim, nlp_trim=nlp_trim,
                fprint=False, strict_region_order=True, _log=False,
            )
            p, e = self._keep_middle_freqs(self._results.pop(), mid_region)

            if p is None:
                continue
            if params is None:
                params = p
                errors = e
            else:
                params = np.vstack((params, p))
                errors = np.vstack((errors, e))

        sort_idx = np.argsort(params[:, 2])
        params = params[sort_idx]
        errors = errors[sort_idx]

        if fprint:
            print(f"{GRE}Sub-band estimation complete.{END}")
        self._results.append(
            Result(params, errors, region=None, noise_region=None, sfo=self.sfo)
        )

    def _get_subband_indices(
        self,
        nsubbands: int,
    ) -> Tuple[Iterable[Tuple[int, int]], Iterable[Tuple[int, int]]]:
        # (nsubbands - 2) full-size regions plus 2 half-size regions on each end.
        width = int(np.ceil(2 * self.data.size / (nsubbands - 1)))
        mid_width = int(np.ceil(width / 2))
        start_factor = int(np.ceil(self.data.size / (nsubbands - 1)))
        idxs = []
        mid_idxs = []
        for i in range(0, nsubbands - 2):
            start = i * start_factor
            mid_start = int(np.ceil((i + 0.5) * start_factor))
            if i == nsubbands - 3:
                idxs.append((start, self.data.size - 1))
            else:
                idxs.append((start, start + width))
            mid_idxs.append((mid_start, mid_start + mid_width))

        idxs.insert(0, (0, start_factor))
        idxs.append(((nsubbands - 2) * start_factor, self.data.size - 1))
        mid_idxs.insert(0, (0, mid_idxs[0][0]))
        mid_idxs.append((mid_idxs[-1][-1], self.data.size - 1))

        return idxs, mid_idxs

    @staticmethod
    def _keep_middle_freqs(
        result: Result,
        mid_region: Tuple[float, float],
    ) -> Tuple[np.ndarray, np.ndarray]:
        if result.params.size == 0:
            return None, None
        to_remove = (
            list(np.nonzero(result.params[:, 2] >= mid_region[0])[0]) +
            list(np.nonzero(result.params[:, 2] < mid_region[1])[0])
        )
        return (
            np.delete(result.params, to_remove, axis=0),
            np.delete(result.errors, to_remove, axis=0),
        )

    def make_fid(
        self,
        indices: Optional[Iterable[int]] = None,
        pts: Optional[Iterable[int]] = None,
    ) -> np.ndarray:
        r"""Construct a noiseless FID from estimation result parameters.

        Parameters
        ----------
        indices
            The indices of results to extract errors from. Index ``0`` corresponds to
            the first result obtained using the estimator, ``1`` corresponds to
            the next, etc.  If ``None``, all results will be used.

        pts
            The number of points to construct the time-points with in each dimesnion.
            If ``None``, and ``self.default_pts`` is a tuple of ints, it will be
            used.
        """
        sanity_check(
            (
                "indices", indices, sfuncs.check_int_list, (),
                {"max_value": len(self._results) - 1}, True,
            ),
            (
                "pts", pts, sfuncs.check_int_list, (),
                {
                    "length": self.dim,
                    "len_one_can_be_listless": True,
                    "min_value": 1,
                },
                True,
            ),
        )

        return super().make_fid(indices, pts=pts)

    @logger
    def plot_result(
        self,
        indices: Optional[Iterable[int]] = None,
        *,
        plot_residual: bool = True,
        plot_model: bool = False,
        residual_shift: Optional[Iterable[float]] = None,
        model_shift: Optional[float] = None,
        shifts_unit: str = "ppm",
        data_color: Any = "#000000",
        residual_color: Any = "#808080",
        model_color: Any = "#808080",
        oscillator_colors: Optional[Any] = None,
        show_labels: bool = False,
        stylesheet: Optional[Union[str, Path]] = None,
    ) -> Iterable[ResultPlotter]:
        """Write estimation results to text and PDF files.

        Parameters
        ----------
        indices
            The indices of results to include. Index ``0`` corresponds to the first
            result obtained using the estimator, ``1`` corresponds to the next, etc.
            If ``None``, all results will be included.

        plot_model
            If ``True``, plot the model generated using ``result``. This model is
            a summation of all oscillator present in the result.

        plot_residual
            If ``True``, plot the difference between the data and the model
            generated using ``result``.

        residual_shift
            Specifies a translation of the residual plot along the y-axis. If
            ``None``, a default shift will be applied.

        model_shift
            Specifies a translation of the residual plot along the y-axis. If
            ``None``, a default shift will be applied.

        shifts_unit
            Units to display chemical shifts in. Must be either ``'ppm'`` or
            ``'hz'``.

        data_color
            The colour used to plot the data. Any value that is recognised by
            matplotlib as a color is permitted. See `here
            <https://matplotlib.org/stable/tutorials/colors/colors.html>`_ for
            a full description of valid values.

        residual_color
            # The colour used to plot the residual. See ``data_color`` for a
            # description of valid colors.

        model_color
            The colour used to plot the model. See ``data_color`` for a
            description of valid colors.

        oscillator_colors
            Describes how to color individual oscillators. The following
            is a complete list of options:

            * If a valid matplotlib color is given, all oscillators will
              be given this color.
            * If a string corresponding to a matplotlib colormap is given,
              the oscillators will be consecutively shaded by linear increments
              of this colormap. For all valid colormaps, see
              `here <https://matplotlib.org/stable/tutorials/colors/\
              colormaps.html>`__
            * If an iterable object containing valid matplotlib colors is
              given, these colors will be cycled.
              For example, if ``oscillator_colors = ['r', 'g', 'b']``:

              + Oscillators 1, 4, 7, ... would be :red:`red (#FF0000)`
              + Oscillators 2, 5, 8, ... would be :green:`green (#008000)`
              + Oscillators 3, 6, 9, ... would be :blue:`blue (#0000FF)`

            * If ``None``, the default colouring method will be applied, which
              involves cycling through the following colors:

                - :oscblue:`#1063E0`
                - :oscorange:`#EB9310`
                - :oscgreen:`#2BB539`
                - :oscred:`#D4200C`

        show_labels
            If ``True``, each oscillator will be given a numerical label
            in the plot, if ``False``, the labels will be hidden.

        stylesheet
            The name of/path to a matplotlib stylesheet for further
            customaisation of the plot. See `here <https://matplotlib.org/\
            stable/tutorials/introductory/customizing.html>`__ for more
            information on stylesheets.
        """
        self._check_results_exist()
        sanity_check(
            (
                "indices", indices, sfuncs.check_int_list, (),
                {
                    "must_be_positive": True,
                    "max_value": len(self._results) - 1,
                },
                True,
            ),
            ("plot_residual", plot_residual, sfuncs.check_bool),
            ("plot_model", plot_model, sfuncs.check_bool),
            ("residual_shift", residual_shift, sfuncs.check_float, (), {}, True),
            ("model_shift", model_shift, sfuncs.check_float, (), {}, True),
            (
                "shifts_unit", shifts_unit, sfuncs.check_frequency_unit,
                (self.hz_ppm_valid,),
            ),
            ("data_color", data_color, sfuncs.check_mpl_color),
            ("residual_color", residual_color, sfuncs.check_mpl_color),
            ("model_color", model_color, sfuncs.check_mpl_color),
            (
                "oscillator_colors", oscillator_colors, sfuncs.check_oscillator_colors,
                (), {}, True,
            ),
            ("show_labels", show_labels, sfuncs.check_bool),
            ("stylesheet", stylesheet, sfuncs.check_str, (), {}, True),
        )
        results = self.get_results(indices)

        expinfo = ExpInfo(
            1,
            sw=self.sw(),
            offset=self.offset(),
            sfo=self.sfo,
            nuclei=self.nuclei,
            default_pts=self.default_pts,
        )

        return [
            ResultPlotter(
                self._data,
                result.get_params(funit="hz"),
                expinfo,
                region=result.get_region(unit=shifts_unit),
                shifts_unit=shifts_unit,
                plot_residual=plot_residual,
                plot_model=plot_model,
                residual_shift=residual_shift,
                model_shift=model_shift,
                data_color=data_color,
                residual_color=residual_color,
                model_color=model_color,
                oscillator_colors=oscillator_colors,
                show_labels=show_labels,
                stylesheet=stylesheet,
            )
            for result in results
        ]

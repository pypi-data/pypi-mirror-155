"""
Module containing the spacing functions for the binarycpython package. Very under-populated at the moment, but more are likely to come soon

This class object is an extension to the population grid object

Tasks:
    TODO: add more spacing functions to this module.
"""

# pylint: disable=E1101

import sys
import math
import json
import functools
from typing import Union
import traceback

import numpy as np
import cachetools
import diskcache



import py_rinterpolate


class spacing_functions:
    """
    Extension for the Population class containing the code for spacing functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    @cachetools.cachedmethod(lambda self: self.caches["spacing_functions.const_linear"])
    def const_linear(
        self, min_bound: Union[int, float], max_bound: Union[int, float], steps: int
    ) -> list:
        """
        Samples a range linearly. Uses numpy linspace, and returns an array of floats. Do NOT use this for integers.

        Args:
            min_bound: lower bound of range
            max_bound: upper bound of range
            steps: number of segments between min_bound and max_bound

        Returns:
            np.linspace(min_bound, max_bound, steps)
        """
        return np.linspace(min_bound, max_bound, steps)

    @cachetools.cachedmethod(lambda self: self.caches["spacing_functions.const_int"])
    def const_int(
        self, min_bound: Union[int, float], max_bound: Union[int, float], steps: int
    ) -> list:
        """
        Samples an integer range linearly. Returns a list of ints.

        Args:
            min_bound: lower bound of range, must be an integer (is converted to int)
            max_bound: upper bound of range, must be an integer (is converted to int)
            steps: number of segments between min_bound and max_bound

        Returns:
            range(min_bound,max_bound,step)

            where step is int((int(max_bound)-int(min_bound))/steps)
        """

        step = int((int(max_bound) - int(min_bound)) / max(1, steps - 1))
        if steps <= 1:
            return [int(min_bound)]
        return range(int(min_bound), int(max_bound + step), step)

    ############################################################
    @cachetools.cachedmethod(lambda self: self.caches["spacing_functions.const_ranges"])
    def const_ranges(self, ranges) -> list:
        """
        Samples a series of ranges linearly.

        Args:
            ranges: a tuple of tuples passed to the self.const_linear() spacing function.

        Returns:
            numpy array of masses

        Example:
            The following allocates 10 stars between 0.1 and 0.65, 20 stars between 0.65
            and 0.85, and 10 stars between 0.85 and 10.0 Msun::

                samplerfunc="const_ranges((({},{},{}),({},{},{}),({},{},{})))".format(
                    0.1, 0.65, 10,
                    0.65, 0.85, 20,
                    0.85, 10.0, 10
                )

        """

        masses = np.empty(0)
        for valuerange in ranges:
            masses = np.append(masses, self.const_linear(*valuerange))
        return np.unique(masses)

    ############################################################
    def peak_normalized_gaussian_func(
        self, x: Union[int, float], mean: Union[int, float], sigma: Union[int, float]
    ) -> Union[int, float]:
        """
        Function to evaluate a Gaussian at a given point, note
        that the normalization is such that the peak is always 1.0,
        not that the integral is 1.0

        Args:
            x: location at which to evaluate the distribution
            mean: mean of the Gaussian
            sigma: standard deviation of the Gaussian

        Returns:
            value of the Gaussian at x
        """

        gaussian_prefactor = 1.0  # / math.sqrt(2.0 * math.pi)

        r = 1.0 / sigma
        y = (x - mean) * r
        return gaussian_prefactor * math.exp(-0.5 * y ** 2)

    ############################################################
    @cachetools.cachedmethod(
        lambda self: self.caches["spacing_functions.gaussian_zoom"]
    )
    def gaussian_zoom(
        self,
        min_bound: Union[int, float],
        max_bound: Union[int, float],
        zoom_mean: Union[int, float],
        zoom_dispersion: Union[int, float],
        zoom_magnitude: Union[int, float],
        steps: int,
    ) -> list:
        """
        Samples such that a region is zoomed in according to a 1-Gaussian function

        Args:
            min_bound: lower bound of range
            max_bound: upper bound of range
            zoom_mean: mean of the Gaussian zoom location
            zoom_dispersion: dispersion of the Gaussian
            zoom_magnitude: depth of the Gaussian (should be 0<= zoom_magntiude <1)
            steps: number of segments between min_bound and max_bound assuming a linear step
                   this is what you'd normally call "resolution"

        Returns:
            Numpy array of sample values
        """

        # linear spacing: this is what we'd have
        # in the absence of a Gaussian zoom
        linear_spacing = (max_bound - min_bound) / (steps - 1)

        # make the list of values
        x = min_bound
        array = np.array([])
        while x <= max_bound:
            array = np.append(array, x)
            g = self.peak_normalized_gaussian_func(x, zoom_mean, zoom_dispersion)
            f = 1.0 - zoom_magnitude * g
            dx = linear_spacing * f
            x = x + dx

        # force the last array member to be max_bound if it's not
        if array[-1] != max_bound:
            array[-1] = max_bound

        return np.unique(array)

    def const_dt(self, cachedir=None, usecache=True, **kwargs):
        """
        const_dt returns a list of masses spaced at a constant age difference

        Args:
            dt: the time difference between the masses (1000.0 Myr, used when logspacing==False)
            dlogt : the delta log10(time) difference between masses (0.1 dex, used when logspacing==True)
            mmin: the minimum mass to be considered in the stellar lifetime interpolation table (0.07 Msun)
            mmax: the maximum mass to be considered in the stellar lifetime interpolation table (100.0 Msun)
            nres: the resolution of the stellar lifetime interpolation table (100)
            logspacing: whether to use log-spaced time, in which case dt is actually d(log10(t))
            tmin: the minimum time to consider (Myr, default 3.0 Myr)
            tmax: the maximum time to consider (Myr, default None which means we use the grid option 'max_evolution_time')
            max_evolution_time: overrides bse_options['max_evolution_time'] if set
            mindm: a tuple of tuples containing a mass range and minimum mass spacing in that range. The default is ((0.07,1.0,0.1),(1.0,300.0,1.0)) allocated a minimum dm of 0.1Msun in the mass range 0.07 to 1.0 Msun and 1.0Msun in the range 1.0 to 300.0 Msun. Anything you set overrides this. Note, if you use only one tuple, you must set it with a trailing comma, thus, e.g. ((0.07,1.0,0.1),). (default None)
            maxdm: a list of tuples similar to mindm but specifying a maximum mass spacing. In the case of maxdm, if the third option in each tuple is negative it is treated as a log step (its absolute value is used as the step).  (default None)
            fsample: a global sampling (Shannon-like) factor (<1) to improve resolution (default 1.0, set to smaller to improve resolution)
            factor: all masses generated are multiplied by this after generation
            showtable: if True, the mass list and times are shown to stdout after generation
            showlist: if True, show the mass list once generated
            logmasses: if True, the masses are logged with math.log()
            log10masses: if True, the masses are logged with math.log10()
            usecache: if True (the default) uses cached results if they are saved (in cachedir) and cachedir is not None
            cachedir: where the cache is stored. if None, defaults to grid_options['cache_dir']+'/const_dt_cache'
            vb : verbose logging flag (default False)

        Returns:
            Array of masses.

        Example:
            these are lines set as options to Population.add_grid_value(...)::

                # linear time bins of 1Gyr
                samplerfunc="self.const_dt(self,dt=1000,nres=100,mmin=0.07,mmax=2.0,showtable=True)"

                # logarithmic spacing in time, generally suitable for Galactic chemical evolution yield grids.
                samplerfunc="self.const_dt(self,dlogt=0.1,nres=100,mmin=0.07,mmax=80.0,maxdm=((0.07,1.0,0.1),(1.0,10.0,1.0),(10.0,80.0,2.0)),showtable=True,logspacing=True,fsample=1.0/4.0)"

        """

        if usecache:
            if cachedir is None:
                cachedir = self.grid_options["cache_dir"]

            if cachedir is not None:
                cachedir += "/const_dt_cache"
                cache = diskcache.Cache(cachedir)
                print(
                    "Use const_dt cache in {} [cache object {}]".format(cachedir, cache)
                )
            else:
                print("const_dt uses no cache")
                cache = None

        def _const_dt_wrapper(
            cachedir=None,
            num_cores=None,
            bse_options=None,
            dt=1000.0,
            dlogt=0.1,
            mmin=0.07,
            mmax=100.0,
            nres=1000,
            logspacing=False,
            tmin=3.0,  # start at 3Myr
            tmax=None,  # use max_evolution_time by default
            max_evolution_time=None,
            mindm=None,  # tuple of tuples
            maxdm=((0.07, 1.0, 0.1), (1.0, 300.0, 1.0)),  # tuple of tuples
            fsample=1.0,
            factor=1.0,
            logmasses=False,
            log10masses=False,
            showlist=False,
            showtable=False,
            usecache=True,
            vb=False,
        ):
            """
            Wrapper function for the const_dt funtion which handles verbose logging and filtering of arguments
            """

            print(
                "call _const_dt num_cores={} dt={} dlogt={} mmin={} mmax={} nres={} logspacing={} tmin={} mindm={} maxdm={} fsample={} factor={} logmasses={} log10masses={} showlist={} usecache={} [cache={} vb={}]".format(
                    num_cores,
                    dt,
                    dlogt,
                    mmin,
                    mmax,
                    nres,
                    logspacing,
                    tmin,
                    mindm,
                    maxdm,
                    fsample,
                    factor,
                    logmasses,
                    log10masses,
                    showlist,
                    usecache,
                    cache,
                    vb,
                )
            )

            if vb:
                traceback.print_stack()

            # strip bse_options of options that will not affect
            # _const_dt
            bse_stripped = bse_options.copy()

            del_keys = ["multiplicity"]
            for del_key in del_keys:
                if del_key in bse_stripped:
                    del bse_stripped[del_key]

            # make a JSON string of the options (this can be
            # used to check the cache)
            bse_options_json = json.dumps(
                bse_stripped, sort_keys=True, ensure_ascii=False
            )
            if vb:
                print("BSE options JSON:", bse_options_json)

            return _const_dt(
                cachedir=cachedir,
                num_cores=num_cores,
                bse_options_json=bse_options_json,
                dt=dt,
                dlogt=dlogt,
                mmin=mmin,
                mmax=mmax,
                nres=nres,
                logspacing=logspacing,
                tmin=tmin,
                tmax=tmax,
                max_evolution_time=max_evolution_time,
                mindm=mindm,
                maxdm=maxdm,
                fsample=fsample,
                logmasses=logmasses,
                log10masses=log10masses,
                showlist=showlist,
                showtable=showtable,
                usecache=usecache,
            )

        # if we want to use the cache, set the __decorator
        # to just be the cache.memoize function, otherwise
        # make it a wrapped function that just returns the
        # _const_dt function acting on its arguments
        def __dummy_decorator(func):
            """
            Placeholder decorator function
            """

            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                """
                Dummy wrapper function
                """

                return func(*args, **kwargs)

            return wrapped
                
        if cache is not None:
            __decorator = cache.memoize
        else:
            __decorator = __dummy_decorator

        #@cache.memoize()    
        @__decorator() # note: () works with python3.9+, maybe not for 3.8
        def _const_dt(
            cachedir=None,
            num_cores=None,
            bse_options_json=None,  # JSON string
            dt=1000.0,
            dlogt=0.1,
            mmin=0.07,
            mmax=100.0,
            nres=1000,
            logspacing=False,
            tmin=3.0,  # start at 3Myr
            tmax=None,  # use max_evolution_time by default
            max_evolution_time=None,
            mindm=None,  # tuple of tuples
            maxdm=((0.07, 1.0, 0.1), (1.0, 300.0, 1.0)),  # tuple of tuples
            fsample=1.0,
            factor=1.0,
            logmasses=False,
            log10masses=False,
            showlist=False,
            showtable=False,
            usecache=True,
        ):
            """
            first thing to do is make a stellar lifetime table

            we should use the bse_options_json passed in
            so our lifetime_population uses the same physics
            as the main grid

            TODO: Describe this function better with arguments and
            """

            # convert bse_options to dict
            bse_options = json.loads(bse_options_json)

            # perhaps override max_evolution_time
            if max_evolution_time:
                bse_options["max_evolution_time"] = max_evolution_time

            from binarycpython.utils.grid import Population
            lifetime_population = Population()
            lifetime_population.bse_options = bse_options

            # we only want to evolve the star during nuclear burning,
            # we don't want a dry run of the grid
            # we want to use the right number of CPU cores
            lifetime_population.set(
                do_dry_run=False,
                num_cores=num_cores,
                max_stellar_type_1=10,
                save_ensemble_chunks=False,
                symlink_latest_gridcode=False,
                modulo=1,
                start_at=0,
                slurm=0,
                condor=0,
                multiplicity=1,
                ensemble=0,
                ensemble_dt=1e3,
                ensemble_logdt=0.1,
                # for debugging
                verbosity=1,
                log_dt=1,
            )

            # make a grid in M1
            lifetime_population.add_grid_variable(
                name="lnM_1",
                parameter_name="M_1",
                longname="log Primary mass",  # == single-star mass
                valuerange=[math.log(mmin), math.log(mmax)],
                samplerfunc="self.const_linear(math.log({mmin}),math.log({mmax}),{nres})".format(
                    mmin=mmin, mmax=mmax, nres=nres
                ),
                probdist="1",  # dprob/dm1 : we don't care, so just set it to 1
                dphasevol="dlnM_1",
                precode="M_1=math.exp(lnM_1)",
                condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
                gridtype="edge",
            )

            # set up the parse function
            def _parse_function(self, output):
                """
                Parse function for the const_dt binary_c calls
                """

                if output:
                    for line in output.splitlines():
                        data = line.split()
                        if data[0] == "SINGLE_STAR_LIFETIME":
                            # append (log10(mass), log10(lifetime)) tuples
                            logm = math.log10(float(data[1]))
                            logt = math.log10(float(data[2]))
                            # print(line)
                            # print("logM=",logm,"M=",10.0**logm," -> logt=",logt)
                            self.grid_results["interpolation table m->t"][logm] = logt
                            self.grid_results["interpolation table t->m"][logt] = logm

            lifetime_population.set(
                parse_function=_parse_function,
            )

            # run to build the interpolation table
            print(
                "Running population to make lifetime interpolation table, please wait"
            )
            lifetime_population.evolve()
            # print("Data table",lifetime_population.grid_results['interpolation table t->m'])

            if (
                "interpolation table t->m" not in lifetime_population.grid_results
                or len(
                    lifetime_population.grid_results["interpolation table t->m"].keys()
                )
                == 0
            ):
                print(
                    "\n\n\nError: The t->m lifetime table is empty. One usual cause for this is that the tmax or max_evolution_time option (currently passed in to const_dt as {tmax}) is too short for there to be any entries in the table before the first timestep. Try increasing tmax and max_evolution_time, shorten the timestep or, if using log times, set tstart to be closer to 0.\n".format(
                        tmax=tmax
                    )
                )
                sys.exit()

            # convert to nested lists for the interpolator
            #
            # make time -> mass table
            data_table_time_mass = []
            times = sorted(
                lifetime_population.grid_results["interpolation table t->m"].keys()
            )
            for time in times:
                mass = lifetime_population.grid_results["interpolation table t->m"][
                    time
                ]
                # we have to make sure the time is monotonic (not guaranteed at high mass)
                if len(data_table_time_mass) == 0:
                    data_table_time_mass.append([time, mass])
                elif mass < data_table_time_mass[-1][1]:
                    data_table_time_mass.append([time, mass])

            # make mass -> time table
            data_table_mass_time = []
            masses = sorted(
                lifetime_population.grid_results["interpolation table m->t"].keys()
            )
            for mass in masses:
                time = lifetime_population.grid_results["interpolation table m->t"][
                    mass
                ]
                data_table_mass_time.append([mass, time])

            # set up interpolators
            interpolator_time_mass = py_rinterpolate.Rinterpolate(
                table=data_table_time_mass,
                nparams=1,
                ndata=1,
                verbosity=0,  # mass  # lifetime
            )
            interpolator_mass_time = py_rinterpolate.Rinterpolate(
                table=data_table_mass_time,
                nparams=1,
                ndata=1,
                verbosity=0,  # lifetime  # mass
            )

            def _mass_from_time(linear_time):
                """
                Function to get a mass given a time, calculated by using the interpolator_time_mass
                """

                return (
                    10.0
                    ** interpolator_time_mass.interpolate([math.log10(linear_time)])[0]
                )

            def _time_from_mass(mass):
                """
                Function to get a time given a mass, calculated by using the interpolator_time_mass
                """

                return 10.0 ** interpolator_mass_time.interpolate([math.log10(mass)])[0]

            def _uniq(_list):
                """
                Function to return a list containing only unique elements

                TODO: move this to the functions file
                """

                return sorted(list(set(_list)))

            def _format(_list):
                """
                Function to format a list of numbers as %g strings
                """

                return [float("{x:g}".format(x=x)) for x in _list]

            # construct mass list, always include the min and max
            mass_list = [mmin, mmax]

            # first, make sure the stars are separated by only
            # maxdm
            if maxdm:
                for x in maxdm:
                    range_min = x[0]
                    range_max = x[1]
                    dm = x[2]
                    if dm < 0.0:
                        # use log scale
                        dlogm = -dm
                        logm = math.log(mmin)
                        logmmax = math.log(mmax)
                        logrange_min = math.log(range_min)
                        logrange_max = math.log(range_max)
                        while logm <= logmmax:
                            if logrange_min <= logm <= logrange_max:
                                mass_list.append(math.exp(logm))
                            logm += dlogm
                    else:
                        # use linear scale
                        m = mmin
                        while m <= mmax:
                            if range_min <= m <= range_max:
                                mass_list.append(m)
                            m += dm

            # start time loop at tmax or max_evolution_time
            t = tmax if tmax else bse_options["max_evolution_time"]

            # set default mass list
            if logspacing:
                logt = math.log10(t)
                logtmin = math.log10(tmin)
                while logt > logtmin:
                    m = _mass_from_time(10.0 ** logt)
                    mass_list.append(m)
                    logt = max(logtmin, logt - dlogt * fsample)
            else:
                while t > tmin:
                    m = _mass_from_time(t)
                    mass_list.append(m)
                    t = max(tmin, t - dt * fsample)

            # make mass list unique
            mass_list = _uniq(mass_list)

            if mindm:
                for x in mindm:
                    range_min = x[0]
                    range_max = x[1]
                    mindm = x[2]
                    # impose a minimum dm: if two masses in the list
                    # are separated by < this, remove the second
                    for index, mass in enumerate(mass_list):
                        if index > 0 and range_min <= mass <= range_max:
                            dm = mass_list[index] - mass_list[index - 1]
                            if dm < mindm:
                                mass_list[index - 1] = 0.0
                    mass_list = _uniq(mass_list)
                    if mass_list[0] == 0.0:
                        mass_list.remove(0.0)

            # apply multiplication factor if given
            if factor and factor != 1.0:
                mass_list = [m * factor for m in mass_list]

            # reformat numbers
            mass_list = _format(mass_list)

            # show the mass<>time table?
            if showtable:
                twas = 0.0
                logtwas = 0.0
                for i, m in enumerate(mass_list):
                    t = _time_from_mass(m)
                    logt = math.log10(t)
                    if twas > 0.0:
                        print(
                            "{i:4d} m={m:13g} t={t:13g} log10(t)={logt:13g} dt={dt:13g} dlog10(t)={dlogt:13g}".format(
                                i=i,
                                m=m,
                                t=t,
                                logt=logt,
                                dt=twas - t,
                                dlogt=logtwas - logt,
                            )
                        )
                    else:
                        print(
                            "{i:4d} m={m:13g} t={t:13g} log10(t)={logt:13g}".format(
                                i=i, m=m, t=t, logt=logt
                            )
                        )
                        twas = t
                        logtwas = logt
                    sys.exit()

            # return the mass list as a numpy array
            mass_array = np.unique(np.array(mass_list))

            # perhaps log the masses
            if logmasses:
                mass_array = np.log(mass_array)
            if log10masses:
                mass_array = np.log10(mass_array)

            return mass_array

        # call _const_dt and return the mass_list
        #
        # Note: because _const_dt is cached to disk, calling it may
        #       use the cached result.
        #
        # Note: we send a sorted JSON string instead of the
        #       bse_options dict to make sure the order is preserved

        mass_list = _const_dt_wrapper(
            cachedir=cachedir,
            num_cores=self.grid_options["num_cores"],
            bse_options=self.bse_options,
            **kwargs,
        )
        if cache:
            cache.close()

        if kwargs.get("showlist", True):
            print("const_dt mass list ({} masses)\n".format(len(mass_list)), mass_list)

        return mass_list

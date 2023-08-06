"""
File containing the class extension for the population object that contains cache functionality

Module containing (e.g. LRU) cache functionality for binary_c-python.

We use cachetools when possible because this allows us to set up the
cache of the appropriate size for the task in the grid_options dict.
Please see the LRU_* options in there.
"""

# pylint: disable=E1101

import os
import time
import tempfile
import importlib
import getpass
import contextlib

import cachetools


class cache:
    """
    Class extension for the population object that contains cache functionality
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def default_cache_dir(self):
        """
        Return a default cache directory path for binary_c-python, or None if we cannot find one. This is used in grid_options_defaults.py
        """

        error_string = "__*ERR*__"  # string that cannot be a path
        for path in [
            os.path.join(os.environ.get("HOME", error_string), ".cache"),
            os.path.join(os.environ.get("TMP", error_string), "cache"),
            os.path.join("var", "tmp", getpass.getuser(), "cache"),
        ]:
            if not error_string in path and os.path.isdir(path):
                return os.path.join(path, "binary_c")
        return None

    class NullCache(cachetools.Cache):
        """
        A cachetools cache object that does as little as possible and never matches.
        """

        def __init__(self, *args, **kwargs):
            """
            Init function for the spacing_functions class

            TODO: is this class necesarry to be defined *within* the cache class? can't it just be outside?
            """

            return None

        def popitem(self):
            """
            pop function placeholder
            """

            return  # do nothing

        def __getitem__(self, key):
            """
            getter function placeholder
            """

            return self.__missing__(key)

        def __setitem__(self, key, value):
            """
            Setter function placeholder
            """

            return

        def __delitem__(self, key):
            """
            deleter function placeholder
            """

            return

    def setup_function_cache(self, vb=False, cachetype=None):
        """
        Function to wrap binary_c-python's functions in function cache.

        The functions listed in self.grid_options['function_cache_functions'] are
        given caches of size self.grid_options['function_cache_size'][func]

        Args: None
        """

        # add our custom NullCache to the cachetools selection
        setattr(cachetools, "NullCache", self.NullCache)

        if not self.grid_options["function_cache"]:
            # no function cache: set all to NullCache
            # TODO: This cachetype(Nullcache) is wrong.
            for func in self.grid_options["function_cache_functions"].keys():
                self.function_cache[func] = cachetype(NullCache)

        for func in self.grid_options["function_cache_functions"].keys():
            (maxsize, cachetype, testargs) = self.grid_options[
                "function_cache_functions"
            ].get(func)

            # which cache should we use?
            if cachetype:
                # use type passed in, if given
                usecachetype = cachetype
            elif not self.grid_options["function_cache"]:
                # function cache is disabled, use NoCache
                usecachetype = "NoCache"
            else:
                if cachetype is None:
                    # use the default type
                    usecachetype = self.grid_options["function_cache_default_type"]
                else:
                    # use type passed in
                    usecachetype = cachetype

            if vb:
                print(
                    "Setup cache for func {func} : maxsize={maxsize}, cachetype={cachetype}, testargs={testargs}-> use {usecachetype}".format(
                        func=func,
                        maxsize=maxsize,
                        cachetype=cachetype,
                        testargs=testargs,
                        usecachetype=usecachetype,
                    )
                )

            if usecachetype == "TTLCache":
                extra_cacheargs = [self.grid_options["function_cache_TTL"]]
            else:
                extra_cacheargs = []

            # detect if the function is already wrapped
            x = func.split(".")
            modulename = "binarycpython.utils.population_extensions." + x[0]
            module = importlib.import_module(modulename)
            _method = eval(
                "module.{}.{}".format(x[0], x[1])
            )  # TODO: we can do this differently with some .get call instead of eval
            _wrapped = getattr(_method, "__wrapped__", False)

            # if function is wrapped...
            if _wrapped and id(_method) != id(_wrapped):
                # save the wrapped function (this calls the cache)
                if func not in self.cached_function_cache:
                    self.cached_function_cache[func] = _method
                    self.original_function_cache[func] = _wrapped

                if usecachetype == "NoCache":
                    # unwrap if we're after NoCache
                    _code = "module.{}.{} = _wrapped".format(x[0], x[1])
                    exec(_code)
            else:
                # function isn't wrapped, which means it was previously
                # unwrapped, so rewrap it if not using NoCache
                if usecachetype != "NoCache" and func in self.cached_function_cache:
                    _code = 'module.{}.{} = self.cached_function_cache["{}"]'.format(
                        x[0], x[1], func
                    )
                    exec(_code)

            # check we're not still wrapped
            _method = eval("module" + "." + x[0] + "." + x[1])
            _wrapped = getattr(_method, "__wrapped__", False)

            # if NoCache (explicity use no cache), just use NullCache
            # (it's never actually set)
            if usecachetype == "NoCache":
                cachetools_func = getattr(cachetools, "NullCache")
            else:
                cachetools_func = getattr(cachetools, usecachetype)

            if maxsize == 0:
                maxsize = self.grid_options["function_cache_default_maxsize"]

            if vb:
                print(
                    "Make function cache for func {func}, maxsize {maxsize}".format(
                        func=func, maxsize=maxsize
                    )
                )

            # set up cache function args
            if maxsize is None:
                args = [2]
            else:
                args = [maxsize]
            args += extra_cacheargs

            # clear any existing cache
            if func in self.caches:
                try:
                    self.caches[func].cache_clear()
                except:
                    pass
                del self.caches[func]

            # set up new cache using the appropriate cachetools function
            if usecachetype != "NoCache":
                self.caches[func] = cachetools_func(*args)

    def test_caches(self, dt=5.0):
        """
        Function to test cache speeds of the functions that binary_c-python automatically caches.

        Args:
            dt (default 5) in seconds the length of each test. Long is more accurate, but takes longer.
        """

        # loop lists
        cachetypes = ("NoCache", "NullCache", "FIFOCache", "LRUCache", "TTLCache")
        functions = self.grid_options["function_cache_functions"].keys()
        maxsizes = (0, 1, 2, 4, 8, 16, 32, 64, 128, 256)

        self.grid_options["function_cache"] = True
        for n, func in enumerate(functions):
            print("Cache speed test of function {func}".format(func=func))
            print("{:18s}".format(""), end="")
            for x, maxsize in enumerate(maxsizes):
                print("{:>9s}".format(str(maxsize)), end="")
            print("")

            best = 0
            best_type = None
            best_maxsize = None
            for y, type in enumerate(cachetypes):
                print("{:18s}".format(type), end="")
                self.grid_options["function_cache_default_type"] = type
                self.setup_function_cache()
                (maxsize, cachetype, testargs) = self.grid_options[
                    "function_cache_functions"
                ].get(func)

                # TODO: Make this part better: needs to be able to handle any depth
                x = func.split(".")
                modulename = "binarycpython.utils.population_extensions." + x[0]
                module = importlib.import_module(modulename)
                _method = eval("module.{}.{}".format(x[0], x[1]))

                if testargs:

                    def _func_wrap(*args, **kwargs):
                        """
                        wrap to return args and kwargs

                        TODO: i think this function can be defined elsewhere
                        """

                        return (args, kwargs)

                    args, kwargs = eval("_func_wrap({})".format(testargs))
                    for x, maxsize in enumerate(maxsizes):
                        if type == "NoCache" and maxsize > 0:
                            continue

                        # redirect stdout to prevent lots of output
                        with contextlib.redirect_stdout(None):

                            # loop for dt seconds
                            tfin = dt + time.time()
                            count = 0
                            try:
                                while time.time() < tfin:
                                    _method(self, *args, **kwargs)
                                    count += 1
                            # TODO: specify the exception
                            except Exception as e:
                                print("Cache call failed:", e)
                                self.exit(1)

                        if count < 99999:
                            print("{:9d}".format(count), end="")
                        else:
                            print("{:9.2e}".format(float(count)), end="")

                        if count > best:
                            best = count
                            best_type = type
                            best_maxsize = maxsize
                    print("")

            print(
                "Best cache type {type} with maxsize {maxsize}\n".format(
                    type=best_type, maxsize=best_maxsize
                )
            )

    """
Cache speed test of function distribution_functions.powerlaw_constant
                          0        1        2        4        8       16       32       64      128      256
NoCache            6.28e+07
NullCache          6.39e+07 6.40e+07 6.41e+07 6.39e+07 6.44e+07 6.43e+07 6.37e+07 6.40e+07 6.38e+07 6.40e+07
FIFOCache          6.41e+07 6.37e+07 6.40e+07 6.39e+07 6.40e+07 6.37e+07 6.41e+07 6.40e+07 6.41e+07 6.40e+07
LRUCache           6.42e+07 6.41e+07 6.42e+07 6.41e+07 6.38e+07 6.43e+07 6.41e+07 6.43e+07 6.40e+07 6.41e+07
TTLCache           6.41e+07 6.35e+07 6.37e+07 6.39e+07 6.37e+07 6.42e+07 6.39e+07 6.38e+07 6.37e+07 6.38e+07
Best cache type NullCache with maxsize 8

Cache speed test of function distribution_functions.calculate_constants_three_part_powerlaw
                          0        1        2        4        8       16       32       64      128      256
NoCache            1.44e+07
NullCache          9.13e+06 9.18e+06 9.20e+06 9.21e+06 9.20e+06 9.12e+06 9.18e+06 9.18e+06 9.15e+06 9.12e+06
FIFOCache          2.53e+07 2.52e+07 2.51e+07 2.50e+07 2.51e+07 2.52e+07 2.52e+07 2.52e+07 2.52e+07 2.51e+07
LRUCache           1.62e+07 1.62e+07 1.62e+07 1.62e+07 1.62e+07 1.62e+07 1.62e+07 1.62e+07 1.62e+07 1.62e+07
TTLCache           1.43e+07 1.43e+07 1.43e+07 1.43e+07 1.43e+07 1.44e+07 1.42e+07 1.43e+07 1.43e+07 1.43e+07
Best cache type FIFOCache with maxsize 0

Cache speed test of function distribution_functions.gaussian_normalizing_const
                          0        1        2        4        8       16       32       64      128      256
NoCache               64183
NullCache             64340    64339    64544    64260    64491    64382    64400    63974    63954    64338
FIFOCache          2.62e+07 2.62e+07 2.62e+07 2.61e+07 2.61e+07 2.59e+07 2.61e+07 2.59e+07 2.57e+07 2.59e+07
LRUCache           1.66e+07 1.66e+07 1.65e+07 1.66e+07 1.65e+07 1.65e+07 1.64e+07 1.65e+07 1.64e+07 1.65e+07
TTLCache           1.42e+07 1.44e+07 1.42e+07 1.44e+07 1.43e+07 1.43e+07 1.42e+07 1.44e+07 1.42e+07 1.44e+07
Best cache type FIFOCache with maxsize 1

Cache speed test of function spacing_functions.const_linear
                          0        1        2        4        8       16       32       64      128      256
NoCache            1.22e+06
NullCache          1.05e+06 1.05e+06 1.06e+06 1.05e+06 1.05e+06 1.06e+06 1.05e+06 1.05e+06 1.05e+06 1.05e+06
FIFOCache          2.85e+07 2.85e+07 2.86e+07 2.85e+07 2.84e+07 2.85e+07 2.84e+07 2.84e+07 2.85e+07 2.81e+07
LRUCache           1.77e+07 1.79e+07 1.73e+07 1.73e+07 1.76e+07 1.79e+07 1.76e+07 1.74e+07 1.74e+07 1.72e+07
TTLCache           1.46e+07 1.49e+07 1.50e+07 1.53e+07 1.51e+07 1.53e+07 1.52e+07 1.51e+07 1.47e+07 1.50e+07
Best cache type FIFOCache with maxsize 2

Cache speed test of function spacing_functions.const_int
                          0        1        2        4        8       16       32       64      128      256
NoCache            4.23e+07
NullCache          1.65e+07 1.66e+07 1.65e+07 1.64e+07 1.66e+07 1.65e+07 1.59e+07 1.59e+07 1.65e+07 1.64e+07
FIFOCache          2.86e+07 2.86e+07 2.87e+07 2.86e+07 2.84e+07 2.86e+07 2.81e+07 2.79e+07 2.78e+07 2.85e+07
LRUCache           1.78e+07 1.78e+07 1.77e+07 1.75e+07 1.77e+07 1.78e+07 1.78e+07 1.78e+07 1.74e+07 1.75e+07
TTLCache           1.55e+07 1.54e+07 1.55e+07 1.54e+07 1.55e+07 1.49e+07 1.52e+07 1.51e+07 1.52e+07 1.54e+07
Best cache type NoCache with maxsize 0

Cache speed test of function spacing_functions.const_ranges
                          0        1        2        4        8       16       32       64      128      256
NoCache            2.54e+05
NullCache          2.25e+05 2.25e+05 2.24e+05 2.25e+05 2.25e+05 2.25e+05 2.25e+05 2.26e+05 2.25e+05 2.26e+05
FIFOCache          2.58e+07 2.55e+07 2.53e+07 2.54e+07 2.56e+07 2.57e+07 2.56e+07 2.57e+07 2.58e+07 2.58e+07
LRUCache           1.62e+07 1.63e+07 1.62e+07 1.62e+07 1.61e+07 1.62e+07 1.62e+07 1.62e+07 1.61e+07 1.63e+07
TTLCache           1.41e+07 1.43e+07 1.42e+07 1.42e+07 1.40e+07 1.42e+07 1.42e+07 1.43e+07 1.40e+07 1.43e+07
Best cache type FIFOCache with maxsize 128

Cache speed test of function spacing_functions.gaussian_zoom
                          0        1        2        4        8       16       32       64      128      256
NoCache               24703
NullCache             24872    24935    24927    24896    24968    24964    24882    24840    24873    24913
FIFOCache          2.54e+07 2.54e+07 2.54e+07 2.54e+07 2.53e+07 2.52e+07 2.53e+07 2.51e+07 2.52e+07 2.52e+07
LRUCache           1.63e+07 1.63e+07 1.63e+07 1.64e+07 1.63e+07 1.64e+07 1.63e+07 1.63e+07 1.63e+07 1.63e+07
TTLCache           1.43e+07 1.43e+07 1.42e+07 1.42e+07 1.43e+07 1.42e+07 1.43e+07 1.43e+07 1.43e+07 1.43e+07
Best cache type FIFOCache with maxsize 0
    """

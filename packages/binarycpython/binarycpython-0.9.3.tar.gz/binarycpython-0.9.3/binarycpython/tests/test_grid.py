"""
Unit tests for the grid module

TODO: jobID
TODO: exit
TODO: _set_nprocesses
TODO: _pre_run_setup
TODO: clean
TODO: _evolve_population
TODO: _system_queue_filler
TODO: _evolve_population_grid
TODO: _evolve_system_mp
TODO: _parent_signal_handler
TODO: _child_signal_handler
TODO: _process_run_population_grid
TODO: _cleanup
TODO: _dry_run
TODO: _dry_run_source_file
TODO: _load_source_file
TODO: was_killed
TODO: _check_binary_c_error

TODO: Before running the non-unit tests to cover functions like evolve, we need to run the unit tests
"""

import os
import sys
import json
import gzip
import shutil
import unittest
import numpy as np

from binarycpython.utils.functions import temp_dir, Capturing, remove_file, bin_data
from binarycpython.utils.dicts import (
    merge_dicts,
)

from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test_grid")
shutil.rmtree(TMP_DIR)
os.makedirs(TMP_DIR, exist_ok=True)

TEST_VERBOSITY = 1


def parse_function_test_grid_evolve_2_threads_with_custom_logging(self, output): # pragma: no cover
    """
    Simple parse function that directly appends all the output to a file
    """

    # Get some information from the
    data_dir = self.custom_options["data_dir"]

    # make outputfilename
    output_filename = os.path.join(
        data_dir,
        "test_grid_evolve_2_threads_with_custom_logging_outputfile_population_{}_thread_{}.dat".format(
            self.grid_options["_population_id"], self.process_ID
        ),
    )

    # Check directory, make if necessary
    os.makedirs(data_dir, exist_ok=True)

    if not os.path.exists(output_filename):
        with open(output_filename, "w") as first_f:
            first_f.write(output + "\n")
    else:
        with open(output_filename, "a") as first_f:
            first_f.write(output + "\n")


def parse_function_adding_results(self, output): # pragma: no cover
    """
    Example parse function
    """

    seperator = " "

    parameters = ["time", "mass", "zams_mass", "probability", "stellar_type"]

    self.grid_results["example"]["count"] += 1

    # Go over the output.
    for line in output.splitlines():
        headerline = line.split()[0]

        # CHeck the header and act accordingly
        if headerline == "EXAMPLE_OUTPUT":
            values = line.split()[1:]

            # Bin the mass probability
            self.grid_results["example"]["mass"][
                bin_data(float(values[2]), binwidth=0.5)
            ] += float(values[3])

            #
            if not len(parameters) == len(values):
                print("Number of column names isnt equal to number of columns")
                raise ValueError

    # record the probability of this line (Beware, this is meant to only be run once for each system. its a controls quantity)
    self.grid_results["example"]["probability"] += float(values[3])


class test__setup(unittest.TestCase):
    """
    Unittests for _setup function
    """

    def test_setup(self):
        with Capturing() as _:
            self._test_setup()

    def _test_setup(self):
        """
        Unittests for function _setup
        """
        test_pop = Population(tmp_dir=TMP_DIR)

        self.assertTrue("orbital_period" in test_pop.defaults)
        self.assertTrue("metallicity" in test_pop.defaults)
        self.assertNotIn("help_all", test_pop.cleaned_up_defaults)
        self.assertEqual(test_pop.bse_options, {})
        self.assertEqual(test_pop.custom_options, {})
        self.assertEqual(test_pop.argline_dict, {})
        self.assertEqual(test_pop.persistent_data_memory_dict, {})
        self.assertTrue(test_pop.grid_options["parse_function"] is None)
        self.assertTrue(isinstance(test_pop.grid_options["_main_pid"], int))


class test_set(unittest.TestCase):
    """
    Unittests for _setup function
    """

    def test_set(self):
        with Capturing() as _:
            self._test_set()

    def _test_set(self):
        """
        Unittests for function set
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(num_cores=2, verbosity=TEST_VERBOSITY)
        test_pop.set(M_1=10)
        test_pop.set(data_dir="/tmp/binary_c_python")
        test_pop.set(ensemble_filter_SUPERNOVAE=1, ensemble_dt=1000)

        self.assertIn("data_dir", test_pop.custom_options)
        self.assertEqual(test_pop.custom_options["data_dir"], "/tmp/binary_c_python")

        #
        self.assertTrue(test_pop.bse_options["M_1"] == 10)
        self.assertTrue(test_pop.bse_options["ensemble_filter_SUPERNOVAE"] == 1)

        #
        self.assertTrue(test_pop.grid_options["num_cores"] == 2)


class test_cmdline(unittest.TestCase):
    """
    Unittests for cmdline function
    """

    def test_cmdline(self):
        with Capturing() as _:
            self._test_cmdline()

    def _test_cmdline(self):
        """
        Unittests for function parse_cmdline
        """

        # copy old sys.argv values
        prev_sysargv = sys.argv.copy()

        # make a dummy cmdline arg input
        sys.argv = [
            "script",
            "metallicity=0.0002",
            "num_cores=2",
            "data_dir=/tmp/binary_c_python",
        ]

        # Set up population
        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(data_dir="/tmp", verbosity=TEST_VERBOSITY)

        # parse arguments
        test_pop.parse_cmdline()

        # metallicity
        self.assertTrue(isinstance(test_pop.bse_options["metallicity"], str))
        self.assertTrue(test_pop.bse_options["metallicity"] == "0.0002")

        # Amt cores
        self.assertTrue(isinstance(test_pop.grid_options["num_cores"], int))
        self.assertTrue(test_pop.grid_options["num_cores"] == 2)

        # datadir
        self.assertTrue(isinstance(test_pop.custom_options["data_dir"], str))
        self.assertTrue(test_pop.custom_options["data_dir"] == "/tmp/binary_c_python")

        # put back the other args if they exist
        sys.argv = prev_sysargv.copy()


class test__return_argline(unittest.TestCase):
    """
    Unittests for _return_argline function
    """

    def test__return_argline(self):
        with Capturing() as _:
            self._test__return_argline()

    def _test__return_argline(self):
        """
        Unittests for the function _return_argline
        """

        # Set up population
        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(metallicity=0.02, verbosity=TEST_VERBOSITY)
        test_pop.set(M_1=10)

        argline = test_pop._return_argline()
        self.assertTrue(argline == "binary_c M_1 10 metallicity 0.02")

        # custom dict
        argline2 = test_pop._return_argline(
            {"example_parameter1": 10, "example_parameter2": "hello"}
        )
        self.assertTrue(
            argline2 == "binary_c example_parameter1 10 example_parameter2 hello"
        )


class test_return_population_settings(unittest.TestCase):
    """
    Unittests for return_population_settings function
    """

    def test_return_population_settings(self):
        with Capturing() as _:
            self._test_return_population_settings()

    def _test_return_population_settings(self):
        """
        Unittests for the function return_population_settings
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(metallicity=0.02, verbosity=TEST_VERBOSITY)
        test_pop.set(M_1=10)
        test_pop.set(num_cores=2)
        test_pop.set(data_dir="/tmp")

        population_settings = test_pop.return_population_settings()

        self.assertIn("bse_options", population_settings)
        self.assertTrue(population_settings["bse_options"]["metallicity"] == 0.02)
        self.assertTrue(population_settings["bse_options"]["M_1"] == 10)

        self.assertIn("grid_options", population_settings)
        self.assertTrue(population_settings["grid_options"]["num_cores"] == 2)

        self.assertIn("custom_options", population_settings)
        self.assertTrue(population_settings["custom_options"]["data_dir"] == "/tmp")


class test_return_binary_c_defaults(unittest.TestCase):
    """
    Unittests for return_binary_c_defaults function
    """

    def test_return_binary_c_defaults(self):
        with Capturing() as _:
            self._test_return_binary_c_defaults()

    def _test_return_binary_c_defaults(self):
        """
        Unittests for the function return_binary_c_defaults
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        binary_c_defaults = test_pop.return_binary_c_defaults()
        self.assertIn("probability", binary_c_defaults)
        self.assertIn("phasevol", binary_c_defaults)
        self.assertIn("metallicity", binary_c_defaults)


class test_return_all_info(unittest.TestCase):
    """
    Unittests for return_all_info function
    """

    def test_return_all_info(self):
        with Capturing() as _:
            self._test_return_all_info()

    def _test_return_all_info(self):
        """
        Unittests for the function return_all_info
        Not going to do too much tests here, just check if they are not empty
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        all_info = test_pop.return_all_info()

        self.assertIn("population_settings", all_info)
        self.assertIn("binary_c_defaults", all_info)
        self.assertIn("binary_c_version_info", all_info)
        self.assertIn("binary_c_help_all", all_info)

        self.assertNotEqual(all_info["population_settings"], {})
        self.assertNotEqual(all_info["binary_c_defaults"], {})
        self.assertNotEqual(all_info["binary_c_version_info"], {})
        self.assertNotEqual(all_info["binary_c_help_all"], {})


class test_export_all_info(unittest.TestCase):
    """
    Unittests for export_all_info function
    """

    def test_export_all_info(self):
        with Capturing() as _:
            self._test_export_all_info()

    def _test_export_all_info(self):
        """
        Unittests for the function export_all_info
        """

        test_pop = Population(tmp_dir=TMP_DIR)

        test_pop.set(metallicity=0.02, verbosity=TEST_VERBOSITY)
        test_pop.set(M_1=10)
        test_pop.set(num_cores=2)
        test_pop.set(data_dir=TMP_DIR)

        # datadir
        settings_filename = test_pop.export_all_info(use_datadir=True)
        self.assertTrue(os.path.isfile(settings_filename))

        # We currently export the file as a gzip file so we need to take that into accoutn
        with gzip.open(settings_filename, "rb") as f:
            all_info = json.loads(f.read())

        #
        self.assertIn("population_settings", all_info)
        self.assertIn("binary_c_defaults", all_info)
        self.assertIn("binary_c_version_info", all_info)
        self.assertIn("binary_c_help_all", all_info)

        #
        self.assertNotEqual(all_info["population_settings"], {})
        self.assertNotEqual(all_info["binary_c_defaults"], {})
        self.assertNotEqual(all_info["binary_c_version_info"], {})
        self.assertNotEqual(all_info["binary_c_help_all"], {})

        # custom name
        # datadir
        settings_filename = test_pop.export_all_info(
            use_datadir=False,
            outfile=os.path.join(TMP_DIR, "example_settings.json"),
        )
        self.assertTrue(os.path.isfile(settings_filename))
        with open(settings_filename, "r") as f:
            all_info = json.loads(f.read())

        #
        self.assertIn("population_settings", all_info)
        self.assertIn("binary_c_defaults", all_info)
        self.assertIn("binary_c_version_info", all_info)
        self.assertIn("binary_c_help_all", all_info)

        #
        self.assertNotEqual(all_info["population_settings"], {})
        self.assertNotEqual(all_info["binary_c_defaults"], {})
        self.assertNotEqual(all_info["binary_c_version_info"], {})
        self.assertNotEqual(all_info["binary_c_help_all"], {})

        # wrong filename
        self.assertRaises(
            ValueError,
            test_pop.export_all_info,
            use_datadir=False,
            outfile=os.path.join(TMP_DIR, "example_settings.txt"),
        )


class test__cleanup_defaults(unittest.TestCase):
    """
    Unittests for _cleanup_defaults function
    """

    def test__cleanup_defaults(self):
        with Capturing() as _:
            self._test__cleanup_defaults()

    def _test__cleanup_defaults(self):
        """
        Unittests for the function _cleanup_defaults
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        cleaned_up_defaults = test_pop._cleanup_defaults()
        self.assertNotIn("help_all", cleaned_up_defaults)


class test__increment_probtot(unittest.TestCase):
    """
    Unittests for _increment_probtot function
    """

    def test__increment_probtot(self):
        with Capturing() as _:
            self._test__increment_probtot()

    def _test__increment_probtot(self):
        """
        Unittests for the function _increment_probtot
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop._increment_probtot(0.5)
        self.assertEqual(test_pop.grid_options["_probtot"], 0.5)


class test__increment_count(unittest.TestCase):
    """
    Unittests for _increment_count function
    """

    def test__increment_count(self):
        with Capturing() as _:
            self._test__increment_count()

    def _test__increment_count(self):
        """
        Unittests for the function _increment_count
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop._increment_count()
        self.assertEqual(test_pop.grid_options["_count"], 1)


class test__dict_from_line_source_file(unittest.TestCase):
    """
    Unittests for _dict_from_line_source_file function
    """

    def test__dict_from_line_source_file(self):
        with Capturing() as _:
            self._test__dict_from_line_source_file()

    def _test__dict_from_line_source_file(self):
        """
        Unittests for the function _dict_from_line_source_file
        """

        source_file = os.path.join(TMP_DIR, "example_source_file.txt")

        # write
        with open(source_file, "w") as f:
            f.write("binary_c M_1 10 metallicity 0.02\n")

        test_pop = Population(tmp_dir=TMP_DIR)

        # readout
        with open(source_file, "r") as f:
            for line in f.readlines():
                argdict = test_pop._dict_from_line_source_file(line)

                self.assertTrue(argdict["M_1"] == 10)
                self.assertTrue(argdict["metallicity"] == 0.02)


class test_evolve_single(unittest.TestCase):
    """
    Unittests for evolve_single function
    """

    def test_evolve_single(self):
        with Capturing() as _:
            self._test_evolve_single()

    def _test_evolve_single(self):
        """
        Unittests for the function evolve_single
        """

        CUSTOM_LOGGING_STRING_MASSES = """
        Printf("TEST_CUSTOM_LOGGING_1 %30.12e %g %g %g %g\\n",
            //
            stardata->model.time, // 1

            // masses
            stardata->common.zero_age.mass[0], //
            stardata->common.zero_age.mass[1], //

            stardata->star[0].mass,
            stardata->star[1].mass
            );
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(
            M_1=10,
            M_2=5,
            orbital_period=100000,
            metallicty=0.02,
            max_evolution_time=15000,
            verbosity=TEST_VERBOSITY,
        )

        test_pop.set(C_logging_code=CUSTOM_LOGGING_STRING_MASSES)

        output = test_pop.evolve_single()

        #
        self.assertTrue(len(output.splitlines()) > 1)
        self.assertIn("TEST_CUSTOM_LOGGING_1", output)

        #
        custom_logging_dict = {"TEST_CUSTOM_LOGGING_2": ["star[0].mass", "model.time"]}
        test_pop_2 = Population(tmp_dir=TMP_DIR)
        test_pop_2.set(
            M_1=10,
            M_2=5,
            orbital_period=100000,
            metallicty=0.02,
            max_evolution_time=15000,
            verbosity=TEST_VERBOSITY,
        )

        test_pop_2.set(C_auto_logging=custom_logging_dict)

        output_2 = test_pop_2.evolve_single()

        #
        self.assertTrue(len(output_2.splitlines()) > 1)
        self.assertIn("TEST_CUSTOM_LOGGING_2", output_2)


########
# Some tests that are not really -unit- tests
class test_resultdict(unittest.TestCase):
    """
    Unittests for bin_data
    """

    def test_adding_results(self):
        with Capturing() as _:
            self._test_adding_results()

    def _test_adding_results(self):
        """
        Function to test whether the results are properly added and combined
        """

        # Create custom logging statement
        custom_logging_statement = """
        if (stardata->model.time < stardata->model.max_evolution_time)
        {
            Printf("EXAMPLE_OUTPUT %30.16e %g %g %30.12e %d\\n",
                //
                stardata->model.time, // 1
                stardata->star[0].mass, // 2
                stardata->common.zero_age.mass[0], // 3
                stardata->model.probability, // 4
                stardata->star[0].stellar_type // 5
          );
        };
        /* Kill the simulation to save time */
        stardata->model.max_evolution_time = stardata->model.time - stardata->model.dtm;
        """

        example_pop = Population(tmp_dir=TMP_DIR)
        example_pop.set(verbosity=0)
        example_pop.set(
            max_evolution_time=15000,  # bse_options
            # grid_options
            num_cores=3,
            tmp_dir=TMP_DIR,
            # Custom options
            data_dir=os.path.join(TMP_DIR, "test_resultdict"),  # custom_options
            C_logging_code=custom_logging_statement,
            parse_function=parse_function_adding_results,
        )

        # Add grid variables
        resolution = {"M_1": 10}

        # Mass
        example_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[2, 150],
            samplerfunc="self.const_linear(math.log(2), math.log(150), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 150, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        ## Executing a population
        ## This uses the values generated by the grid_variables
        analytics = example_pop.evolve()

        #
        grid_prob = analytics["total_probability"]
        result_dict_prob = example_pop.grid_results["example"]["probability"]

        # amt systems
        grid_count = analytics["total_count"]
        result_dict_count = example_pop.grid_results["example"]["count"]

        # Check if the total probability matches
        self.assertAlmostEqual(
            grid_prob,
            result_dict_prob,
            places=12,
            msg="Total probability from grid {} and from result dict {} are not equal".format(
                grid_prob, result_dict_prob
            ),
        )

        # Check if the total count matches
        self.assertEqual(
            grid_count,
            result_dict_count,
            msg="Total count from grid {} and from result dict {} are not equal".format(
                grid_count, result_dict_count
            ),
        )

        # Check if the structure is what we expect. Note: this depends on the probability calculation. if that changes we need to recalibrate this
        test_case_dict = {
            2.25: 0.01895481306515,
            3.75: 0.01081338190204,
            5.75: 0.006168841009268,
            9.25: 0.003519213484031,
            13.75: 0.002007648361756,
            21.25: 0.001145327489437,
            33.25: 0.0006533888518775,
            50.75: 0.0003727466560393,
            78.25: 0.000212645301782,
            120.75: 0.0001213103421247,
        }

        self.assertEqual(
            test_case_dict, dict(example_pop.grid_results["example"]["mass"])
        )


class test_grid_evolve(unittest.TestCase):
    """
    Unittests for function Population.evolve()
    """

    def test_grid_evolve_1_thread(self):
        with Capturing() as _:
            self._test_grid_evolve_1_thread()

    def _test_grid_evolve_1_thread(self):
        """
        Unittests to see if 1 thread does all the systems
        """

        test_pop_evolve_1_thread = Population(tmp_dir=TMP_DIR)
        test_pop_evolve_1_thread.set(
            num_cores=1, M_2=1, orbital_period=100000, verbosity=TEST_VERBOSITY
        )

        resolution = {"M_1": 10}

        test_pop_evolve_1_thread.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop_evolve_1_thread.evolve()
        self.assertLess(
            np.abs(analytics["total_probability"] - 0.10820655287892997),
            1e-10,
            msg=analytics["total_probability"],
        )
        self.assertTrue(analytics["total_count"] == 10)

    def test_grid_evolve_2_threads(self):
        with Capturing() as _:
            self._test_grid_evolve_2_threads()

    def _test_grid_evolve_2_threads(self):
        """
        Unittests to see if multiple threads handle the all the systems correctly
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(
            num_cores=2, M_2=1, orbital_period=100000, verbosity=TEST_VERBOSITY
        )

        resolution = {"M_1": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        self.assertLess(
            np.abs(analytics["total_probability"] - 0.10820655287892997),
            1e-10,
            msg=analytics["total_probability"],
        )  #
        self.assertTrue(analytics["total_count"] == 10)

    def test_grid_evolve_2_threads_with_custom_logging(self):
        with Capturing() as _:
            self._test_grid_evolve_2_threads_with_custom_logging()

    def _test_grid_evolve_2_threads_with_custom_logging(self):
        """
        Unittests to see if multiple threads do the custom logging correctly
        """

        data_dir_value = os.path.join(TMP_DIR, "grid_tests")
        num_cores_value = 2
        custom_logging_string = 'Printf("MY_STELLAR_DATA_TEST_EXAMPLE %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));'

        test_pop = Population(tmp_dir=TMP_DIR)

        test_pop.set(
            num_cores=num_cores_value,
            verbosity=TEST_VERBOSITY,
            M_2=1,
            orbital_period=100000,
            data_dir=data_dir_value,
            C_logging_code=custom_logging_string,  # input it like this.
            parse_function=parse_function_test_grid_evolve_2_threads_with_custom_logging,
        )
        test_pop.set(ensemble=0)
        resolution = {"M_1": 2}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        output_names = [
            os.path.join(
                data_dir_value,
                "test_grid_evolve_2_threads_with_custom_logging_outputfile_population_{}_thread_{}.dat".format(
                    analytics["population_id"], thread_id
                ),
            )
            for thread_id in range(num_cores_value)
        ]

        for output_name in output_names:
            self.assertTrue(os.path.isfile(output_name))

            with open(output_name, "r") as f:
                output_string = f.read()

            self.assertIn("MY_STELLAR_DATA_TEST_EXAMPLE", output_string)

            remove_file(output_name)

    def test_grid_evolve_with_condition_error(self):
        with Capturing() as _:
            self._test_grid_evolve_with_condition_error()

    def _test_grid_evolve_with_condition_error(self):
        """
        Unittests to see if the threads catch the errors correctly.
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(
            num_cores=2, M_2=1, orbital_period=100000, verbosity=TEST_VERBOSITY
        )

        # Set the amt of failed systems that each thread will log
        test_pop.set(failed_systems_threshold=4)

        CUSTOM_LOGGING_STRING_WITH_EXIT = """
Exit_binary_c(BINARY_C_NORMAL_EXIT, "testing exits. This is part of the testing, don't worry");
Printf("TEST_CUSTOM_LOGGING_1 %30.12e %g %g %g %g\\n",
    //
    stardata->model.time, // 1

    // masses
    stardata->common.zero_age.mass[0], //
    stardata->common.zero_age.mass[1], //

    stardata->star[0].mass,
    stardata->star[1].mass
);
        """

        test_pop.set(C_logging_code=CUSTOM_LOGGING_STRING_WITH_EXIT)

        resolution = {"M_1": 10}
        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        self.assertLess(
            np.abs(analytics["total_probability"] - 0.10820655287892997),
            1e-10,
            msg=analytics["total_probability"],
        )  #
        self.assertEqual(analytics["failed_systems_error_codes"], [0])
        self.assertTrue(analytics["total_count"] == 10)
        self.assertTrue(analytics["failed_count"] == 10)
        self.assertTrue(analytics["errors_found"] is True)
        self.assertTrue(analytics["errors_exceeded"] is True)

        # test to see if 1 thread does all the systems

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(
            num_cores=2, M_2=1, orbital_period=100000, verbosity=TEST_VERBOSITY
        )
        test_pop.set(failed_systems_threshold=4)
        test_pop.set(C_logging_code=CUSTOM_LOGGING_STRING_WITH_EXIT)

        resolution = {"M_1": 10, "q": 2}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        test_pop.add_grid_variable(
            name="q",
            longname="Mass ratio",
            valuerange=["0.1/M_1", 1],
            samplerfunc="self.const_linear(0.1/M_1, 1, {})".format(resolution["q"]),
            probdist="self.flatsections(q, [{'min': 0.1/M_1, 'max': 1.0, 'height': 1}])",
            dphasevol="dq",
            precode="M_2 = q * M_1",
            parameter_name="M_2",
            # condition="M_1 in dir()",  # Impose a condition on this grid variable. Mostly for a check for yourself
            condition="'random_var' in dir()",  # This will raise an error because random_var is not defined.
        )

        # TODO: why should it raise this error? It should probably raise a valueerror when the limit is exceeded right?
        # DEcided to turn it off for now because there is not raise VAlueError in that chain of functions.
        # NOTE: Found out why this test was here. It is to do with the condition random_var in dir(), but I changed the behaviour from raising an error to continue. This has to do with the moe&distefano code that will loop over several multiplicities
        # TODO: make sure the continue behaviour is what we actually want.

        # self.assertRaises(ValueError, test_pop.evolve)

    def test_grid_evolve_no_grid_variables(self):
        with Capturing() as _:
            self._test_grid_evolve_no_grid_variables()

    def _test_grid_evolve_no_grid_variables(self):
        """
        Unittests to see if errors are raised if there are no grid variables
        """

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(
            num_cores=1, M_2=1, orbital_period=100000, verbosity=TEST_VERBOSITY
        )

        resolution = {"M_1": 10}
        self.assertRaises(ValueError, test_pop.evolve)

    def test_grid_evolve_2_threads_with_ensemble_direct_output(self):
        with Capturing() as _:
            self._test_grid_evolve_2_threads_with_ensemble_direct_output()

    def _test_grid_evolve_2_threads_with_ensemble_direct_output(self):
        """
        Unittests to see if multiple threads output the ensemble information to files correctly
        """

        data_dir_value = TMP_DIR
        num_cores_value = 2

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(
            num_cores=num_cores_value,
            verbosity=TEST_VERBOSITY,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
            ensemble_dt=1000,
        )
        test_pop.set(
            data_dir=TMP_DIR,
            combine_ensemble_with_thread_joining=False,
        )

        resolution = {"M_1": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()
        output_names = [
            os.path.join(
                data_dir_value,
                "ensemble_output_{}_{}.json".format(
                    analytics["population_id"], thread_id
                ),
            )
            for thread_id in range(num_cores_value)
        ]

        for output_name in output_names:
            self.assertTrue(os.path.isfile(output_name))

            with open(output_name, "r") as f:
                file_content = f.read()

                ensemble_json = json.loads(file_content)

                self.assertTrue(isinstance(ensemble_json, dict))
                self.assertNotEqual(ensemble_json, {})

                self.assertIn("number_counts", ensemble_json)
                self.assertNotEqual(ensemble_json["number_counts"], {})

    def test_grid_evolve_2_threads_with_ensemble_combining(self):
        with Capturing() as _:
            self._test_grid_evolve_2_threads_with_ensemble_combining()

    def _test_grid_evolve_2_threads_with_ensemble_combining(self):
        """
        Unittests to see if multiple threads correclty combine the ensemble data and store them in the grid
        """

        data_dir_value = TMP_DIR
        num_cores_value = 2

        test_pop = Population(tmp_dir=TMP_DIR)
        test_pop.set(
            num_cores=num_cores_value,
            verbosity=TEST_VERBOSITY,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
            ensemble_dt=1000,
        )
        test_pop.set(
            data_dir=TMP_DIR,
            combine_ensemble_with_thread_joining=True,
        )

        resolution = {"M_1": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics = test_pop.evolve()

        self.assertTrue(isinstance(test_pop.grid_ensemble_results["ensemble"], dict))
        self.assertNotEqual(test_pop.grid_ensemble_results["ensemble"], {})

        self.assertIn("number_counts", test_pop.grid_ensemble_results["ensemble"])
        self.assertNotEqual(
            test_pop.grid_ensemble_results["ensemble"]["number_counts"], {}
        )

    def test_grid_evolve_2_threads_with_ensemble_comparing_two_methods(self):
        with Capturing() as _:
            self._test_grid_evolve_2_threads_with_ensemble_comparing_two_methods()

    def _test_grid_evolve_2_threads_with_ensemble_comparing_two_methods(self):
        """
        Unittests to compare the method of storing the combined ensemble data in the object and writing them to files and combining them later. they have to be the same
        """

        data_dir_value = TMP_DIR
        num_cores_value = 2

        # First
        test_pop_1 = Population(tmp_dir=TMP_DIR)
        test_pop_1.set(
            num_cores=num_cores_value,
            verbosity=TEST_VERBOSITY,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
            ensemble_dt=1000,
        )
        test_pop_1.set(
            data_dir=TMP_DIR,
            combine_ensemble_with_thread_joining=True,
        )

        resolution = {"M_1": 10}

        test_pop_1.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics_1 = test_pop_1.evolve()
        ensemble_output_1 = test_pop_1.grid_ensemble_results

        # second
        test_pop_2 = Population(tmp_dir=TMP_DIR)
        test_pop_2.set(
            num_cores=num_cores_value,
            verbosity=TEST_VERBOSITY,
            M_2=1,
            orbital_period=100000,
            ensemble=1,
            ensemble_defer=1,
            ensemble_filters_off=1,
            ensemble_filter_STELLAR_TYPE_COUNTS=1,
            ensemble_dt=1000,
        )
        test_pop_2.set(
            data_dir=TMP_DIR,
            combine_ensemble_with_thread_joining=False,
        )

        resolution = {"M_1": 10}

        test_pop_2.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="self.const_linear(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        analytics_2 = test_pop_2.evolve()
        output_names_2 = [
            os.path.join(
                data_dir_value,
                "ensemble_output_{}_{}.json".format(
                    analytics_2["population_id"], thread_id
                ),
            )
            for thread_id in range(num_cores_value)
        ]
        ensemble_output_2 = {}

        for output_name in output_names_2:
            self.assertTrue(os.path.isfile(output_name))

            with open(output_name, "r") as f:
                file_content = f.read()

                ensemble_json = json.loads(file_content)

                ensemble_output_2 = merge_dicts(ensemble_output_2, ensemble_json)

        for key in ensemble_output_1["ensemble"]["number_counts"]["stellar_type"]["0"]:
            self.assertIn(key, ensemble_output_2["number_counts"]["stellar_type"]["0"])

            # compare values
            self.assertLess(
                np.abs(
                    ensemble_output_1["ensemble"]["number_counts"]["stellar_type"]["0"][
                        key
                    ]
                    - ensemble_output_2["number_counts"]["stellar_type"]["0"][key]
                ),
                1e-8,
            )


if __name__ == "__main__":
    unittest.main()

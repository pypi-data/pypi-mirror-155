"""
Unit tests for the ensemble module
"""

import os
import sys
import json
import unittest

import io
from io import StringIO

from binarycpython.utils.functions import (
    temp_dir,
    Capturing,
)
from binarycpython.utils.ensemble import (
    binaryc_json_serializer,
    handle_ensemble_string_to_json,
    BinarycEncoder,
    BinarycDecoder,
    extract_ensemble_json_from_string,
    load_ensemble,
    ensemble_file_type,
    open_ensemble,
)
from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test_ensemble")
TEST_VERBOSITY = 1


class test_binaryc_json_serializer(unittest.TestCase):
    """
    Unittests for function binaryc_json_serializer
    """

    def test_not_function(self):
        with Capturing() as output:
            self._test_not_function()

    def _test_not_function(self):
        """
        Test passing an object that doesnt get turned in to a string
        """

        stringo = "hello"
        output = binaryc_json_serializer(stringo)
        self.assertTrue(stringo == output)

    def test_function(self):
        with Capturing() as output:
            self._test_function()

    def _test_function(self):
        """
        Test passing an object that gets turned in to a string: a function
        """

        string_of_function = str(os.path.isfile)
        output = binaryc_json_serializer(os.path.isfile)
        self.assertTrue(string_of_function == output)


class test_handle_ensemble_string_to_json(unittest.TestCase):
    """
    Unittests for function handle_ensemble_string_to_json
    """

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        Test passing string representation of a dictionary.
        """

        _ = str(os.path.isfile)
        input_string = '{"ding": 10, "list_example": [1,2,3]}'
        output_dict = handle_ensemble_string_to_json(input_string)

        self.assertTrue(isinstance(output_dict, dict))
        self.assertTrue(output_dict["ding"] == 10)
        self.assertTrue(output_dict["list_example"] == [1, 2, 3])


class test_BinarycEncoder(unittest.TestCase):
    """
    Unittests for class BinarycEncoder
    """

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        Test that the object is converted to strings
        """

        input_1 = {"a": BinarycEncoder}
        output_1 = json.dumps(input_1, cls=BinarycEncoder)
        self.assertTrue(isinstance(output_1, str))

        dict_output_1 = json.loads(output_1)
        self.assertTrue(isinstance(dict_output_1["a"], str))


class test_BinarycDecoder(unittest.TestCase):
    """
    Unittests for class BinarycDecoder
    """

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        Test that the object is converted to floats
        """

        input_1 = '{"a": "10.0"}'
        output_1 = json.loads(input_1)
        output_2 = json.loads(input_1, cls=BinarycDecoder)

        self.assertTrue(isinstance(output_1["a"], str))
        self.assertTrue(isinstance(output_2["a"], float))


class test_extract_ensemble_json_from_string(unittest.TestCase):
    """
    Unittests for class extract_ensemble_json_from_string
    """

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        Simple test without errors
        """

        input_1 = 'ENSEMBLE_JSON {"a": 10}'
        output_1 = extract_ensemble_json_from_string(input_1)

        self.assertTrue(isinstance(output_1, dict))
        self.assertEqual(output_1, {"a": 10})

    def test_2(self):
        with Capturing() as _:
            self._test_2()

    def _test_2(self):
        """
        Simple test with 2 lines
        """

        input_1 = 'ENSEMBLE_JSON {"a": 10}\nENSEMBLE_JSON {"b": 20}'

        capturedOutput = StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  #  and redirect stdout.
        _ = extract_ensemble_json_from_string(input_1)
        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertTrue(capturedOutput.getvalue().startswith("Warning:"))

    def test_3(self):
        with Capturing() as _:
            self._test_3()

    def _test_3(self):
        """
        Simple test with empty input
        """

        input_1 = ""
        output_1 = extract_ensemble_json_from_string(input_1)

        self.assertTrue(isinstance(output_1, dict))
        self.assertEqual(output_1, {})

    def test_4(self):
        with Capturing() as _:
            self._test_4()

    def test_4(self):
        """
        Simple test with missing starting string
        """

        input_1 = ' {"a": 10}'

        #
        capturedOutput = StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  #  and redirect stdout.
        _ = extract_ensemble_json_from_string(input_1)
        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertTrue(capturedOutput.getvalue().startswith("Error:"))


class test_load_ensemble(unittest.TestCase):
    """
    Unittests for class extract_ensemble_json_from_string
    """

    def __init__(self, *args, **kwargs):
        """
        init function
        """
        super(test_load_ensemble, self).__init__(*args, **kwargs)

        #
        self.run_population()

    def run_population(self):
        with Capturing() as _:
            self._run_population()

    def _run_population(self):
        """
        Function to run the population to create the ensemble files
        """

        # First
        test_pop_1 = Population()
        test_pop_1.set(
            num_cores=2,
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

        _ = test_pop_1.evolve()
        ensemble_output_1 = test_pop_1.grid_ensemble_results

        self.normal_ensemble_output_name = os.path.join(
            TMP_DIR, "test_load_ensemble_ensemble_output.json"
        )
        self.bzip2_ensemble_output_name = os.path.join(
            TMP_DIR, "test_load_ensemble_ensemble_output.json.bz2"
        )
        self.no_extension_ensemble_output_name = os.path.join(
            TMP_DIR, "test_load_ensemble_ensemble_output"
        )

        # Write ensemble to json with normal write
        test_pop_1.write_ensemble(self.normal_ensemble_output_name)

        # Write ensemble to bzip
        test_pop_1.write_ensemble(self.bzip2_ensemble_output_name)

        # Write ensemble without extension
        with open(self.no_extension_ensemble_output_name, "w") as f:
            f.write(json.dumps(ensemble_output_1))

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        Simple test to load ensemble with normal filetype
        """

        # load data
        loaded_data_1 = load_ensemble(self.normal_ensemble_output_name)

        self.assertTrue(isinstance(loaded_data_1, dict))

    def test_2(self):
        with Capturing() as _:
            self._test_2()

    def _test_2(self):
        """
        Simple test to load ensemble with msgpack type
        """

        # load data
        loaded_data_1 = load_ensemble(self.bzip2_ensemble_output_name)

        self.assertTrue(isinstance(loaded_data_1, dict))

    def test_3(self):
        with Capturing() as _:
            self._test_3()

    def _test_3(self):
        """
        Simple test to load ensemble with timing output
        """

        #
        capturedOutput = StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  #  and redirect stdout.
        _ = load_ensemble(self.normal_ensemble_output_name, timing=True)
        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertTrue("Took" in capturedOutput.getvalue())

    def test_4(self):
        with Capturing() as _:
            self._test_4()

    def _test_4(self):
        """
        Simple test to load ensemble conveting to floats and timing
        """

        #
        capturedOutput = StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  #  and redirect stdout.
        loaded_data_1 = load_ensemble(
            self.normal_ensemble_output_name, timing=True, convert_float_keys=True
        )
        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertTrue("Took" in capturedOutput.getvalue())


class test_ensemble_file_type(unittest.TestCase):
    """
    Unittests for class ensemble_file_type
    """

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        filetype tests
        """

        # Json test
        input_1 = "/tmp/test.json"
        output_1 = ensemble_file_type(input_1)

        self.assertEqual(output_1, "JSON")

        # Msgpack
        input_2 = "/tmp/test.msgpack"
        output_2 = ensemble_file_type(input_2)

        self.assertEqual(output_2, "msgpack")

        # None
        input_3 = "/tmp/test"
        output_3 = ensemble_file_type(input_3)

        self.assertIsNone(output_3)


class test_open_ensemble(unittest.TestCase):
    """
    Unittests for class open_ensemble:
    """

    def __init__(self, *args, **kwargs):
        """
        init function
        """
        super(test_open_ensemble, self).__init__(*args, **kwargs)

        #
        self.run_population()

    def run_population(self):
        with Capturing() as _:
            self._run_population()

    def _run_population(self):
        """
        Function to run the population to create the ensemble files
        """

        # First
        test_pop_1 = Population()
        test_pop_1.set(
            num_cores=2,
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

        _ = test_pop_1.evolve()
        ensemble_output_1 = test_pop_1.grid_ensemble_results

        self.normal_ensemble_output_name = os.path.join(
            TMP_DIR, "test_open_ensemble_ensemble_output.json"
        )
        self.bzip2_ensemble_output_name = os.path.join(
            TMP_DIR, "test_open_ensemble_ensemble_output.json.bz2"
        )
        self.gzip_ensemble_output_name = os.path.join(
            TMP_DIR, "test_open_ensemble_ensemble_output.json.gz"
        )
        # self.msgpack_ensemble_output_name = os.path.join(TMP_DIR, 'test_open_ensemble_ensemble_output.msgpack')

        # Write ensemble to json with normal write
        test_pop_1.write_ensemble(self.normal_ensemble_output_name)

        # Write ensemble to bzip
        test_pop_1.write_ensemble(self.bzip2_ensemble_output_name)

        # gzip
        test_pop_1.write_ensemble(self.gzip_ensemble_output_name)

        # # Msgpack
        # test_pop_1.write_ensemble(self.msgpack_ensemble_output_name)

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        filetype tests
        """

        self.msgpack_ensemble_output_name = os.path.join(
            TMP_DIR, "test_open_ensemble_ensemble_output.msgpack.gz"
        )

        #
        handle_1 = open_ensemble(self.normal_ensemble_output_name)
        self.assertTrue(isinstance(handle_1, io._io.TextIOWrapper))
        handle_1.close()

        #
        handle_2 = open_ensemble(self.bzip2_ensemble_output_name)
        self.assertTrue(isinstance(handle_2, io._io.TextIOWrapper))
        handle_2.close()

        #
        handle_3 = open_ensemble(self.gzip_ensemble_output_name)
        self.assertTrue(isinstance(handle_3, io._io.TextIOWrapper))
        handle_3.close()

        # # TODO: implement this again
        # handle_4 = open_ensemble(self.msgpack_ensemble_output_name)
        # self.assertTrue(isinstance(handle_4, io._io.TextIOWrapper))
        # handle_4.close()


if __name__ == "__main__":
    unittest.main()

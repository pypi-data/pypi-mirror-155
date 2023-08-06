"""
Unittests for the custom_logging module
"""

import unittest

from binarycpython.utils.custom_logging_functions import *
from binarycpython.utils.functions import Capturing

TMP_DIR = temp_dir("tests", "test_custom_logging")


class test_autogen_C_logging_code(unittest.TestCase):
    """
    Unit test class for autogen_C_logging_code
    """

    def test_autogen_C_logging_code(self):
        with Capturing() as output:
            self._test_autogen_C_logging_code()
        # print("\n".join(output))

    def _test_autogen_C_logging_code(self):
        """
        Tests for the autogeneration of a print statement from a dictionary. and then checking if the output is correct
        """

        input_dict_1 = None
        output_1 = autogen_C_logging_code(input_dict_1, verbosity=1)
        self.assertEqual(output_1, None, msg="Error. return value should be None")

        input_dict_2 = {
            "MY_STELLAR_DATA": [
                "model.time",
                "star[0].mass",
                "model.probability",
                "model.dt",
            ]
        }
        output_2 = autogen_C_logging_code(input_dict_2, verbosity=1)

        test_output_2 = 'Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));'
        self.assertEqual(
            output_2, test_output_2, msg="Output doesnt match the test_output_2"
        )

        input_dict_3 = {"MY_STELLAR_DATA": 2}
        output_3 = autogen_C_logging_code(input_dict_3, verbosity=1)
        self.assertEqual(output_3, None, msg="Output should be None")


class test_binary_c_log_code(unittest.TestCase):
    """
    Unit test for binary_c_log_code
    """

    def test_binary_c_log_code(self):
        with Capturing() as output:
            self._test_binary_c_log_code()
        # print("\n".join(output))

    def _test_binary_c_log_code(self):
        """
        Test to see if passing a print statement to the function results in correct binary_c output
        """

        input_1 = "None"
        output_1 = binary_c_log_code(input_1, verbosity=1)
        self.assertEqual(output_1, None, msg="Output should be None")

        input_2 = 'Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));'
        output_2 = binary_c_log_code(input_2, verbosity=1)
        test_value_2 = '#pragma push_macro("Max")\n#pragma push_macro("Min")\n#undef Max\n#undef Min\n#include "binary_c.h"\n\n// add visibility __attribute__ ((visibility ("default"))) to it \nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata);\nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata)\n{\n    // struct stardata_t * stardata = (struct stardata_t *)x;\n    Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));;\n}\n\n#undef Max \n#undef Min\n#pragma pop_macro("Min")\n#pragma pop_macro("Max")    '

        self.assertEqual(
            output_2,
            test_value_2,
            msg="Output does not match what it should be: {}".format(test_value_2),
        )


class test_binary_c_write_log_code(unittest.TestCase):
    """
    Unit test for binary_c_write_log_code
    """

    def test_binary_c_write_log_code(self):
        with Capturing() as output:
            self._test_binary_c_write_log_code()
        # print("\n".join(output))

    def _test_binary_c_write_log_code(self):
        """
        Tests to see if writing the code to a file and reading that out again is the same
        """

        input_1 = '#pragma push_macro("Max")\n#pragma push_macro("Min")\n#undef Max\n#undef Min\n#include "binary_c.h"\n\n// add visibility __attribute__ ((visibility ("default"))) to it \nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata);\nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata)\n{\n    // struct stardata_t * stardata = (struct stardata_t *)x;\n    Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));;\n}\n\n#undef Max \n#undef Min\n#pragma pop_macro("Min")\n#pragma pop_macro("Max")    '

        binary_c_write_log_code(
            input_1,
            os.path.join(TMP_DIR, "test_binary_c_write_log_code.txt"),
            verbosity=1,
        )

        self.assertTrue(
            os.path.isfile(os.path.join(TMP_DIR, "test_binary_c_write_log_code.txt")),
            msg="File not created",
        )
        with open(os.path.join(TMP_DIR, "test_binary_c_write_log_code.txt")) as f:
            content_file = repr(f.read())
        self.assertEqual(repr(input_1), content_file, msg="Contents are not similar")


class test_from_binary_c_config(unittest.TestCase):
    """
    Unit test for from_binary_c_config
    """

    def test_from_binary_c_config(self):
        with Capturing() as output:
            self._test_from_binary_c_config()
        # print("\n".join(output))

    def _test_from_binary_c_config(self):
        """
        Tests for interfacing with binary_c-config
        """

        # not going to test everything here, just the version and any output at all

        BINARY_C_DIR = os.getenv("BINARY_C")
        if BINARY_C_DIR:
            BINARY_C_CONFIG = os.path.join(BINARY_C_DIR, "binary_c-config")

        self.assertTrue(
            os.path.isfile(BINARY_C_CONFIG),
            msg="{} doesn't exist".format(BINARY_C_CONFIG),
        )

        input_1 = "aa"
        output_1 = from_binary_c_config(BINARY_C_CONFIG, input_1)
        self.assertTrue(output_1.startswith("Usage"))

        input_2 = "version"
        output_2 = from_binary_c_config(BINARY_C_CONFIG, input_2)
        self.assertIn(
            output_2,
            ["2.1.7", "2.2pre1", "2.2.0", "2.2.1"],
            msg="binary_c version doesnt match",
        )


class test_return_compilation_dict(unittest.TestCase):
    """
    Unit test for return_compilation_dict
    """

    def test_return_compilation_dict(self):
        with Capturing() as output:
            self._test_return_compilation_dict()
        # print("\n".join(output))

    def _test_return_compilation_dict(self):
        """
        Tests to see if the compilation dictionary contains the correct keys
        """

        # Just going to check whether the dictionary has the components it needs
        # TODO: check whether we need to make this better

        output = return_compilation_dict(verbosity=1)

        self.assertTrue("cc" in output)
        self.assertTrue("ld" in output)
        self.assertTrue("ccflags" in output)
        self.assertTrue("libs" in output)
        self.assertTrue("inc" in output)


class test_create_and_load_logging_function(unittest.TestCase):
    """
    Unit test for return_compilation_dict
    """

    def test_create_and_load_logging_function(self):
        with Capturing() as output:
            self._test_create_and_load_logging_function()
        # print("\n".join(output))

    def _test_create_and_load_logging_function(self):
        """
        Tests checking the output of create_and_load_logging_function. Should return a valid memory int and a correct filename
        """

        #
        input_1 = '#pragma push_macro("MAX")\n#pragma push_macro("MIN")\n#undef MAX\n#undef MIN\n#include "binary_c.h"\n\n// add visibility __attribute__ ((visibility ("default"))) to it \nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata);\nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata)\n{\n    // struct stardata_t * stardata = (struct stardata_t *)x;\n    Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));;\n}\n\n#undef MAX \n#undef MIN\n#pragma pop_macro("MIN")\n#pragma pop_macro("MAX")    '
        output_1 = create_and_load_logging_function(input_1, verbosity=1)

        self.assertTrue(isinstance(output_1[0], int), msg="memaddr is not an int")
        self.assertTrue(output_1[0] > 0, msg="memaddr is an int but not set correctly")
        self.assertTrue(
            "libcustom_logging" in output_1[1],
            msg="Name of the libcustom_logging not correct",
        )


if __name__ == "__main__":
    unittest.main()

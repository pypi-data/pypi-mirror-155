"""
Unit tests for the _version_info Population extension module

TODO: minimum_stellar_mass
"""

import os
import unittest

from binarycpython.utils.functions import (
    temp_dir,
    Capturing,
)
from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test__version_info")


class test_return_binary_c_version_info(unittest.TestCase):
    """
    Unittests for return_binary_c_version_info
    """

    def __init__(self, *args, **kwargs):
        """
        init
        """
        super(test_return_binary_c_version_info, self).__init__(*args, **kwargs)
        self._version_info_pop = Population()

    def test_return_binary_c_version_info(self):
        with Capturing() as output:
            self._test_return_binary_c_version_info()

    def _test_return_binary_c_version_info(self):
        """
        Unittests for the function return_binary_c_version_info
        """

        test_pop = Population()
        binary_c_version_info = test_pop.return_binary_c_version_info(parsed=True)

        self.assertTrue(isinstance(binary_c_version_info, dict))
        self.assertIn("isotopes", binary_c_version_info)
        self.assertIn("argpairs", binary_c_version_info)
        self.assertIn("ensembles", binary_c_version_info)
        self.assertIn("macros", binary_c_version_info)
        self.assertIn("dt_limits", binary_c_version_info)
        self.assertIn("nucleosynthesis_sources", binary_c_version_info)
        self.assertIn("miscellaneous", binary_c_version_info)

        self.assertIsNotNone(binary_c_version_info["argpairs"])
        self.assertIsNotNone(binary_c_version_info["ensembles"])
        self.assertIsNotNone(binary_c_version_info["macros"])
        self.assertIsNotNone(binary_c_version_info["dt_limits"])
        self.assertIsNotNone(binary_c_version_info["miscellaneous"])

        if binary_c_version_info["macros"]["NUCSYN"] == "on":
            self.assertIsNotNone(binary_c_version_info["isotopes"])

            if binary_c_version_info["macros"]["NUCSYN_ID_SOURCES"] == "on":
                self.assertIsNotNone(binary_c_version_info["nucleosynthesis_sources"])

    def test_not_parsed(self):
        with Capturing() as output:
            self._test_not_parsed()

    def _test_not_parsed(self):
        """
        Test for the raw version_info output
        """

        version_info = self._version_info_pop.return_binary_c_version_info(parsed=False)

        self.assertTrue(isinstance(version_info, str))
        self.assertIn("Build", version_info)
        self.assertIn("REIMERS_ETA_DEFAULT", version_info)
        self.assertIn("SIGMA_THOMPSON", version_info)

    def test_parsed(self):
        with Capturing() as output:
            self._test_parsed()

    def _test_parsed(self):
        """
        Test for the parssed version_info
        """

        # also tests the parse_version_info indirectly
        version_info_parsed = self._version_info_pop.return_binary_c_version_info(
            parsed=True
        )

        self.assertTrue(isinstance(version_info_parsed, dict))
        self.assertIn("isotopes", version_info_parsed.keys())
        self.assertIn("argpairs", version_info_parsed.keys())
        self.assertIn("ensembles", version_info_parsed.keys())
        self.assertIn("macros", version_info_parsed.keys())
        self.assertIn("elements", version_info_parsed.keys())
        self.assertIn("dt_limits", version_info_parsed.keys())
        self.assertIn("nucleosynthesis_sources", version_info_parsed.keys())
        self.assertIn("miscellaneous", version_info_parsed.keys())

    def test_envvar(self):
        with Capturing() as output:
            self._test_envvar()

    def _test_envvar(self):
        """
        Test for the parsed version info with a value already present
        """

        os.environ["BINARY_C_MACRO_HEADER"] = "macroxyz"

        # also tests the parse_version_info indirectly
        version_info_parsed = self._version_info_pop.return_binary_c_version_info(
            parsed=True
        )

        self.assertTrue(isinstance(version_info_parsed, dict))
        self.assertIn("isotopes", version_info_parsed.keys())
        self.assertIn("argpairs", version_info_parsed.keys())
        self.assertIn("ensembles", version_info_parsed.keys())
        self.assertIn("macros", version_info_parsed.keys())
        self.assertIn("elements", version_info_parsed.keys())
        self.assertIn("dt_limits", version_info_parsed.keys())
        self.assertIn("nucleosynthesis_sources", version_info_parsed.keys())
        self.assertIn("miscellaneous", version_info_parsed.keys())


class test_parse_binary_c_version_info(unittest.TestCase):
    """
    Unittests for function parse_binary_c_version_info
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        Test for the parsed versio info, more detailed
        """

        _version_info_pop = Population()

        #
        info = _version_info_pop.return_binary_c_version_info(parsed=False)
        parsed_info = _version_info_pop.parse_binary_c_version_info(info)

        self.assertIn("isotopes", parsed_info.keys())
        self.assertIn("argpairs", parsed_info.keys())
        self.assertIn("ensembles", parsed_info.keys())
        self.assertIn("macros", parsed_info.keys())
        self.assertIn("elements", parsed_info.keys())
        self.assertIn("dt_limits", parsed_info.keys())
        self.assertIn("nucleosynthesis_sources", parsed_info.keys())
        self.assertIn("miscellaneous", parsed_info.keys())

        self.assertIsNotNone(parsed_info["argpairs"])
        self.assertIsNotNone(parsed_info["ensembles"])
        self.assertIsNotNone(parsed_info["macros"])
        self.assertIsNotNone(parsed_info["dt_limits"])
        self.assertIsNotNone(parsed_info["miscellaneous"])

        if parsed_info["macros"]["NUCSYN"] == "on":
            self.assertIsNotNone(parsed_info["isotopes"])

            if parsed_info["macros"]["NUCSYN_ID_SOURCES"] == "on":
                self.assertIsNotNone(parsed_info["nucleosynthesis_sources"])


if __name__ == "__main__":
    unittest.main()

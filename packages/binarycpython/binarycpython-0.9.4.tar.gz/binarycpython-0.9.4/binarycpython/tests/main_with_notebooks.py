# /usr/bin/env python
"""
Main file for the tests. This file imports all the combined_test functions from all files.
"""

import unittest

from binarycpython.tests.test_c_bindings import *
from binarycpython.tests.test_custom_logging import *
from binarycpython.tests.test_distributions import *
from binarycpython.tests.test_functions import *
from binarycpython.tests.test_grid import *
from binarycpython.tests.test_hpc_functions import *
from binarycpython.tests.test_plot_functions import *
from binarycpython.tests.test_run_system_wrapper import *
from binarycpython.tests.test_spacing_functions import *
from binarycpython.tests.test_useful_funcs import *
from binarycpython.tests.test_grid_options_defaults import *
from binarycpython.tests.test_stellar_types import *
from test_notebooks import *

if __name__ == "__main__":
    unittest.main()

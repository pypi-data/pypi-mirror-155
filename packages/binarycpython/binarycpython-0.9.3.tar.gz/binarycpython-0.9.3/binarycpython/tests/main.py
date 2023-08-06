# /usr/bin/env python
"""
Main file for the tests. This file imports all the unit test functions from all modules except for the notebooks and for the HPC functions
"""

# pylint: disable=W0611

import unittest

from binarycpython.tests.test_c_bindings import (
    test_run_system,
    test_return_store_memaddr,
    test_ensemble_functions,
)
from binarycpython.tests.test_custom_logging import (
    test_autogen_C_logging_code,
    test_binary_c_log_code,
    test_binary_c_write_log_code,
    test_from_binary_c_config,
    test_return_compilation_dict,
    test_create_and_load_logging_function,
)
from binarycpython.tests.test_dicts import (
    test_merge_dicts,
    test_setopts,
    test_AutoVivicationDict,
    test_inspect_dict,
    test_custom_sort_dict,
    test_filter_dict,
    test_filter_dict_through_values,
    test_prepare_dict,
    test_normalize_dict,
    test_multiply_values_dict,
    test_count_keys_recursive,
    test_keys_to_floats,
    test_recursive_change_key_to_float,
    test_recursive_change_key_to_string,
    test_multiply_float_values,
    test_subtract_dicts,
    test_update_dicts,
    test__nested_get,
)
from binarycpython.tests.test_ensemble import (
    test_binaryc_json_serializer,
    test_handle_ensemble_string_to_json,
    test_BinarycEncoder,
    test_BinarycDecoder,
    test_extract_ensemble_json_from_string,
    test_load_ensemble,
    test_ensemble_file_type,
    test_open_ensemble,
)
from binarycpython.tests.test_functions import (
    test_verbose_print,
    test_temp_dir,
    test_remove_file,
    test_create_hdf5,
    test_output_lines,
    test_example_parse_output,
    test_get_defaults,
    test_get_arg_keys,
    test_create_arg_string,
    test_get_help,
    test_get_help_all,
    test_get_help_super,
    test_make_build_text,
    test_write_binary_c_parameter_descriptions_to_rst_file,
    test_bin_data,
)
from binarycpython.tests.test_grid import (
    test__setup,
    test_set,
    test_cmdline,
    test__return_argline,
    test_return_population_settings,
    test_return_binary_c_defaults,
    test_return_all_info,
    test_export_all_info,
    test__cleanup_defaults,
    test__increment_probtot,
    test__increment_count,
    test__dict_from_line_source_file,
    test_evolve_single,
    test_grid_evolve,
    test_resultdict,
)
from binarycpython.tests.test_plot_functions import (
    test_color_by_index,
    test_plot_system,
)
from binarycpython.tests.test_run_system_wrapper import *

from binarycpython.tests.tests_population_extensions.test_distribution_functions import (
    test_flat,
    test_number,
    test_const_distribution,
    test_powerlaw,
    test_three_part_power_law,
    test_Kroupa2001,
    test_ktg93,
    test_imf_tinsley1980,
    test_imf_scalo1986,
    test_imf_scalo1998,
    test_imf_chabrier2003,
    test_duquennoy1991,
    test_gaussian,
    test_Arenou2010_binary_fraction,
    test_raghavan2010_binary_fraction,
    test_Izzard2012_period_distribution,
    test_flatsections,
    test_sana12,
)
from binarycpython.tests.tests_population_extensions.test_grid_options_defaults import (
    test_grid_options_help,
    test_grid_options_description_checker,
    test_write_grid_options_to_rst_file,
)

from binarycpython.tests.tests_population_extensions.test_version_info import (
    test_return_binary_c_version_info,
    test_parse_binary_c_version_info,
)
from binarycpython.tests.tests_population_extensions.test_gridcode import (
    test_add_grid_variable,
)

from binarycpython.tests.tests_population_extensions.test_HPC import (
    test_HPC_njobs,
    test_HPC_job,
    test_HPC_job_type,
    test_HPC_jobID,
    test_HPC_jobID_tuple,
    test_HPC_dirs,
    test_HPC_id_filename,
    test_HPC_check_requirements,
    test_HPC_set_status,
    test_HPC_get_status,
    test_HPC_job_task,
    test_HPC_dir,
    test_HPC_id_from_dir,
)
from binarycpython.tests.tests_population_extensions.test_condor import (
    test_condorID,
    test_condor_dirs,
    test_condor_check_requirements,
    test_set_condor_status,
    test_get_condor_status,
    test_condor_outfile,
    test_make_condor_dirs,
)
from binarycpython.tests.tests_population_extensions.test_slurm import (
    test_slurmID,
    test_slurm_dirs,
    test_slurm_check_requirements,
    test_set_slurm_status,
    test_get_slurm_status,
    test_slurm_outfile,
    test_make_slurm_dirs,
)

from binarycpython.tests.test_stellar_types import *
from binarycpython.tests.test_useful_funcs import (
    test_calc_period_from_sep,
    test_calc_sep_from_period,
    test_roche_lobe,
    test_ragb,
    test_rzams,
    test_zams_collission,
)


# from binarycpython.tests.test_spacing_functions import *
# from binarycpython.tests.test_grid_options_defaults import *
# from binarycpython.tests.test_hpc_functions import *


if __name__ == "__main__":
    unittest.main()

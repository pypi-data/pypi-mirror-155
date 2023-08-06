"""
Module that contains the default options for the population grid code along with the description for these options, in the form of dictionaries:
    - grid_options_defaults_dict: dictionary containing the default values for all the options
    - grid_options_descriptions: dictionary containing the description for these options.

There are several other functions in this module, mostly to generate help texts or documents:
    - grid_options_help: interactive function for the user to get descriptions for options
    - grid_options_description_checker: function that checks that checks which options have a description.
    - write_grid_options_to_rst_file: function to generate the .rst document for the docs

With this its also possible to automatically generate a document containing all the setting names + descriptions.

All the options starting with _ should not be changed by the user except when you really know what you're doing (which is probably hacking the code :P)

TODO: reconsider having this all as class methods. It seems unnecessary to have all these functions as class methods.
"""

# pylint: disable=E1101

import os
import shutil
import sys

from binarycpython.utils.custom_logging_functions import temp_dir
from binarycpython.utils.functions import (
    command_string_from_list,
    now,
)

_MOE2017_VERBOSITY_LEVEL = 5
_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL = 6
_MOE2017_VERBOSITY_INTERPOLATOR_EXTRA_LEVEL = 7

secs_per_day = 86400  # probably needs to go somewhere more sensible


class grid_options_defaults:
    """
    Class extension to Population grid containing all the functionality for the options and defaults
    """

    def __init__(self, **kwargs):
        """
        Init function for the grid_options_defaults class
        """

        return

    def get_grid_options_defaults_dict(self):
        """
        Function to return the default values for the grid options
        """

        # Options dict
        return {
            ##########################
            # general (or unordered..)
            ##########################
            "num_cores": 1,  # total number of cores used to evolve the population
            "num_cores_available": None,  # set automatically, not by the user
            "parse_function": None,  # Function to parse the output with.
            "multiplicity_fraction_function": 0,  # Which multiplicity fraction function to use. 0: None, 1: Arenou 2010, 2: Rhagavan 2010, 3: Moe and di Stefano 2017
            "tmp_dir": temp_dir(),  # Setting the temp dir of the program
            "cache_dir": self.default_cache_dir(),  # Cache location, usually $HOME/.cache
            "status_dir": None,  #
            "_main_pid": -1,  # Placeholder for the main process id of the run.
            "save_ensemble_chunks": True,  # Force the ensemble chunk to be saved even if we are joining a thread (just in case the joining fails)
            "combine_ensemble_with_thread_joining": True,  # Flag on whether to combine everything and return it to the user or if false: write it to data_dir/ensemble_output_{population_id}_{thread_id}.json
            "_commandline_input": "",
            "log_runtime_systems": 0,  # whether to log the runtime of the systems (1 file per thread. stored in the tmp_dir)
            "_actually_evolve_system": True,  # Whether to actually evolve the systems of just act as if. for testing. used in _process_run_population_grid
            "max_queue_size": 0,  # Maximum size of the system call queue. Set to 0 for this to be calculated automatically
            "run_zero_probability_system": True,  # Whether to run the zero probability systems
            "_zero_prob_stars_skipped": 0,
            "ensemble_factor_in_probability_weighted_mass": False,  # Whether to multiply the ensemble results by 1/probability_weighted_mass
            "do_dry_run": True,  # Whether to do a dry run to calculate the total probability for this run
            "dry_run_num_cores": 1,  # number of parallel processes for the dry run (outer loop)
            "dry_run_hook": None,  # Function hook for the dry run: this function is called, if not None, for every star in the dry run. Useful for checking initial distributions.
            "custom_generator": None,  # Place for the custom system generator
            "return_after_dry_run": False,  # Return immediately after a dry run?
            "exit_after_dry_run": False,  # Exit after dry run?
            "print_stack_on_exit": False,  # print the stack trace on exit calls?
            #####################
            # System information
            #####################
            "command_line": command_string_from_list(sys.argv),
            "original_command_line": os.getenv("BINARY_C_PYTHON_ORIGINAL_CMD_LINE"),
            "working_diretory": os.getcwd(),
            "original_working_diretory": os.getenv("BINARY_C_PYTHON_ORIGINAL_WD"),
            "start_time": now(),
            "original_submission_time": os.getenv(
                "BINARY_C_PYTHON_ORIGINAL_SUBMISSION_TIME"
            ),
            ##########################
            # Execution log:
            ##########################
            "verbosity": 0,  # Level of verbosity of the simulation
            "log_file": os.path.join(  # not used (yet?)
                temp_dir(), "binary_c_python.log"
            ),  # Set to None to not log to file. The directory will be created
            "log_dt": 5,  # time between vb=1 logging outputs
            "n_logging_stats": 50,  # number of logging stats used to calculate time remaining (etc.) default = 50
            "log_newline": "\n",  # newline character in logs ("\n" for newlines, "\x0d" for carriage return)
            ##########################
            # binary_c files
            ##########################
            "_binary_c_executable": os.path.join(os.environ["BINARY_C"], "binary_c"),
            "_binary_c_shared_library": os.path.join(
                os.environ["BINARY_C"], "src", "libbinary_c.so"
            ),
            "_binary_c_config_executable": os.path.join(
                os.environ["BINARY_C"], "binary_c-config"
            ),
            "_binary_c_dir": os.environ["BINARY_C"],
            ##########################
            # Moe and di Stefano (2017) internal settings
            ##########################
            "_loaded_Moe2017_data": False,  # Holds flag whether the Moe and di Stefano (2017) data is loaded into memory
            "_set_Moe2017_grid": False,  # Whether the Moe and di Stefano (2017) grid has been loaded
            "Moe2017_options": None,  # Holds the Moe and di Stefano (2017) options.
            "_Moe2017_JSON_data": None,  # Stores the data
            ##########################
            # Custom logging
            ##########################
            "C_auto_logging": None,  # Should contain a dictionary where the keys are they headers
            # and the values are lists of parameters that should be logged.
            # This will get parsed by autogen_C_logging_code in custom_logging_functions.py
            "C_logging_code": None,  # Should contain a string which holds the logging code.
            "custom_logging_func_memaddr": -1,  # Contains the custom_logging functions memory address
            "_custom_logging_shared_library_file": None,  # file containing the .so file
            ##########################
            # Store pre-loading:
            ##########################
            "_store_memaddr": -1,  # Contains the store object memory address, useful for pre loading.
            # defaults to -1 and isn't used if that's the default then.
            ##########################
            # Log args: logging of arguments
            ##########################
            "log_args": 0,  # unused
            "log_args_dir": "/tmp/",  # unused
            ##########################
            # Population evolution
            ##########################
            ## General
            "evolution_type": "grid",  # Flag for type of population evolution
            "_evolution_type_options": [
                "grid",
                "custom_generator",
            ],  # available choices for type of population evolution. # TODO: fill later with Monte Carlo, source file
            "_system_generator": None,  # value that holds the function that generates the system
            # (result of building the grid script)
            "source_file_filename": None,  # filename for the source
            "_count": 0,  # count of systems
            "_total_starcount": 0,  # Total count of systems in this generator
            "_probtot": 0,  # total probability
            "weight": 1.0,  # weighting for the probability
            "repeat": 1,  # number of times to repeat each system (probability is adjusted to be 1/repeat)
            "_start_time_evolution": 0,  # Start time of the grid
            "_end_time_evolution": 0,  # end time of the grid
            "_errors_found": False,  # Flag whether there are any errors from binary_c
            "_errors_exceeded": False,  # Flag whether the number of errors have exceeded the limit
            "_failed_count": 0,  # number of failed systems
            "_failed_prob": 0,  # Summed probability of failed systems
            "failed_systems_threshold": 20,  # Maximum failed systems per process allowed to fail before the process stops logging the failing systems.
            "_failed_systems_error_codes": [],  # List to store the unique error codes
            "_population_id": 0,  # Random id of this grid/population run, Unique code for the population. Should be set only once by the controller process.
            "_total_mass_run": 0,  # To count the total mass that thread/process has ran
            "_total_probability_weighted_mass_run": 0,  # To count the total mass * probability for each system that thread/process has ran
            "modulo": 1,  # run modulo n of the grid.
            "start_at": 0,  # start at the first model
            "skip_before" : 0, # skip models before this
            ## Grid type evolution
            "_grid_variables": {},  # grid variables
            "gridcode_filename": None,  # filename of gridcode
            "symlink_latest_gridcode": True,  # symlink to latest gridcode
            "save_population_object": None,  # filename to which we should save a pickled grid object as the final thing we do
            "joinlist": None,
            "do_analytics": True,  # if True, calculate analytics prior to return
            "save_snapshots": True,  # if True, save snapshots on SIGINT
            "restore_from_snapshot_file": None,  # file to restore from
            "restore_from_snapshot_dir": None,  # dir to restore from
            "exit_code": 0,  # return code
            "stop_queue": False,
            "_killed": False,
            "_queue_done": False,
            ## Monte carlo type evolution
            # TODO: make MC options
            ## Evolution from source file
            # TODO: make run from sourcefile options.
            ########################################
            # function caching options
            ########################################
            "function_cache": True,
            "function_cache_default_maxsize": 256,
            "function_cache_default_type": "NullCache",  # one of LRUCache, LFUCache, FIFOCache, MRUCache, RRCache, TTLCache, NullCache, NoCache
            "function_cache_TTL": 30,
            "function_cache_functions": {
                # key=function_name : value=(cache_size, cache_type, test_args (string))
                #
                # if cache_size is 0, use function_cache_default_maxsize
                # set above
                #
                # if cache_type is None, use function_cache_default_type
                # set above
                #
                # if n is None, no cache is set up
                "distribution_functions.powerlaw_constant": (0, "NoCache", "1,100,-2"),
                "distribution_functions.calculate_constants_three_part_powerlaw": (
                    16,
                    "FIFOCache",
                    "0.1,0.5,1,100,-1.3,-2.3,-2.3",
                ),
                "distribution_functions.gaussian_normalizing_const": (
                    16,
                    "FIFOCache",
                    "1.0,1.0,-10.0,+10.0",
                ),
                "spacing_functions.const_linear": (16, "FIFOCache", "1,10,9"),
                "spacing_functions.const_int": (0, None, "1,10,9"),
                "spacing_functions.const_ranges": (
                    16,
                    "FIFOCache",
                    "((0.1,0.65,10),(0.65,0.85,20),(0.85,10.0,10))",
                ),
                "spacing_functions.gaussian_zoom": (
                    16,
                    "FIFOCache",
                    "1.0,10.0,5.0,2.0,0.9,100",
                ),
            },
            ########################################
            # HPC variables
            ########################################
            "HPC_force_join": 0,  # if True, and the HPC variable ("slurm" or "condor") is 3, skip checking our own job and force the join
            "HPC_rebuild_joinlist": 0,  # if True, ignore the joinlist we would usually use and rebuild it automatically
            ########################################
            # Slurm stuff
            ########################################
            "slurm": 0,  # dont use the slurm by default, 0 = no slurm, 1 = launch slurm jobs, 2 = run slurm jobs
            "slurm_ntasks": 1,  # CPUs required per array job: usually only need this to be 1
            "slurm_dir": "",  # working directory containing scripts output logs etc.
            "slurm_njobs": 0,  # number of scripts; set to 0 as default
            "slurm_jobid": "",  # slurm job id (%A)
            "slurm_memory": "512MB",  # memory required for the job
            "slurm_warn_max_memory": "1024MB",  # warn if we set it to more than this (usually by accident)
            "slurm_postpone_join": 0,  # if 1 do not join on slurm, join elsewhere. want to do it off the slurm grid (e.g. with more RAM)
            "slurm_jobarrayindex": None,  # slurm job array index (%a)
            "slurm_jobname": "binary_c-python",  # default
            "slurm_partition": None,
            "slurm_time": '0',  # total time. 0 = infinite time
            "slurm_postpone_sbatch": 0,  # if 1: don't submit, just make the script
            "slurm_array": None,  # override for --array, useful for rerunning jobs
            "slurm_array_max_jobs": None,  # override for the max number of concurrent array jobs
            "slurm_extra_settings": {},  # Dictionary of extra settings for Slurm to put in its launch script.
            "slurm_sbatch": shutil.which("sbatch"),  # sbatch command
            "slurm_env": shutil.which("env"),  # env location for Slurm
            "slurm_bash": shutil.which("bash"),  # bash location for Slurm
            "slurm_pwd": shutil.which("pwd"),  # pwd command location for Slurm
            "slurm_date": shutil.which("date"),  # bash location for Slurm
            ########################################
            # Condor stuff
            ########################################
            "condor": 0,  # 1 to use condor, 0 otherwise
            "condor_dir": "",  # working directory containing e.g. scripts, output, logs (e.g. should be NFS available to all)
            "condor_njobs": 0,  # number of scripts/jobs that CONDOR will run in total
            "condor_ClusterID": None,  # condor cluster id, equivalent to Slurm's jobid
            "condor_Process": None,  # condor process, equivalent to Slurm's jobarrayindex
            "condor_postpone_submit": 0,  # if 1, the condor script is not submitted (useful for debugging). Default 0.
            "condor_postpone_join": 0,  # if 1, data is not joined, e.g. if you want to do it off the condor grid (e.g. with more RAM). Default 0.
            "condor_memory": 512,  # in MB, the memory use (ImageSize) of the job
            "condor_warn_max_memory": 1024,  # in MB, the memory use (ImageSize) of the job
            "condor_universe": "vanilla",  # usually vanilla universe
            "condor_extra_settings": {},  # Place to put extra configuration for the CONDOR submit file. The key and value of the dict will become the key and value of the line in te slurm batch file. Will be put in after all the other settings (and before the command). Take care not to overwrite something without really meaning to do so.
            # snapshots and checkpoints
            "condor_snapshot_on_kill": 0,  # if 1 snapshot on SIGKILL before exit
            "condor_stream_output": True,  # stream stdout
            "condor_stream_error": True,  # stream stderr
            "condor_should_transfer_files": "YES",
            "condor_when_to_transfer_output": "ON_EXIT_OR_EVICT",
            # (useful for debugging, otherwise a lot of work)
            "condor_requirements": "",  # job requirements
            "condor_env": shutil.which("env"),  # /usr/bin/env location
            "condor_bash": shutil.which("bash"),  # bash executable location
            "condor_pwd": shutil.which("pwd"),  # pwd command location for Condor
            "condor_date": shutil.which("date"),  # bash location for Condor
            "condor_initial_dir": None,  # directory from which condor is run, if None is the directory in which your script is run
            "condor_submit": shutil.which("condor_submit"),  # the condor_submit command
            "condor_q": shutil.which("condor_q"),  # the condor_submit command
            "condor_getenv": True,  # if True condor takes the environment at submission and copies it to the jobs. You almost certainly want this.
            "condor_batchname": "binary_c-condor",  # Condor batchname option
            "condor_kill_sig": "SIGINT",  # signal Condor should use to stop a process : note that grid.py expects this to be "SIGINT"
            # ########################################
            # # GRID
            # ########################################
            # control flow
            "rungrid": 1,  # usually run the grid, but can be 0 to skip it (e.g. for condor/slurm admin)
        }

    def get_grid_options_descriptions(self):
        """
        Function that returns the descriptions for all the grid options

        TODO: consider putting input types for all of them
        """

        # Grid containing the descriptions of the options
        return {
            "tmp_dir": "Directory where certain types of output are stored. The grid code is stored in that directory, as well as the custom logging libraries. Log files and other diagnostics will usually be written to this location, unless specified otherwise",  # TODO: improve this
            "status_dir": "Directory where grid status is stored",
            "_binary_c_dir": "Director where binary_c is stored. This options are not really used",
            "_binary_c_config_executable": "Full path of the binary_c-config executable. This options is not used in the population object.",
            "_binary_c_executable": "Full path to the binary_c executable. This options is not used in the population object.",
            "_binary_c_shared_library": "Full path to the libbinary_c file. This options is not used in the population object",
            "verbosity": "Verbosity of the population code. Default is 0, by which only errors will be printed. Higher values will show more output, which is good for debugging.",
            "log_dt": "Time between verbose logging output.",
            "log_newline": "Newline character used at the end of verbose logging statements. This is \\n (newline) by default, but \\x0d (carriage return) might also be what you want.",
            "n_logging_stats": "Number of logging statistics used to calculate time remaining (etc.). E.g., if you set this to 10 the previous 10 calls to the verbose log will be used to construct an estimate of the time remaining.",
            "num_cores": "The number of cores that the population grid will use. You can set this manually by entering an integer great than 0. When 0 uses all logical cores. When -1 uses all physical cores. Input: int",
            "num_processes": "Number of processes launched by multiprocessing. This should be set automatically by binary_c-python, not by the user.",
            "_start_time_evolution": "Variable storing the start timestamp of the population evolution. Set by the object itself.",
            "_end_time_evolution": "Variable storing the end timestamp of the population evolution. Set by the object itself",
            "_total_starcount": "Variable storing the total number of systems in the generator. Used and set by the population object.",
            "_custom_logging_shared_library_file": "filename for the custom_logging shared library. Used and set by the population object",
            "_errors_found": "Variable storing a Boolean flag whether errors by binary_c are encountered.",
            "_errors_exceeded": "Variable storing a Boolean flag whether the number of errors was higher than the set threshold (failed_systems_threshold). If True, then the command line arguments of the failing systems will not be stored in the failed_system_log files.",
            "source_file_filename": "Variable containing the source file containing lines of binary_c command line calls. These all have to start with binary_c.",  # TODO: Expand
            "C_auto_logging": "Dictionary containing parameters to be logged by binary_c. The structure of this dictionary is as follows: the key is used as the headline which the user can then catch. The value at that key is a list of binary_c system parameters (like star[0].mass)",
            "C_logging_code": "Variable to store the exact code that is used for the custom_logging. In this way the user can do more complex logging, as well as putting these logging strings in files.",
            "_failed_count": "Variable storing the number of failed systems.",
            "_evolution_type_options": "List containing the evolution type options.",
            "_failed_prob": "Variable storing the total probability of all the failed systems",
            "_failed_systems_error_codes": "List storing the unique error codes raised by binary_c of the failed systems",
            "_grid_variables": "Dictionary storing the grid_variables. These contain properties which are accessed by the _generate_grid_code function",
            "_population_id": "Variable storing a unique 32-char hex string.",
            "_commandline_input": "String containing the arguments passed to the population object via the command line. Set and used by the population object.",
            "_system_generator": "Function object that contains the system generator function. This can be from a grid, or a source file, or a Monte Carlo grid.",
            "gridcode_filename": "Filename for the grid code. Set and used by the population object. TODO: allow the user to provide their own function, rather than only a generated function.",
            "log_args": "Boolean to log the arguments.",
            "log_args_dir": "Directory to log the arguments to.",
            "log_file": "Log file for the population object. Unused",
            "custom_logging_func_memaddr": "Memory address where the custom_logging_function is stored. Input: int",
            "_count": "Counter tracking which system the generator is on.",
            "_probtot": "Total probability of the population.",
            "_main_pid": "Main process ID of the master process. Used and set by the population object.",
            "_store_memaddr": "Memory address of the store object for binary_c.",
            "failed_systems_threshold": "Variable storing the maximum number of systems that are allowed to fail before logging their command line arguments to failed_systems log files",
            "parse_function": "Function that the user can provide to handle the output the binary_c. This function has to take the arguments (self, output). Its best not to return anything in this function, and just store stuff in the self.grid_results dictionary, or just output results to a file",
            ############################################################
            # Condor
            "condor": "Integer flag used to control HTCondor (referred to as Condor here) jobs. Default is 0 which means no Condor. 1 means launch Condor jobs. Do not manually set this to 2 (run Condor jobs) or 3 (join Condor job data) unless you know what you are doing, this is usually done for you.",
            "condor_dir": "String. Working directory containing e.g. scripts, output, logs (e.g. should be NFS available to all jobs). This directory should not exist when you launch the Condor jobs.",
            "condor_njobs": "Integer. Number of jobs that Condor will run",
            "condor_ClusterID": "Integer. Condor ClusterID variable, equivalent to Slurm's jobid. Jobs are numbered <ClusterID>.<Process>",
            "condor_Process": "Integer. Condor Process variable, equivalent to Slurm's jobarrayindex. Jobs are numbered <ClusterID>.<Process>",
            "condor_postpone_submit": "Integer. Debugging tool. If 1, the condor script is not submitted (useful for debugging). Default 0.",
            "condor_postpone_join": "Integer. Use to delay the joining of Condor grid data. If 1, data is not joined, e.g. if you want to do it off the condor grid (e.g. with more RAM). Default 0.",
            "condor_memory": "Integer. In MB, the memory use (ImageSize) of the job.",
            "condor_warn_max_memory": "Integer. In MB, the memory use (ImageSize) of the job.",
            "condor_universe": 'String. The HTCondor "universe": this is "vanilla" by default.',
            "condor_extra_settings": "Dictionary. Place to put extra configuration for the CONDOR submit file. The key and value of the dict will become the key and value of the line in te slurm batch file. Will be put in after all the other settings (and before the command). Take care not to overwrite something without really meaning to do so.",
            "condor_snapshot_on_kill": "Integer. If 1 we save a snapshot on SIGKILL before exit.",
            "condor_stream_output": "Boolean. If True, we activate Condor's stdout stream. If False, this data is copied at the end of the job.",
            "condor_stream_error": "Boolean. If True, we activate Condor's stderr stream. If False, this data is copied at the end of the job.",
            "condor_should_transfer_files": 'Integer. Condor\'s option to transfer files at the end of the job. You should set this to "YES"',
            "condor_when_to_transfer_output": 'Integer. Condor\'s option to decide when output files are transferred. You should usually set this to "ON_EXIT_OR_EVICT"',
            "condor_requirements": "String. Condor job requirements. These are passed to Condor directly, you should read the HTCondor manual to learn about this. If no requirements exist, leave as an string.",
            "condor_env": 'String. Points the location of the "env" command, e.g. /usr/bin/env or /bin/env, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            "condor_bash": 'String. Points the location of the "bash" command, e.g. /bin/bash, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            "condor_pwd": 'String. Points the location of the "pwd" command, e.g. /bin/pwd, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            "condor_date": 'String. Points the location of the "date" command, e.g. /usr/bin/date, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            "condor_initial_dir": "String. Directory from which condor scripts are run. If set to the default, None, this is the directory from which your script is run.",
            "condor_submit": 'String. The Condor_submit command, usually "/usr/bin/condor_submit" but will depend on your HTCondor installation.',
            "condor_q": 'String. The Condor_q command, usually "/usr/bin/condor_q" but will depend on your HTCondor installation.',
            "condor_getenv": "Boolean. If True, the default, condor takes the environment at submission and copies it to the jobs. You almost certainly want this to be True.",
            "condor_batchname": 'String. Condor batchname option: this is what appears in condor_q. Defaults to "binary_c-condor"',
            "condor_kill_sig": 'String. Signal Condor should use to stop a process. Note that grid.py expects this to be "SIGINT" which is the default.',
            ############################################################
            # Slurm options
            ############################################################
            "slurm": "Integer flag used to control Slurm jobs. Default is 0 which means no Slurm. 1 means launch Slurm jobs. Do not manually set this to 2 (run Slurm jobs) or 3 (join Slurm job data) unless you know what you are doing, this is usually done for you.",
            "slurm_dir": "String. Working directory containing e.g. scripts, output, logs (e.g. should be NFS available to all jobs). This directory should not exist when you launch the Slurm jobs.",
            "slurm_ntasks": "Integer. Number of CPUs required per array job: usually only need this to be 1 (the default).",
            "slurm_njobs": "Integer. Number of Slurm jobs to be launched.",
            "slurm_jobid": "Integer. Slurm job id. Each job is numbered <slurm_jobid>.<slurm_jobarrayindex>.",
            "slurm_jobarrayindex": "Integer. Slurm job array index. Each job is numbered <slurm_jobid>.<slurm_jobarrayindex>.",
            "slurm_memory": 'String. Memory required for the job. Should be in megabytes in a format that Slurm understands, e.g. "512MB" (the default).',
            "slurm_warn_max_memory": 'String. If we set slurm_memory in excess of this, warn the user because this is usually a mistake. Default "1024MB".',
            "slurm_postpone_join": "Integer, default 0. If 1 do not join job results with Slurm, instead you have to do it later manually.",
            "slurm_jobname": 'String which names the Slurm jobs, default "binary_c-python".',
            "slurm_partition": "String containing the Slurm partition name. You should check your local Slurm installation to find out partition information, e.g. using the sview command.",
            "slurm_time": "String. The time a Slurm job is allowed to take. Default is 0 which means no limit. Please check the Slurm documentation for required format of this option.",
            "slurm_postpone_sbatch": "Integer, default 0. If set to 1, do not launch Slurm jobs with sbatch, just make the scripts that would have.",
            "slurm_array": "String. Override for Slurm's --array option, useful for rerunning jobs manually. Default None.",
            "slurm_array_max_jobs": "Integer. Override for the max number of concurrent Slurm array jobs. Default None.",
            "slurm_extra_settings": "Dictionary of extra settings for Slurm to put in its launch script. Please see the Slurm documentation for the many options that are available to you.",
            "slurm_sbatch": 'String. The Slurm "sbatch" submission command, usually "/usr/bin/sbatch" but will depend on your Slurm installation. By default is set automatically.',
            "slurm_env": 'String. Points the location of the "env" command, e.g. /usr/bin/env or /bin/env, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            "slurm_bash": 'String. Points the location of the "bash" command, e.g. /bin/bash, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            "slurm_pwd": 'String. Points the location of the "pwd" command, e.g. /bin/pwd, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            "slurm_date": 'String. Points the location of the "date" command, e.g. /usr/bin/date, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
            ############################################################
            # High power computing (HPC) variables
            ############################################################
            "HPC_force_join": 'Integer, default 0. If 1, and the HPC variable ("slurm" or "condor") is 3, skip checking our own job and force the join.',
            "HPC_rebuild_joinlist": "Integer, default 0. If 1, ignore the joinlist we would usually use and rebuild it automatically",
            ############################################################
            # Cacheing
            ############################################################
            "function_cache": "Boolean, default True. If True, we use a cache for certain function calls.",
            "function_cache_default_maxsize": "Integer, default 256. The default maxsize of the cache. Should be a power of 2.",
            "function_cache_default_type": "String. One of the following types: LRUCache, LFUCache, FIFOCache, MRUCache, RRCache, TTLCache, NullCache, NoCache. You can find details of what these mean in the Python cachetools manual, except fo NoCache which means no cache is used at all, and NullCache is a dummy cache that never matches, used for testing overheads.",
            "function_cache_functions.": "Dict. Keys are the function names that should be in the cache. The value is a tuple of (cache_size, cache_type, test_args) where cache_size used as the size of the cache, or if 0 the function_cache_default_maxsize is used. The cache_type is the function_cache_default_type if None, otherwise is the cache type (see the list defined at function_cache_default_type). The test_args are constant arguments used to call the function when testing the cache, see cache.cache_test() for details.",
            ############################################################
            "weight": "Weight factor for each system. The calculated probability is multiplied by this. If the user wants each system to be repeated several times, then this variable should not be changed, rather change the _repeat variable instead, as that handles the reduction in probability per system. This is useful for systems that have a process with some random element in it.",  # TODO: add more info here, regarding the evolution splitting.
            "repeat": "Factor of how many times a system should be repeated. Consider the evolution splitting binary_c argument for supernovae kick repeating.",
            "evolution_type": "Variable containing the type of evolution used of the grid. Multiprocessing, linear processing or possibly something else (e.g. for Slurm or Condor).",
            "combine_ensemble_with_thread_joining": "Boolean flag on whether to combine everything and return it to the user or if false: write it to data_dir/ensemble_output_{population_id}_{thread_id}.json",
            "log_runtime_systems": "Whether to log the runtime of the systems . Each systems run by the thread is logged to a file and is stored in the tmp_dir. (1 file per thread). Don't use this if you are planning to run a lot of systems. This is mostly for debugging and finding systems that take long to run. Integer, default = 0. if value is 1 then the systems are logged",
            "_total_mass_run": "To count the total mass that thread/process has ran",
            "_total_probability_weighted_mass_run": "To count the total mass * probability for each system that thread/process has ran",
            "_actually_evolve_system": "Whether to actually evolve the systems of just act as if. for testing. used in _process_run_population_grid",
            "max_queue_size": "Maximum size of the queue that is used to feed the processes. Don't make this too big! Default: 1000. Input: int",
            "_set_Moe2017_grid": "Internal flag whether the Moe and di Stefano (2017) grid has been loaded",
            "run_zero_probability_system": "Whether to run the zero probability systems. Default: True. Input: Boolean",
            "_zero_prob_stars_skipped": "Internal counter to track how many systems are skipped because they have 0 probability",
            "ensemble_factor_in_probability_weighted_mass": "Flag to multiply all the ensemble results with 1/probability_weighted_mass",
            "multiplicity_fraction_function": "Which multiplicity fraction function to use. 0: None, 1: Arenou 2010, 2: Rhagavan 2010, 3: Moe and di Stefano (2017) 2017",
            "m&s_options": "Internal variable that holds the Moe and di Stefano (2017) options. Don't write to this your self",
            "_loaded_Moe2017_data": "Internal variable storing whether the Moe and di Stefano (2017) data has been loaded into memory",
            "do_dry_run": "Whether to do a dry run to calculate the total probability for this run",
            "dry_run_hook": "Function hook to be called for every system in a dry run. The function is passed a dict of the system parameters. Does nothing if None (the default).",
            "return_after_dry_run": "If True, return immediately after a dry run (and don't run actual stars). Default is False.",
            "exit_after_dry_run": "If True, exits after a dry run. Default is False.",
            "print_stack_on_exit": "If True, prints a stack trace when the population's exit method is called.",
            "_Moe2017_JSON_data": "Location to store the loaded Moe&diStefano2017 dataset",  # Stores the data
        }

    #################################
    # Grid options functions

    # Utility functions
    def grid_options_help(self, option: str) -> dict:
        """
        Function that prints out the description of a grid option. Useful function for the user.

        Args:
            option: which option you want to have the description of

        returns:
            dict containing the option, the description if its there, otherwise empty string. And if the key doesnt exist, the dict is empty
        """

        #
        grid_options_defaults_dict = self.get_grid_options_defaults_dict()
        grid_options_descriptions = self.get_grid_options_descriptions()

        #
        option_keys = grid_options_defaults_dict.keys()
        description_keys = grid_options_descriptions.keys()

        # If the option is unknown
        if option not in option_keys:
            print(
                "Error: This is an invalid entry. Option does not exist, please choose from the following options:\n\t{}".format(
                    ", ".join(option_keys)
                )
            )
            return {}

        # If its not described
        if option not in description_keys:
            print(
                "This option has not been described properly yet. Please contact on of the authors"
            )
            return {option: ""}

        # If its known and described:
        print(grid_options_descriptions[option])
        return {option: grid_options_descriptions[option]}

    def grid_options_description_checker(self, print_info: bool = True) -> int:
        """
        Function that checks which descriptions are missing

        Args:
            print_info: whether to print out information about which options contain proper descriptions and which do not

        Returns:
            the number of undescribed keys
        """

        #
        grid_options_defaults_dict = self.get_grid_options_defaults_dict()
        grid_options_descriptions = self.get_grid_options_descriptions()

        #
        option_keys = grid_options_defaults_dict.keys()
        description_keys = grid_options_descriptions.keys()

        #
        undescribed_keys = list(set(option_keys) - set(description_keys))

        if undescribed_keys:
            if print_info:
                print(
                    "Warning: the following keys have no description yet:\n\t{}".format(
                        ", ".join(sorted(undescribed_keys))
                    )
                )
                print(
                    "Total description progress: {:.2f}%%".format(
                        100 * len(description_keys) / len(option_keys)
                    )
                )
        return len(undescribed_keys)

    def write_grid_options_to_rst_file(self, output_file: str) -> None:
        """
        Function that writes the descriptions of the grid options to an rst file

        Args:
            output_file: target file where the grid options descriptions are written to
        """

        # Get the options and the description
        options = self.get_grid_options_defaults_dict()
        descriptions = self.get_grid_options_descriptions()

        # Get those that do not have a description
        not_described_yet = list(set(options) - set(descriptions))

        # separate public and private options
        public_options = [key for key in options if not key.startswith("_")]
        private_options = [key for key in options if key.startswith("_")]

        # Check input
        if not output_file.endswith(".rst"):
            msg = "Filename doesn't end with .rst, please provide a proper filename"
            raise ValueError(msg)

        # M&S options
        moe_di_stefano_default_options = self.get_Moe_di_Stefano_2017_default_options()
        moe_di_stefano_default_options_description = (
            self.get_Moe_di_Stefano_2017_default_options_description()
        )

        with self.open(output_file, "w") as f:
            print("Population grid code options", file=f)
            print("{}".format("=" * len("Population grid code options")), file=f)
            print(
                "The following chapter contains all grid code options, along with their descriptions",
                file=f,
            )
            print(
                "There are {} options that are not described yet.".format(
                    len(not_described_yet)
                ),
                file=f,
            )
            print("\n", file=f)

            # Start public options part
            self.print_option_descriptions(
                f,
                public_options,
                descriptions,
                "Public options",
                "The following options are meant to be changed by the user.",
            )

            # Moe & di Stefano options:
            self.print_option_descriptions(
                f,
                moe_di_stefano_default_options,
                moe_di_stefano_default_options_description,
                "Moe & di Stefano sampler options",
                "The following options are meant to be changed by the user.",
            )

            # Start private options part
            self.print_option_descriptions(
                f,
                private_options,
                descriptions,
                "Private options",
                "The following options are not meant to be changed by the user, as these options are used and set internally by the object itself. The description still is provided, but just for documentation purposes.",
            )

    def print_option_descriptions(
        self, filehandle, options, descriptions, title, extra_text
    ):
        """
        Function to print the description of an option
        """

        # Start public options part
        print("{}".format(title), file=filehandle)
        print("{}".format("-" * len("{}".format(title))), file=filehandle)
        print("{}".format(extra_text), file=filehandle)
        print("\n", file=filehandle)

        for option in sorted(options):
            if option in descriptions:
                print(
                    "| **{}**: {}".format(
                        option, descriptions[option].replace("\n", "\n\t")
                    ),
                    file=filehandle,
                )
            else:
                print(
                    "| **{}**: No description available yet".format(option),
                    file=filehandle,
                )
            print("", file=filehandle)

    def default_cache_dir(self):
        """
        Return a default cache directory path, or None if we cannot find one.
        """
        error_string = "__*ERR*__"  # string that cannot be a path
        for path in [
            os.path.join(os.environ.get("HOME", error_string), ".cache", "binary_c"),
            os.path.join(os.environ.get("TMP", error_string), "cache"),
        ]:
            if not error_string in path and os.path.isdir(path):
                return path
        return None

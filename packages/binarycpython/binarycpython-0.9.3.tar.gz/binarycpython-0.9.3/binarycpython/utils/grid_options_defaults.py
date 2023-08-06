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
"""

import os

from binarycpython.utils.custom_logging_functions import temp_dir
from binarycpython.utils.functions import return_binary_c_version_info

_LOGGER_VERBOSITY_LEVEL = 1
_CUSTOM_LOGGING_VERBOSITY_LEVEL = 2
_MOE2017_VERBOSITY_LEVEL = 5
_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL = 6
_MOE2017_VERBOSITY_INTERPOLATOR_EXTRA_LEVEL = 7

# Options dict
grid_options_defaults_dict = {
    ##########################
    # general (or unordered..)
    ##########################
    "num_cores": 1,  # total number of cores used to evolve the population
    "parse_function": None,  # Function to parse the output with.
    "multiplicity_fraction_function": 0,  # Which multiplicity fraction function to use. 0: None, 1: Arenou 2010, 2: Rhagavan 2010, 3: Moe and di Stefano 2017
    "tmp_dir": temp_dir(),  # Setting the temp dir of the program
    "_main_pid": -1,  # Placeholder for the main process id of the run.
    "save_ensemble_chunks": True,  # Force the ensemble chunk to be saved even if we are joining a thread (just in case the joining fails)
    "combine_ensemble_with_thread_joining": True,  # Flag on whether to combine everything and return it to the user or if false: write it to data_dir/ensemble_output_{population_id}_{thread_id}.json
    "_commandline_input": "",
    "log_runtime_systems": 0,  # whether to log the runtime of the systems (1 file per thread. stored in the tmp_dir)
    "_actually_evolve_system": True,  # Whether to actually evolve the systems of just act as if. for testing. used in _process_run_population_grid
    "max_queue_size": 1000,  # Maximum size of the system call queue.
    "run_zero_probability_system": True,  # Whether to run the zero probability systems
    "_zero_prob_stars_skipped": 0,
    "ensemble_factor_in_probability_weighted_mass": False,  # Whether to multiply the ensemble results by 1/probability_weighted_mass
    "do_dry_run": True,  # Whether to do a dry run to calculate the total probability for this run
    "custom_generator": None,  # Place for the custom system generator
    "exit_after_dry_run": False,  # Exit after dry run?
    ##########################
    # Execution log:
    ##########################
    "verbosity": 0,  # Level of verbosity of the simulation
    "log_file": os.path.join(
        temp_dir(), "binary_c_python.log"
    ),  # Set to None to not log to file. The directory will be created
    "log_dt": 5,  # time between vb=1 logging outputs
    "n_logging_stats": 50,  # number of logging stats used to calculate time remaining (etc.) default = 50
    ##########################
    # binary_c files
    ##########################
    "_binary_c_executable": os.path.join(
        os.environ["BINARY_C"], "binary_c"
    ),  # TODO: make this more robust
    "_binary_c_shared_library": os.path.join(
        os.environ["BINARY_C"], "src", "libbinary_c.so"
    ),  # TODO: make this more robust
    "_binary_c_config_executable": os.path.join(
        os.environ["BINARY_C"], "binary_c-config"
    ),  # TODO: make this more robust
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
        "source_file",
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
    ## Grid type evolution
    "_grid_variables": {},  # grid variables
    "gridcode_filename": None,  # filename of gridcode
    "symlink latest gridcode": True,  # symlink to latest gridcode
    ## Monte carlo type evolution
    # TODO: make MC options
    ## Evolution from source file
    # TODO: make run from sourcefile options.
    ## Other no yet implemented parts for the population evolution part
    #     # start at this model number: handy during debugging
    #     # to skip large parts of the grid
    #     start_at => 0
    #     global_error_string => undef,
    #     monitor_files => [],
    #     nextlogtime   => 0,
    #     nthreads      => 1, # number of threads
    #     # start at model offset (0-based, so first model is zero)
    #     offset        => 0,
    #     resolution=>{
    #         shift   =>0,
    #         previous=>0,
    #         n       =>{} # per-variable resolution
    #     },
    #     thread_q      => undef,
    #     threads       => undef, # array of threads objects
    #     tstart        => [gettimeofday], # flexigrid start time
    #     __nvar        => 0, # number of grid variables
    #     _varstub      => undef,
    #     _lock         => undef,
    #     _evcode_pids  => [],
    # };
    ########################################
    # Slurm stuff
    ########################################
    "slurm": 0,  # dont use the slurm by default. 1 = use slurm
    # "slurm_ntasks": 1,  # CPUs required per array job: usually only need this
    # "slurm_command": "",  # Command that slurm runs (e.g. evolve or join_datafiles)
    # "slurm_dir": "",  # working directory containing scripts output logs etc.
    # "slurm_njobs": 0,  # number of scripts; set to 0 as default
    # "slurm_jobid": "",  # slurm job id (%A)
    # "slurm_memory": 512,  # in MB, the memory use of the job
    # "slurm_warn_max_memory": 1024,  # in MB : warn if mem req. > this
    # "slurm_use_all_node_CPUs": 0,  # 1 = use all of a node's CPUs. 0 = use a given number of CPUs
    # "slurm_postpone_join": 0,  # if 1 do not join on slurm, join elsewhere. want to do it off the slurm grid (e.g. with more RAM)
    # "slurm_jobarrayindex": "",  # slurm job array index (%a)
    # "slurm_jobname": "binary_grid",  # default
    # "slurm_partition": None,
    # "slurm_time": 0,  # total time. 0 = infinite time
    # "slurm_postpone_sbatch": 0,  # if 1: don't submit, just make the script
    # "slurm_array": None,  # override for --array, useful for rerunning jobs
    # "slurm_use_all_node_CPUs": 0,  # if given nodes, set to 1
    # # if given CPUs, set to 0
    # # you will want to use this if your Slurm SelectType is e.g. linear
    # # which means it allocates all the CPUs in a node to the job
    # "slurm_control_CPUs": 0,  # if so, leave this many for Pythons control (0)
    # "slurm_array": None,  # override for --array, useful for rerunning jobs
    # "slurm_partition": None,  # MUST be defined
    # "slurm_extra_settings": {},  # Place to put extra configuration for the SLURM batch file. The key and value of the dict will become the key and value of the line in te slurm batch file. Will be put in after all the other settings (and before the command). Take care not to overwrite something without really meaning to do so.
    ########################################
    # Condor stuff
    ########################################
    "condor": 0,  # 1 to use condor, 0 otherwise
    # "condor_command": "",  # condor command e.g. "evolve", "join"
    # "condor_dir": "",  # working directory containing e.g. scripts, output, logs (e.g. should be NFS available to all)
    # "condor_njobs": "",  # number of scripts/jobs that CONDOR will run in total
    # "condor_jobid": "",  # condor job id
    # "condor_postpone_join": 0,  # if 1, data is not joined, e.g. if you want to do it off the condor grid (e.g. with more RAM)
    # # "condor_join_machine": None, # if defined then this is the machine on which the join command should be launched (must be sshable and not postponed)
    # "condor_join_pwd": "",  # directory the join should be in (defaults to $ENV{PWD} if undef)
    # "condor_memory": 1024,  # in MB, the memory use (ImageSize) of the job
    # "condor_universe": "vanilla",  # usually vanilla universe
    # "condor_extra_settings": {},  # Place to put extra configuration for the CONDOR submit file. The key and value of the dict will become the key and value of the line in te slurm batch file. Will be put in after all the other settings (and before the command). Take care not to overwrite something without really meaning to do so.
    # snapshots and checkpoints
    # condor_snapshot_on_kill=>0, # if 1 snapshot on SIGKILL before exit
    # condor_load_from_snapshot=>0, # if 1 check for snapshot .sv file and load it if found
    # condor_checkpoint_interval=>0, # checkpoint interval (seconds)
    # condor_checkpoint_stamp_times=>0, # if 1 then files are given timestamped names
    # (warning: lots of files!), otherwise just store the lates
    # condor_streams=>0, # stream stderr/stdout by default (warning: might cause heavy network load)
    # condor_save_joined_file=>0, # if 1 then results/joined contains the results
    # (useful for debugging, otherwise a lot of work)
    # condor_requirements=>'', # used?
    #     # resubmit options : if the status of a condor script is
    #     # either 'finished','submitted','running' or 'crashed',
    #     # decide whether to resubmit it.
    #     # NB Normally the status is empty, e.g. on the first run.
    #     # These are for restarting runs.
    #     condor_resubmit_finished=>0,
    # condor_resubmit_submitted=>0,
    # condor_resubmit_running=>0,
    # condor_resubmit_crashed=>0,
    ##########################
    # Unordered. Need to go through this. Copied from the perl implementation.
    ##########################
    ##
    # return_array_refs=>1, # quicker data parsing mode
    # sort_args=>1,
    # save_args=>1,
    # nice=>'nice -n +20',  # nice command e.g. 'nice -n +10' or ''
    # timeout=>15, # seconds until timeout
    # log_filename=>"/scratch/davidh/results_simulations/tmp/log.txt",
    # # current_log_filename=>"/scratch/davidh/results_simulations/tmp/grid_errors.log",
    ############################################################
    # Set default grid properties (in %self->{_grid_options}}
    # and %{$self->{_bse_options}})
    # This is the first thing that should be called by the user!
    ############################################################
    # # set signal handlers for timeout
    # $self->set_class_signal_handlers();
    # # set operating system
    # my $os = rob_misc::operating_system();
    # %{$self->{_grid_options}}=(
    #     # save operating system
    # operating_system=>$os,
    #     # process name
    #     process_name => 'binary_grid'.$VERSION,
    # grid_defaults_set=>1, # so we know the grid_defaults function has been called
    # # grid suspend files: assume binary_c by default
    # suspend_files=>[$tmp.'/force_binary_c_suspend',
    #         './force_binary_c_suspend'],
    # snapshot_file=>$tmp.'/binary_c-snapshot',
    # ########################################
    # # infomration about the running grid script
    # ########################################
    # working_directory=>cwd(), # the starting directory
    # perlscript=>$0, # the name of the perlscript
    # perlscript_arguments=>join(' ',@ARGV), # arguments as a string
    # perl_executable=>$^X, # the perl executable
    # command_line=>join(' ',$0,@ARGV), # full command line
    # process_ID=>$$, # process ID of the main perl script
    # ########################################
    # # GRID
    # ########################################
    #     # if undef, generate gridcode, otherwise load the gridcode
    #     # from this file. useful for debugging
    #     gridcode_from_file => undef,
    #     # assume binary_grid perl backend by default
    #     backend =>
    #     $self->{_grid_options}->{backend} //
    #     $binary_grid2::backend //
    #     'binary_grid::Perl',
    #     # custom C function for output : this automatically
    #     # binds if a function is available.
    #     C_logging_code => undef,
    #     C_auto_logging => undef,
    #     custom_output_C_function_pointer => binary_c_function_bind(),
    # # control flow
    # rungrid=>1, # usually run the grid, but can be 0
    # # to skip it (e.g. for condor/slurm runs)
    # merge_datafiles=>'',
    # merge_datafiles_filelist=>'',
    # # parameter space options
    # binary=>0, # set to 0 for single stars, 1 for binaries
    #     # if use_full_resolution is 1, then run a dummy grid to
    #     # calculate the resolution. this could be slow...
    #     use_full_resolution => 1,
    # # the probability in any distribution must be within
    # # this tolerance of 1.0, ignored if undef (if you want
    # # to run *part* of the parameter space then this *must* be undef)
    # probability_tolerance=>undef,
    # # how to deal with a failure of the probability tolerance:
    # # 0 = nothing
    # # 1 = warning
    # # 2 = stop
    # probability_tolerance_failmode=>1,
    # # add up and log system error count and probability
    # add_up_system_errors=>1,
    # log_system_errors=>1,
    # # codes, paths, executables etc.
    # # assume binary_c by default, and set its defaults
    # code=>'binary_c',
    # arg_prefix=>'--',
    # prog=>'binary_c', # executable
    # nice=>'nice -n +0', # nice command
    # ionice=>'',
    # # compress output?
    # binary_c_compression=>0,
    #     # get output as array of pre-split array refs
    #     return_array_refs=>1,
    # # environment
    # shell_environment=>undef,
    # libpath=>undef, # for backwards compatibility
    # # where is binary_c? need this to get the values of some counters
    # rootpath=>$self->okdir($ENV{BINARY_C_ROOTPATH}) //
    # $self->okdir($ENV{HOME}.'/progs/stars/binary_c') //
    # '.' , # last option is a fallback ... will fail if it doesn't exist
    # srcpath=>$self->okdir($ENV{BINARY_C_SRCPATH}) //
    # $self->okdir($ENV{BINARY_C_ROOTPATH}.'/src') //
    # $self->okdir($ENV{HOME}.'/progs/stars/binary_c/src') //
    # './src' , # last option is fallback... will fail if it doesn't exist
    # # stack size per thread in megabytes
    # threads_stack_size=>50,
    # # thread sleep time between starting the evolution code and starting
    # # the grid
    # thread_presleep=>0,
    # # threads
    # # Max time a thread can sit looping (with calls to tbse_line)
    # # before a warning is issued : NB this does not catch real freezes,
    # # just infinite loops (which still output)
    # thread_max_freeze_time_before_warning=>10,
    # # run all models by default: modulo=1, offset=0
    # modulo=>1,
    # offset=>0,
    #     # max number of stars on the queue
    #     maxq_per_thread => 100,
    # # data dump file : undef by default (do nothing)
    # results_hash_dumpfile => '',
    # # compress files with bzip2 by default
    # compress_results_hash => 1,
    # ########################################
    # # CPU
    # ########################################
    # cpu_cap=>0, # if 1, limits to one CPU
    # cpu_affinity => 0, # do not bind to a CPU by default
    # ########################################
    # # Code, Timeouts, Signals
    # ########################################
    # binary_grid_code_filtering=>1, #  you want this, it's (MUCH!) faster
    # pre_filter_file=>undef, # dump pre filtered code to this file
    # post_filter_file=>undef,  # dump post filtered code to this file
    # timeout=>30, # timeout in seconds
    # timeout_vb=>0, # no timeout logging
    # tvb=>0, # no thread logging
    # nfs_sleep=>1, # time to wait for NFS to catch up with file accesses
    # # flexigrid checks the timeouts every
    # # flexigrid_timeout_check_interval seconds
    # flexigrid_timeout_check_interval=>0.01,
    # # this is set to 1 when the grid is finished
    # flexigrid_finished=>0,
    # # allow signals by default
    # 'no signals'=>0,
    # # but perhaps disable specific signals?
    # 'disable signal'=>{INT=>0,ALRM=>0,CONT=>0,USR1=>0,STOP=>0},
    # # dummy variables
    # single_star_period=>1e50,  # orbital period of a single star
    # #### timers : set timers to 0 (or empty list) to ignore,
    # #### NB these must be given context (e.g. main::xyz)
    # #### for functions not in binary_grid
    # timers=>0,
    # timer_subroutines=>[
    #     # this is a suggested default list
    #     'flexigrid',
    #         'set_next_alarm',
    #     'vbout',
    #         'vbout_fast',
    #     'run_flexigrid_thread',
    #         'thread_vb'
    # ],
    # ########################################
    # # INPUT/OUTPUT
    # ########################################
    # blocking=>undef, # not yet set
    # # prepend command with stdbuf to stop buffering (if available)
    # stdbuf_command=>`stdbuf --version`=~/stdbuf \(GNU/ ? ' stdbuf -i0 -o0 -e0 ' : undef,
    # vb=>("@ARGV"=~/\Wvb=(\d+)\W/)[0] // 0, # set to 1 (or more) for verbose output to the screen
    # log_dt_secs=>1, # log output to stdout~every log_dt_secs seconds
    # nmod=>10, # every nmod models there is output to the screen,
    # # if log_dt_secs has been exceeded also (ignored if 0)
    # colour=>1, # set to 1 to use the ANSIColor module for colour output
    # log_args=>0, # do not log args in files
    # log_fins=>0, # log end of runs too
    #     sort_args=>0, # do not sort args
    # save_args=>0, # do not save args in a string
    # log_args_dir=>$tmp, # where to output the args files
    # always_reopen_arg_files=>0, # if 1 then arg files are always closed and reopened
    #   (may cause a lot of disk I/O)
    # lazy_arg_sending=>1, # if 1, the previous args are remembered and
    # # only args that changed are sent (except M1, M2 etc. which always
    # # need sending)
    # # force output files to open on a local disk (not an NFS partion)
    # # not sure how to do this on another OS
    # force_local_hdd_use=>($os eq 'unix'),
    # # for verbose output, define the newline
    # # For terminals use "\x0d", for files use "\n", in the
    # # case of multiple threads this will be set to \n
    # newline=> "\x0d",
    #     # use reset_stars_defaults
    #     reset_stars_defaults=>1,
    # # set signal captures: argument determines behaviour when the code locks up
    # # 0: exit
    # # 1: reset and try the next star (does this work?!)
    # alarm_procedure=>1,
    # # exit on eval failure?
    # exit_on_eval_failure=>1,
    # ## functions: these should be set by perl lexical name
    # ## (they are automatically converted to function pointers
    # ## at runtime)
    # # function to be called just before a thread is created
    # thread_precreate_function=>undef,
    #     thread_precreate_function_pointer=>undef,
    # # function to be called just after a thread is created
    # # (from inside the thread just before *grid () call)
    # threads_entry_function=>undef,
    #     threads_entry_function_pointer=>undef,
    # # function to be called just after a thread is finished
    # # (from inside the thread just after *grid () call)
    # threads_flush_function=>undef,
    # threads_flush_function_pointer=>undef,
    # # function to be called just after a thread is created
    # # (but external to the thread)
    # thread_postrun_function=>undef,
    # thread_postrun_function_pointer=>undef,
    # # function to be called just before a thread join
    # # (external to the thread)
    # thread_prejoin_function=>undef,
    # thread_prejoin_function_pointer=>undef,
    # # default to using the internal join_flexigrid_thread function
    # threads_join_function=>'binary_grid2::join_flexigrid_thread',
    # threads_join_function_pointer=>sub{return $self->join_flexigrid_thread(@_)},
    # # function to be called just after a thread join
    # # (external to the thread)
    # thread_postjoin_function=>undef,
    # thread_postjoin_function_pointer=>undef,
    # # usually, parse_bse in the main script is called
    # parse_bse_function=>'main::parse_bse',
    #     parse_bse_function_pointer=>undef,
    # # if starting_snapshot_file is defined, load initial
    # # values for the grid from the snapshot file rather
    # # than a normal initiation: this enables you to
    # # stop and start a grid
    # starting_snapshot_file=>undef,
}

# Grid containing the descriptions of the options # TODO: add input types for all of them
grid_options_descriptions = {
    "tmp_dir": "Directory where certain types of output are stored. The grid code is stored in that directory, as well as the custom logging libraries. Log files and other diagnostics will usually be written to this location, unless specified otherwise",  # TODO: improve this
    "_binary_c_dir": "Director where binary_c is stored. This options are not really used",
    "_binary_c_config_executable": "Full path of the binary_c-config executable. This options is not used in the population object.",
    "_binary_c_executable": "Full path to the binary_c executable. This options is not used in the population object.",
    "_binary_c_shared_library": "Full path to the libbinary_c file. This options is not used in the population object",
    "verbosity": "Verbosity of the population code. Default is 0, by which only errors will be printed. Higher values will show more output, which is good for debugging.",
    "binary": "Set this to 1 if the population contains binaries. Input: int",  # TODO: write what effect this has.
    "num_cores": "The number of cores that the population grid will use. The multiprocessing is useful but make sure to figure out how many logical cores the machine has (use e.g. psutil.cpu_count(logical=False) to find the true number of cores, psutil.cpu_count(logical=True) to find the number of logical cores). The core is multi processed, not multi threaded, and will gain no extra speed when num_cores exceeds the number of logical cores. Input: int",
    "_start_time_evolution": "Variable storing the start timestamp of the population evolution. Set by the object itself.",  # TODO: make sure this is logged to a file
    "_end_time_evolution": "Variable storing the end timestamp of the population evolution. Set by the object itself",  # TODO: make sure this is logged to a file
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
    "log_args": "Boolean to log the arguments of the current running system. ", 
    "log_args_dir": "Directory to log the arguments of the current running system to.",
    "log_file": "Log file for the population object. Unused",  # TODO: fix the functionality for this and describe it properly
    "custom_logging_func_memaddr": "Memory address where the custom_logging_function is stored. Input: int",
    "_count": "Counter tracking which system the generator is on.",
    "_probtot": "Total probability of the population.",  # TODO: check whether this is used properly throughout
    "_main_pid": "Main process ID of the master process. Used and set by the population object.",
    "_store_memaddr": "Memory address of the store object for binary_c.",
    "failed_systems_threshold": "Variable storing the maximum number of systems that are allowed to fail before logging their command line arguments to failed_systems log files",
    "parse_function": "Function that the user can provide to handle the output the binary_c. This function has to take the arguments (self, output). Its best not to return anything in this function, and just store stuff in the self.grid_results dictionary, or just output results to a file",
    "condor": "Int flag whether to use a condor type population evolution. Not implemented yet.",  # TODO: describe this in more detail
    "slurm": "Int flag whether to use a Slurm type population evolution.",  # TODO: describe this in more detail
    "weight": "Weight factor for each system. The calculated probability is multiplied by this. If the user wants each system to be repeated several times, then this variable should not be changed, rather change the _repeat variable instead, as that handles the reduction in probability per system. This is useful for systems that have a process with some random element in it.",  # TODO: add more info here, regarding the evolution splitting.
    "repeat": "Factor of how many times a system should be repeated. Consider the evolution splitting binary_c argument for supernovae kick repeating.",  # TODO: make sure this is used.
    "evolution_type": "Variable containing the type of evolution used of the grid. Multiprocessing or linear processing",
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
    "_Moe2017_JSON_data": "Location to store the loaded Moe&diStefano2017 dataset",  # Stores the data
}

###
#

MIN_MASS_BINARY_C = float(
    return_binary_c_version_info(parsed=True)["macros"]["BINARY_C_MINIMUM_STELLAR_MASS"]
)


# Default options for the Moe & di Stefano grid
moe_di_stefano_default_options = {
    # place holder for the JSON data to be used if a file
    # isn't specified
    "JSON": None,
    # resolution data
    "resolutions": {
        "M": [
            20,  # M1
            20,  # M2 (i.e. q)
            0,  # M3 currently unused
            0,  # M4 currently unused
        ],
        "logP": [
            20,  # P2 (binary period)
            0,  # P3 (triple period) currently unused
            0,  # P4 (quadruple period) currently unused
        ],
        "ecc": [
            10,  # e (binary eccentricity)
            0,  # e2 (triple eccentricity) currently unused
            0,  # e3 (quadruple eccentricity) currently unused
        ],
    },
    "samplerfuncs": {
        "M": [None, None, None, None],
        "logP": [None, None, None],
        "ecc": [None, None, None],
    },
    "ranges": {
        # stellar masses (Msun)
        "M": [
            MIN_MASS_BINARY_C
            * 1.05,  # 0.08 is a tad bit above the minimum mass. Don't sample at 0.07, otherwise the first row of q values will have a phasevol of 0. Anything higher is fine.
            80.0,  # (rather arbitrary) upper mass cutoff
        ],
        "q": [
            None,  # artificial qmin : set to None to use default
            None,  # artificial qmax : set to None to use default
        ],
        "logP": [0.0, 8.0],  # 0 = log10(1 day)  # 8 = log10(10^8 days)
        "ecc": [0.0, 0.99],
    },
    # minimum stellar mass
    "Mmin": MIN_MASS_BINARY_C,  # We take the value that binary_c has set as the default
    # multiplicity model (as a function of log10M1)
    #
    # You can use 'Poisson' which uses the system multiplicity
    # given by Moe and maps this to single/binary/triple/quad
    # fractions.
    #
    # Alternatively, 'data' takes the fractions directly
    # from the data, but then triples and quadruples are
    # combined (and there are NO quadruples).
    "multiplicity_model": "Poisson",
    # multiplicity modulator:
    # [single, binary, triple, quadruple]
    #
    # e.g. [1,0,0,0] for single stars only
    #      [0,1,0,0] for binary stars only
    #
    # defaults to [1,1,0,0] i.e. all types
    #
    "multiplicity_modulator": [
        1,  # single
        1,  # binary
        0,  # triple
        0,  # quadruple
    ],
    # given a mix of multiplicities, you can either (noting that
    # here (S,B,T,Q) = appropriate modulator * model(S,B,T,Q) )
    #
    # 'norm'  : normalise so the whole population is 1.0
    #           after implementing the appropriate fractions
    #           S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
    #
    # 'raw'   : stick to what is predicted, i.e.
    #           S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
    #           without normalisation
    #           (in which case the total probability < 1.0 unless
    #            all you use single, binary, triple and quadruple)
    #
    # 'merge' : e.g. if you only have single and binary,
    #           add the triples and quadruples to the binaries, so
    #           binaries represent all multiple systems
    #           ...
    #           *** this is canonical binary population synthesis ***
    #
    #           Note: if multiplicity_modulator == [1,1,1,1] this
    #                 option does nothing (equivalent to 'raw').
    #
    #
    # note: if you only set one multiplicity_modulator
    # to 1, and all the others to 0, then normalising
    # will mean that you effectively have the same number
    # of stars as single, binary, triple or quad (whichever
    # is non-zero) i.e. the multiplicity fraction is ignored.
    # This is probably not useful except for
    # testing purposes or comparing to old grids.
    "normalize_multiplicities": "merge",
    # q extrapolation (below 0.15 and above 0.9) method. We can choose from ['flat', 'linear', 'plaw2', 'nolowq']
    "q_low_extrapolation_method": "linear",
    "q_high_extrapolation_method": "linear",
}

moe_di_stefano_default_options_description = {
    "resolutions": "",
    "ranges": "",
    "Mmin": "Minimum stellar mass",
    "multiplicity_model": """
multiplicity model (as a function of log10M1)

You can use 'Poisson' which uses the system multiplicity
given by Moe and maps this to single/binary/triple/quad
fractions.

Alternatively, 'data' takes the fractions directly
from the data, but then triples and quadruples are
combined (and there are NO quadruples).
""",
    "multiplicity_modulator": """
[single, binary, triple, quadruple]

e.g. [1,0,0,0] for single stars only
     [0,1,0,0] for binary stars only

defaults to [1,1,0,0] i.e. singles and binaries
""",
    "normalize_multiplicities": """
'norm': normalise so the whole population is 1.0
        after implementing the appropriate fractions
        S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
        given a mix of multiplicities, you can either (noting that
        here (S,B,T,Q) = appropriate modulator * model(S,B,T,Q) )
        note: if you only set one multiplicity_modulator
        to 1, and all the others to 0, then normalising
        will mean that you effectively have the same number
        of stars as single, binary, triple or quad (whichever
        is non-zero) i.e. the multiplicity fraction is ignored.
        This is probably not useful except for
        testing purposes or comparing to old grids.

'raw'   : stick to what is predicted, i.e.
          S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
          without normalisation
          (in which case the total probability < 1.0 unless
          all you use single, binary, triple and quadruple)

'merge' : e.g. if you only have single and binary,
          add the triples and quadruples to the binaries, so
          binaries represent all multiple systems
          ...
          *** this is canonical binary population synthesis ***

          It only takes the maximum multiplicity into account,
          i.e. it doesn't multiply the resulting array by the multiplicity modulator again.
          This prevents the resulting array to always be 1 if only 1 multiplicity modulator element is nonzero

          Note: if multiplicity_modulator == [1,1,1,1]. this option does nothing (equivalent to 'raw').
""",
    "q_low_extrapolation_method": """
q extrapolation (below 0.15) method
    none
    flat
    linear2
    plaw2
    nolowq
""",
    "q_high_extrapolation_method": "Same as q_low_extrapolation_method",
}


#################################
# Grid options functions

# Utility functions
def grid_options_help(option: str) -> dict:
    """
    Function that prints out the description of a grid option. Useful function for the user.

    Args:
        option: which option you want to have the description of

    returns:
        dict containing the option, the description if its there, otherwise empty string. And if the key doesnt exist, the dict is empty
    """

    option_keys = grid_options_defaults_dict.keys()
    description_keys = grid_options_descriptions.keys()

    if not option in option_keys:
        print(
            "Error: This is an invalid entry. Option does not exist, please choose from the following options:\n\t{}".format(
                ", ".join(option_keys)
            )
        )
        return {}

    else:
        if not option in description_keys:
            print(
                "This option has not been described properly yet. Please contact on of the authors"
            )
            return {option: ""}
        else:
            print(grid_options_descriptions[option])
            return {option: grid_options_descriptions[option]}


def grid_options_description_checker(print_info: bool = True) -> int:
    """
    Function that checks which descriptions are missing

    Args:
        print_info: whether to print out information about which options contain proper descriptions and which do not

    Returns:
        the number of undescribed keys
    """

    # Get the keys
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


def write_grid_options_to_rst_file(output_file: str) -> None:
    """
    Function that writes the descriptions of the grid options to a rst file

    Tasks:
        TODO: separate things into private and public options

    Args:
        output_file: target file where the grid options descriptions are written to
    """

    # Get the options and the description
    options = grid_options_defaults_dict
    descriptions = grid_options_descriptions

    # Get those that do not have a description
    not_described_yet = list(set(options) - set(descriptions))

    # separate public and private options
    public_options = [key for key in options if not key.startswith("_")]
    private_options = [key for key in options if key.startswith("_")]

    # Check input
    if not output_file.endswith(".rst"):
        print("Filename doesn't end with .rst, please provide a proper filename")
        return None

    with open(output_file, "w") as f:
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
        print_option_descriptions(
            f,
            public_options,
            descriptions,
            "Public options",
            "The following options are meant to be changed by the user.",
        )

        # Moe & di Stefano options:
        print_option_descriptions(
            f,
            moe_di_stefano_default_options,
            moe_di_stefano_default_options_description,
            "Moe & di Stefano sampler options",
            "The following options are meant to be changed by the user.",
        )

        # Start private options part
        print_option_descriptions(
            f,
            private_options,
            descriptions,
            "Private options",
            "The following options are not meant to be changed by the user, as these options are used and set internally by the object itself. The description still is provided, but just for documentation purposes.",
        )


def print_option_descriptions(filehandle, options, descriptions, title, extra_text):
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

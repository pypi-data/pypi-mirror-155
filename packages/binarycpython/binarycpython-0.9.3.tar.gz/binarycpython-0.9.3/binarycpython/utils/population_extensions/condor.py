"""
The class extension for the population object that contains the Condor functionality

TODO: there are many uses of $<variable name> in this file but this is not perl and we should replace them by actual format placeholders
"""

# pylint: disable=E1101

import os
import re
import sys
import stat
import time
import subprocess

import pathlib

import datasize
import lib_programname
from binarycpython.utils.functions import (
    command_string_from_list,
    now,
)


class condor:
    """
    Extension for the Population class containing the code for Condor grid runs
    """

    def __init__(self, **kwargs):
        """
        Init function for the condor class
        """

        return

    def condorID(self, ClusterID=None, Process=None):
        """
        Function to return a Condor job ID as a string, [ClusterID].[Process]. The ClusterID and Process passed in are used if given, otherwise we default to the condor_ClusterID and condor_Process in grid_options.
        """
        if ClusterID is None:
            ClusterID = self.grid_options["condor_ClusterID"]
        if Process is None:
            Process = self.grid_options["condor_Process"]
        return "{ClusterID}.{Process}".format(ClusterID=ClusterID, Process=Process)

    def condorpath(self, path, condor_dir=None):
        """
        Function to return the full condor directory path.
        """

        if condor_dir is None:
            condor_dir = self.grid_options["condor_dir"]
        return os.path.abspath(os.path.join(condor_dir, path))

    def condor_status_file(self, ClusterID=None, Process=None, condor_dir=None):
        """
        Return the condor status file corresponding to the ClusterID and Process, which default to grid_options condor_ClusterID and condor_Process, respectively.
        """
        return os.path.join(
            self.condorpath("status", condor_dir=condor_dir),
            self.condorID(ClusterID, Process),
        )

    def condor_check_requirements(self):
        """
        Function to check whether the condor parameters in grid_options have been set appropriately.
        """
        if self.grid_options["condor"] > 0 and (
            self.grid_options["condor_dir"] is None
            or not os.path.isdir(self.grid_options["condor_dir"])
        ):
            return (
                False,
                "You have set condor={condor} but not set condor_dir ({condor_dir}) correctly. Please set it and try again.".format(
                    condor=self.grid_options["condor"],
                    condor_dir=self.grid_options["condor_dir"],
                ),
            )
        return (True, "")

    def condor_dirs(self):
        """
        Directories associated specifically with this condor job.
        """

        return ["condor_dir"]

    def set_condor_status(self, string, condor_dir=None):
        """
        Set the condor status corresponing to the self object, which should have condor_ClusterID and condor_Process set.

        Args:
            string : the status string to be set
            dir : the directory in which the status directory is held. If not set, this defaults to the HPC directory (e.g. slurm_dir or condor_dir).
        """
        # save condor ClusterID to file

        if condor_dir is None:
            condor_dir = self.grid_options["condor_dir"]

        idfile = os.path.join(condor_dir, "ClusterID")
        if not os.path.exists(idfile):
            with self.open(idfile, "w", encoding="utf-8") as fClusterID:
                fClusterID.write(
                    "{ClusterID}\n".format(
                        ClusterID=self.grid_options["condor_ClusterID"]
                    )
                )
                fClusterID.close()
                self.NFS_flush_hack(idfile)

        # save condor status
        file = self.condor_status_file(condor_dir=condor_dir)
        if file:
            with self.open(file, "w", encoding="utf-8") as f:
                f.write(string)
                f.close()
                self.NFS_flush_hack(file)

    def get_condor_status(self, ClusterID=None, Process=None, condor_dir=None):
        """
        Get and return the condor status corresponing to the self object, or ClusterID.Process if they are passed in. If no status is found, returns an empty string..
        """
        if ClusterID is None:
            ClusterID = self.grid_options["condor_ClusterID"]
        if Process is None:
            Process = self.grid_options["condor_Process"]
        if ClusterID is None or Process is None:
            return None
        # print("get_condor_status {}.{}".format(ClusterID,Process))

        try:
            path = pathlib.Path(
                self.condor_status_file(
                    condor_dir=condor_dir, ClusterID=ClusterID, Process=Process
                )
            )
            # print("path={}".format(path))
            # print("size={}".format(path.stat().st_size))
            if path:
                s = path.read_text().strip()
                # print("contains {}".format(s))
                return s
            # print("path empty")
            return ""

        # NOTE: What is the actual exception that can occur here?
        # TODO: We should specify that exception
        except:
            # print("read failed")
            return ""

    def condor_outfile(self, condor_dir=None):
        """
        return a standard filename for the condor chunk files
        """
        file = "{id}.gz".format(id=self.condorID())
        if condor_dir is None:
            condor_dir = self.grid_options["condor_dir"]
        return os.path.abspath(os.path.join(condor_dir, "results", file))

    def make_condor_dirs(self, condor_dir=None):
        """
        Function to make the condor directories
        """

        # make the condor directories
        if condor_dir is None:
            condor_dir = self.grid_options["condor_dir"]
        if not condor_dir:
            print(
                "You must set self.grid_options['condor_dir'] (or pass condor_dir=whatever to make_condor_dirs()) to a directory which we can use to set up binary_c-python's Condor files. This should be unique to your set of grids."
            )
            os.exit()

        # make a list of directories, these contain the various condor
        # output, status files, etc.
        dirs = []
        for d in ["stdout", "stderr", "log", "results", "status", "snapshots"]:
            dirs.append(self.condorpath(d, condor_dir=condor_dir))

        # make the directories: we do not allow these to already exist
        # as the condor directory should be a fresh location for each set of jobs
        for d in dirs:
            try:
                pathlib.Path(self.condorpath(d, condor_dir=condor_dir)).mkdir(
                    exist_ok=False, parents=True
                )
            # TODO: specify the actual exception
            # TODO: is this try-except necessary? Especially having the code fail here, instead of earlier, if the directories exist already. Otherwise we can also just do exist_ok=True?
            except:
                print(
                    "Tried to make the directory {d} but it already exists. When you launch a set of binary_c jobs on Condor, you need to set your condor_dir to be a fresh directory with no contents.".format(
                        d=d
                    )
                )
                self.exit(code=1)

        # check that they have been made and exist: we need this
        # because on network mounts (NFS) there's often a delay between the mkdir
        # above and the actual directory being made. This shouldn't be too long...
        fail = True
        count = 0
        count_warn = 10
        while fail is True:
            fail = False
            count += 1
            if count > count_warn:
                print(
                    "Warning: Have been waiting about {} seconds for Condor directories to be made, there seems to be significant delay...".format(
                        count
                    )
                )
            for d in dirs:
                if os.path.isdir(d) is False:
                    fail = True
                    time.sleep(1)
                    break

    def condor_grid(self): # pragma: no cover
        """
        function to be called when running grids when grid_options['condor']>=1

        if grid_options['condor']==1, we set up the condor script and launch the jobs, then return True to exit.
        if grid_options['condor']==2, we run the stars, which means we return False to continue.
        if grid_options['condor']==3, we are being called from the jobs to run the grids, return False to continue.

        TODO: split this function into some parts
        TODO: Comment this function better
        """

        if self.grid_options["condor"] == 3:
            # joining : set the evolution type to "join"
            #
            # return False to continue
            self.grid_options["evolution_type"] = "join"
            return False

        if self.grid_options["condor"] == 2:
            # run a grid of stars only, leaving the results
            # in the appropriate outfile
            #
            # return False to actually run the stars
            self.grid_options["evolution_type"] = "grid"
            return False

        if self.grid_options["condor"] == 1:
            # if condor=1,  we should have no evolution type, we
            # set up the Condor scripts and get them evolving
            # in a Condor queue
            self.grid_options["evolution_type"] = None

            # make dirs
            self.make_condor_dirs()

            # check we're not using too much RAM
            if datasize.DataSize(
                self.grid_options["condor_memory"]
            ) > datasize.DataSize(self.grid_options["condor_warn_max_memory"]):
                print(
                    "WARNING: you want to use {} MB of RAM : this is unlikely to be correct. If you believe it is, set condor_warn_max_memory to something very large (it is currently {} MB)\n".format(
                        self.grid_options["condor_memory"],
                        self.grid_options["condor_warn_max_memory"],
                    )
                )
                self.exit(code=1)

            # get job id (might be passed in)
            ClusterID = (
                self.grid_options["condor_ClusterID"]
                if self.grid_options["condor_ClusterID"] != ""
                else "$ClusterID"
            )

            # get job array index
            Process = (
                self.grid_options["condor_Process"]
                if self.grid_options["condor_Process"] != ""
                else "$Process"
            )

            if self.grid_options["condor_njobs"] == 0:
                print(
                    "binary_c-python Condor : You must set grid_option condor_njobs to be non-zero"
                )
                self.exit(code=1)

            # find the path to the Python script that we are running
            pyscriptpath = str(lib_programname.get_path_executed_script())

            # set the condor initial dir to be our current working directory
            if not self.grid_options["condor_initial_dir"]:
                self.grid_options["condor_initial_dir"] = os.getcwd()

            # build the grid command
            grid_command = (
                [
                    str(self.grid_options["condor_env"]),
                    sys.executable,
                    pyscriptpath,
                ]
                + sys.argv[1:]
                + [
                    "start_at=$Process",  # Process is 0,1,2... which is what we want
                    "modulo=" + str(self.grid_options["condor_njobs"]),
                    "condor_njobs=" + str(self.grid_options["condor_njobs"]),
                    "condor_dir=" + self.grid_options["condor_dir"],
                    "verbosity=" + str(self.grid_options["verbosity"]),
                    "num_cores=" + str(self.grid_options["num_processes"]),
                ]
            )

            grid_command = command_string_from_list(grid_command)

            # make condor script paths
            submit_script_path = self.condorpath("condor_submit_script")
            job_script_path = self.condorpath("condor_job_script")

            # open the files
            try:
                submit_script = self.open(submit_script_path, "w", encoding="utf-8")
            except IOError:
                print(
                    "Could not open Condor script at {path} for writing: please check you have set {condor_dir} correctly (it is currently {condor_dir} and can write to this directory.".format(
                        path=submit_script_path,
                        condor_dir=self.grid_options["condor_dir"],
                    )
                )
            try:
                job_script = self.open(job_script_path, "w", encoding="utf-8")
            except IOError:
                print(
                    "Could not open Condor script at {path} for writing: please check you have set {condor_dir} correctly (it is currently {condor_dir} and can write to this directory.".format(
                        path=job_script_path, condor_dir=self.grid_options["condor_dir"]
                    )
                )

            ############################################################
            # The condor job script calls your binary_c-pthyon script
            ############################################################
            condor_job_script = """#!{bash}
echo "Condor Job Args: $@"

# first two arguments are ClusterID and Process
export ClusterID="$1"
export Process="$2"
shift 2

echo "Job ClusterID $ClusterID Process $Process"

# Set binary_c startup conditions
export BINARY_C_PYTHON_ORIGINAL_CMD_LINE={cmdline}
export BINARY_C_PYTHON_ORIGINAL_WD=`{pwd}`
export BINARY_C_PYTHON_ORIGINAL_SUBMISSION_TIME=`{date}`

# set status to \"running\"
echo \"running\" > "{condor_dir}/status/$ClusterID.$ProcessID"

# make list of files which is checked for joining
# echo "{condor_dir}/results/$ClusterID.$Process.gz" >> "{condor_dir}/results/$ClusterID.all"

# run grid of stars and, if this returns 0, set status to finished
{grid_command} "condor=2" "evolution_type=grid" "condor_ClusterID=$ClusterID" "condor_Process=$Process" "save_population_object={condor_dir}/results/$ClusterID.$Process.gz" && echo -n \"finished\" > "{condor_dir}/status/$ClusterID.$ProcessID" && echo """.format(
                bash=self.grid_options["condor_bash"],
                date=self.grid_options["condor_date"],
                pwd=self.grid_options["condor_pwd"],
                cmdline=repr(self.grid_options["command_line"]),
                grid_command=grid_command,
                condor_dir=self.grid_options["condor_dir"],
            )

            if not self.grid_options["condor_postpone_join"]:
                joinfile = "{condor_dir}/results/{ClusterID}.all".format(
                    condor_dir=self.grid_options["condor_dir"], ClusterID=ClusterID
                )
                condor_job_script += """&& echo \"Checking if we can join...\" && echo && {grid_command} "condor=3" "evolution_type=join" "joinlist={joinfile}" "condor_ClusterID=$ClusterID" "condor_Process=$Process"
                """.format(
                    bash=self.grid_options["condor_bash"],
                    grid_command=grid_command,
                    joinfile=joinfile,
                )

                ############################################################
                # The Condor submit script is sent to condor_submit
                # In here we know $(Cluster) and $(Process) which identify
                # each job
                ############################################################
                extra_settings = ""
                if self.grid_options["condor_extra_settings"]:
                    for key in self.grid_options["condor_extra_settings"]:
                        extra_settings += "{key} = {value}\n".format(
                            key=key,
                            value=self.grid_options["condor_extra_settings"][key],
                        )

                jobid = "$(Cluster).$(Process)"
                condor_submit_script = """
executable = {usr_bin_env}
arguments = {bash} {job_script_path} $(Cluster) $(Process)
universe = {universe}
getenv = {getenv}
initial_dir = {initial_dir}
output = {outfile}
error = {errfile}
log = {logfile}
stream_output = {stream_output}
stream_error = {stream_error}
request_memory = {request_memory}
request_cpus = {request_cpus}
should_transfer_files = {should_transfer_files}
when_to_transfer_output = {when_to_transfer_output}
requirements = {requirements}
JobBatchName = {batchname}
kill_sig = {kill_sig}
{extra_settings}
queue {njobs}
            """.format(
                    usr_bin_env=self.grid_options["condor_env"],
                    bash=self.grid_options["condor_bash"],
                    job_script_path=job_script_path,
                    universe=self.grid_options["condor_universe"],
                    getenv=self.grid_options["condor_getenv"],
                    initial_dir=self.grid_options["condor_initial_dir"],
                    outfile=os.path.abspath(
                        os.path.join(self.grid_options["condor_dir"], "stdout", jobid)
                    ),
                    errfile=os.path.abspath(
                        os.path.join(self.grid_options["condor_dir"], "stderr", jobid)
                    ),
                    logfile=os.path.abspath(
                        os.path.join(self.grid_options["condor_dir"], "log", jobid)
                    ),
                    stream_output=self.grid_options["condor_stream_output"],
                    stream_error=self.grid_options["condor_stream_error"],
                    request_memory=self.grid_options["condor_memory"],
                    request_cpus=self.grid_options["num_processes"],
                    should_transfer_files=self.grid_options[
                        "condor_should_transfer_files"
                    ],
                    when_to_transfer_output=self.grid_options[
                        "condor_when_to_transfer_output"
                    ],
                    requirements=self.grid_options["condor_requirements"],
                    batchname=self.grid_options["condor_batchname"],
                    kill_sig=self.grid_options["condor_kill_sig"],
                    extra_settings=extra_settings,
                    njobs=self.grid_options["condor_njobs"],
                )

            # write the scripts, close them and make them executable by
            # all (so the condor user can pick it up)
            for file, contents in [
                (submit_script, condor_submit_script),
                (job_script, condor_job_script),
            ]:
                path = file.name
                file.writelines(contents)
                file.close()
                os.chmod(
                    path,
                    stat.S_IREAD
                    | stat.S_IWRITE
                    | stat.S_IEXEC
                    | stat.S_IRGRP
                    | stat.S_IXGRP
                    | stat.S_IROTH
                    | stat.S_IXOTH,
                )

            if not self.grid_options["condor_postpone_submit"]:
                # call sbatch to launch the condor jobs
                cmd = [self.grid_options["condor_submit"], submit_script_path]
                with subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                ) as pipes:
                    std_out, std_err = pipes.communicate()

                if pipes.returncode != 0:
                    # an error happened!
                    err_msg = "{red}{err}\nReturn Code: {code}{reset}".format(
                        err=std_err.strip(),
                        code=pipes.returncode,
                        red=self.ANSI_colours["red"],
                        reset=self.ANSI_colours["reset"],
                    )
                    raise Exception(err_msg)

                if len(std_err) > 0:
                    print(
                        "{red}{err}{reset}".format(
                            red=self.ANSI_colours["red"],
                            reset=self.ANSI_colours["reset"],
                            err=std_err.strip().decode("utf-8"),
                        )
                    )

                print(
                    "{yellow}{out}{reset}".format(
                        yellow=self.ANSI_colours["yellow"],
                        reset=self.ANSI_colours["reset"],
                        out=std_out.strip().decode("utf-8"),
                    )
                )
            else:
                # just say we would have (use this for testing)
                print(
                    "Condor script is at {path} but has not been launched".format(
                        path=submit_script_path
                    )
                )

        # some messages to the user, then return
        if self.grid_options["condor_postpone_submit"] == 1:
            print(
                "Condor script written, to {path}, but launching the jobs with sbatch was postponed.".format(
                    path=submit_script_path
                )
            )
        else:
            print("Condor jobs launched.")
            print("All done in condor_grid().")

        # return True so we exit immediately
        return True

    def condor_queue_stats(self): # pragma: no cover
        """
        Return condor queue statistics for this job
        """

        _id = self.grid_options["condor_ClusterID"]
        if not _id:
            return None

        cmd = "{} {} 2>&1".format(
            "/usr/bin/condor_q", _id  # self.grid_options["condor_q"],
        )
        print("Q cmd", cmd)

        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as subp:
            result = subp.stdout.read()
        print("Q result ", result)

        if not result:
            return None

        d = {}
        for x in [
            "jobs",
            "completed",
            "removed",
            "idle",
            "running",
            "held",
            "suspended",
        ]:
            print("Q x ", x)
            m = re.search("(\d+)\s+{}".format(x), result)
            print("Q m ", m)
            if m:
                d[x] = m.group(0)

        print("Q d ", d)
        return d

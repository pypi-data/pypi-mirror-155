"""
Module containing the Slurm functions for the binarycpython package.

This class object is an extension to the population grid object
"""

# pylint: disable=E1101

import os
import sys
import time
import stat
import pathlib
import subprocess

import datasize
import lib_programname
from binarycpython.utils.functions import (
    command_string_from_list,
    now,
)


class slurm:
    """
    Extension for the Population class containing the code for Slurm grid simulations
    """

    def __init__(self, **kwargs):
        """
        Init function for the slurm class
        """

        return

    def slurmID(self, jobid=None, jobarrayindex=None):
        """
        Function to return a Slurm job ID as a string, [jobid].[jobarrayindex]. The jobid and jobarrayindex passed in are used if given, otherwise we default to the jobid and jobarrayindex in grid_options.
        """
        if jobid is None:
            jobid = self.grid_options["slurm_jobid"]
        if jobarrayindex is None:
            jobarrayindex = self.grid_options["slurm_jobarrayindex"]
        return "{jobid}.{jobarrayindex}".format(
            jobid=jobid, jobarrayindex=jobarrayindex
        )

    def slurmpath(self, path, slurm_dir=None):
        """
        Function to return the full slurm directory path.
        """
        if slurm_dir is None:
            slurm_dir = self.grid_options["slurm_dir"]

        return os.path.abspath(os.path.join(slurm_dir, path))

    def slurm_status_file(self, jobid=None, jobarrayindex=None, slurm_dir=None):
        """
        Return the slurm status file corresponding to the jobid and jobarrayindex, which default to grid_options slurm_jobid and slurm_jobarrayindex, respectively.
        """
        return os.path.join(
            self.slurmpath("status", slurm_dir=slurm_dir),
            self.slurmID(jobid=jobid, jobarrayindex=jobarrayindex),
        )

    def slurm_check_requirements(self):
        """
        Function to check whether the slurm parameters in grid_options have been set appropriately.
        """

        if self.grid_options["slurm"] > 0 and (
            self.grid_options["slurm_dir"] is None
            or not os.path.isdir(self.grid_options["slurm_dir"])
        ):
            return (
                False,
                "You have set slurm={slurm} but not set slurm_dir ({slurm_dir}) correctly. Please set it and try again.".format(
                    slurm=self.grid_options["slurm"],
                    slurm_dir=self.grid_options["slurm_dir"],
                ),
            )
        return (True, "")

    def slurm_dirs(self):
        """
        Directories associated specifically with this slurm job.
        """
        return ["slurm_dir"]

    def set_slurm_status(self, string, slurm_dir=None):
        """
        Set the slurm status corresponing to the self object, which should have slurm_jobid and slurm_jobarrayindex set.

        Args:
            string : the status string to be set
            slurm_dir : the directory in which the status directory is held. If not set, this defaults to the HPC directory (e.g. slurm_dir or condor_dir).
        """
        # save slurm jobid to file
        if slurm_dir is None:
            slurm_dir = self.grid_options["slurm_dir"]

        idfile = os.path.join(slurm_dir, "jobid")
        if not os.path.exists(idfile):
            with self.open(idfile, "w", encoding="utf-8") as fjobid:
                fjobid.write("{jobid}\n".format(jobid=self.grid_options["slurm_jobid"]))
                fjobid.close()
                self.NFS_flush_hack(idfile)

        # save slurm status
        status_file = self.slurm_status_file(slurm_dir=slurm_dir)
        if status_file:
            with self.open(status_file, "w", encoding="utf-8") as f:
                f.write(string)
                f.close()
                self.NFS_flush_hack(status_file)

        print("Have set status in",status_file,"to",string)
        with self.open(status_file,"r",encoding="utf-8") as f:
            print("Contents")
            print(f.readlines())
            f.close()

    def get_slurm_status(self, jobid=None, jobarrayindex=None, slurm_dir=None):
        """
        Get and return the slurm status string corresponing to the self object, or jobid.jobarrayindex if they are passed in. If no status is found, returns an empty string.
        """
        if jobid is None:
            jobid = self.grid_options["slurm_jobid"]
        if jobarrayindex is None:
            jobarrayindex = self.grid_options["slurm_jobarrayindex"]
        if jobid is None or jobarrayindex is None:
            return None
        try:

            path = pathlib.Path(
                self.slurm_status_file(
                    slurm_dir=slurm_dir, jobid=jobid, jobarrayindex=jobarrayindex
                )
            )
            if path:
                self.NFS_flush_hack(path)
                return path.read_text().strip()
            return ""
        # TODO: Fix bare exception
        except:
            return ""

    def slurm_outfile(self, slurm_dir=None):
        """
        return a standard filename for the slurm chunk files
        """
        file = "{id}.gz".format(
            id=self.slurmID(),
        )
        if slurm_dir is None:
            slurm_dir = self.grid_options["slurm_dir"]
        return os.path.abspath(os.path.join(slurm_dir, "results", file))

    def make_slurm_dirs(self, slurm_dir=None):
        """
        Function to create the necessary slurm directories
        """

        # TODO: replace the code block below with a function call to slurmpath
        # make the slurm directories
        if slurm_dir is None:
            slurm_dir = self.grid_options["slurm_dir"]

        if not slurm_dir:
            print(
                "You must set self.grid_options['slurm_dir'] (or pass slurm_dir=whatever to make_slurm_dirs()) to a directory which we can use to set up binary_c-python's Slurm files. This should be unique to your set of grids."
            )
            os.exit()

        # make a list of directories, these contain the various slurm
        # output, status files, etc.
        dirs = []
        for slurm_subdir in ["stdout", "stderr", "results", "status", "snapshots"]:
            dirs.append(self.slurmpath(slurm_subdir))

        # make the directories: we do not allow these to already exist
        # as the slurm directory should be a fresh location for each set of jobs
        for d in dirs:
            try:
                pathlib.Path(self.slurmpath(d, slurm_dir=slurm_dir)).mkdir(
                    exist_ok=False, parents=True
                )
            # TODO: fix this bare exception
            except:
                print(
                    "Tried to make the directory {d} but it already exists. When you launch a set of binary_c jobs on Slurm, you need to set your slurm_dir to be a fresh directory with no contents.".format(
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
                    "Warning: Have been waiting about {count} seconds for Slurm directories to be made, there seems to be significant delay...".format(
                        count=count
                    )
                )
            for d in dirs:
                if os.path.isdir(d) is False:
                    fail = True
                    time.sleep(1)
                    break

    def slurm_grid(self): # pragma: no cover
        """
        function to be called when running grids when grid_options['slurm']>=1

        if grid_options['slurm']==1, we set up the slurm script and launch the jobs, then return True to exit.
        if grid_options['slurm']==2, we run the stars, which means we return False to continue.
        if grid_options['slurm']==3, we are being called from the jobs to run the grids, return False to continue.

        TODO: split this function into some parts
        TODO: Comment this function better
        """

        if self.grid_options["slurm"] == 2:
            # run a grid of stars only, leaving the results
            # in the appropriate outfile
            return False

        if self.grid_options["slurm"] == 3:
            # joining : set the evolution type to "join" and return
            # False to continue
            self.grid_options["evolution_type"] = "join"
            return False

        if self.grid_options["slurm"] == 1:
            # if slurm=1,  we should have no evolution type, we
            # set up the Slurm scripts and get them evolving
            # in a Slurm array
            self.grid_options["evolution_type"] = None

            # make dirs
            self.make_slurm_dirs()

            # check we're not using too much RAM
            if datasize.DataSize(self.grid_options["slurm_memory"]) > datasize.DataSize(
                self.grid_options["slurm_warn_max_memory"]
            ):
                print(
                    "WARNING: you want to use {slurm_memory} MB of RAM : this is unlikely to be correct. If you believe it is, set slurm_warn_max_memory to something very large (it is currently {slurm_warn_max_memory} MB)\n".format(
                        slurm_memory=self.grid_options["slurm_memory"],
                        slurm_warn_max_memory=self.grid_options[
                            "slurm_warn_max_memory"
                        ],
                    )
                )
                self.exit(code=1)

            # set up slurm_array
            if not self.grid_options["slurm_array_max_jobs"]:
                self.grid_options["slurm_array_max_jobs"] = self.grid_options[
                    "slurm_njobs"
                ]
                slurm_array = self.grid_options[
                    "slurm_array"
                ] or "1-{njobs}%{max_jobs}".format(
                    njobs=self.grid_options["slurm_njobs"],
                    max_jobs=self.grid_options["slurm_array_max_jobs"],
                )

            # get job id (might be passed in)
            # TODO: is this variable used?
            jobid = (
                self.grid_options["slurm_jobid"]
                if self.grid_options["slurm_jobid"] != ""
                else "$SLURM_ARRAY_JOB_ID"
            )

            # get job array index
            jobarrayindex = self.grid_options["slurm_jobarrayindex"]
            if jobarrayindex is None:
                jobarrayindex = "$SLURM_ARRAY_TASK_ID"

            if self.grid_options["slurm_njobs"] == 0:
                print(
                    "binary_c-python Slurm : You must set grid_option slurm_njobs to be non-zero"
                )
                self.exit(code=1)

            # build the grid command
            grid_command = (
                [
                    str(self.grid_options["slurm_env"]),
                    sys.executable,
                    str(lib_programname.get_path_executed_script()),
                ]
                + sys.argv[1:]
                + [
                    "start_at=$((" + str(jobarrayindex) + "-1))",
                    "modulo=" + str(self.grid_options["slurm_njobs"]),
                    "slurm_njobs=" + str(self.grid_options["slurm_njobs"]),
                    "slurm_dir=" + self.grid_options["slurm_dir"],
                    "verbosity=" + str(self.grid_options["verbosity"]),
                    "num_cores=" + str(self.grid_options["num_processes"]),
                ]
            )

            # wrap command arguments in quotes
            grid_command = command_string_from_list(grid_command)

            # make slurm script
            scriptpath = self.slurmpath("slurm_script")
            try:
                script = self.open(scriptpath, "w", encoding="utf-8")
            except IOError:
                print(
                    "Could not open Slurm script at {path} for writing: please check you have set {slurm_dir} correctly (it is currently {slurm_dir} and can write to this directory.".format(
                        path=scriptpath, slurm_dir=self.grid_options["slurm_dir"]
                    )
                )

            slurmscript = """#!{bash}
# Slurm launch script created by binary_c-python

# Slurm options
#SBATCH --error={slurm_dir}/stderr/%A.%a
#SBATCH --output={slurm_dir}/stdout/%A.%a
#SBATCH --job-name={slurm_jobname}
#SBATCH --partition={slurm_partition}
#SBATCH --time={slurm_time}
#SBATCH --mem={slurm_memory}
#SBATCH --ntasks={slurm_ntasks}
#SBATCH --array={slurm_array}
#SBATCH --cpus-per-task={ncpus}
""".format(
                bash=self.grid_options["slurm_bash"],
                slurm_dir=self.grid_options["slurm_dir"],
                slurm_jobname=self.grid_options["slurm_jobname"],
                slurm_partition=self.grid_options["slurm_partition"],
                slurm_time=self.grid_options["slurm_time"],
                slurm_ntasks=self.grid_options["slurm_ntasks"],
                slurm_memory=self.grid_options["slurm_memory"],
                slurm_array=slurm_array,
                ncpus=self.grid_options["num_processes"],
            )

            for key in self.grid_options["slurm_extra_settings"]:
                slurmscript += "#SBATCH --{key} = {value}\n".format(
                    key=key, value=self.grid_options["slurm_extra_settings"][key]
                )

            slurmscript += """

export BINARY_C_PYTHON_ORIGINAL_CMD_LINE={cmdline}
export BINARY_C_PYTHON_ORIGINAL_WD=`{pwd}`
export BINARY_C_PYTHON_ORIGINAL_SUBMISSION_TIME=`{date}`

# set status to \"running\"
echo \"running\" > "{slurm_dir}/status/$SLURM_ARRAY_JOB_ID.$SLURM_ARRAY_TASK_ID"

# make list of files which is checked for joining
# echo "{slurm_dir}/results/$SLURM_ARRAY_JOB_ID.$SLURM_ARRAY_TASK_ID.gz" >> "{slurm_dir}/results/$SLURM_ARRAY_JOB_ID.all"

# run grid of stars and, if this returns 0, set status to finished
{grid_command} "slurm=2" "evolution_type=grid" "slurm_jobid=$SLURM_ARRAY_JOB_ID" "slurm_jobarrayindex=$SLURM_ARRAY_TASK_ID" "save_population_object={slurm_dir}/results/$SLURM_ARRAY_JOB_ID.$SLURM_ARRAY_TASK_ID.gz" && echo -n \"finished\" > "{slurm_dir}/status/$SLURM_ARRAY_JOB_ID.$SLURM_ARRAY_TASK_ID" && echo """.format(
                slurm_dir=self.grid_options["slurm_dir"],
                grid_command=grid_command,
                cmdline=repr(self.grid_options["command_line"]),
                date=self.grid_options["slurm_date"],
                pwd=self.grid_options["slurm_pwd"],
            )

            if not self.grid_options["slurm_postpone_join"]:
                slurmscript += """&& echo \"Checking if we can join...\" && echo && {grid_command} "slurm=3" "evolution_type=join" "joinlist={slurm_dir}/results/$SLURM_ARRAY_JOB_ID.all" "slurm_jobid=$SLURM_ARRAY_JOB_ID" "slurm_jobarrayindex=$SLURM_ARRAY_TASK_ID"
                """.format(
                    slurm_dir=self.grid_options["slurm_dir"],
                    grid_command=grid_command,
                )
            else:
                slurmscript += "\n"

            # write to script, close it and make it executable by
            # all (so the slurm user can pick it up)
            script.write(slurmscript)
            script.close()
            os.chmod(
                scriptpath,
                stat.S_IREAD
                | stat.S_IWRITE
                | stat.S_IEXEC
                | stat.S_IRGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IXOTH,
            )

            if not self.grid_options["slurm_postpone_sbatch"]:
                # call sbatch to launch the jobs
                cmd = [self.grid_options["slurm_sbatch"], scriptpath]

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

                if len(std_err):
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
                    "Slurm script is at {path} but has not been launched".format(
                        path=scriptpath
                    )
                )

        # some messages to the user, then return
        if self.grid_options["slurm_postpone_sbatch"] == 1:
            print(
                "Slurm script written, but launching the jobs with sbatch was postponed."
            )
        else:
            print("Slurm jobs launched")
            print("All done in slurm_grid().")

        # return True so we exit immediately
        return True

    def slurm_queue_stats(self): # pragma: no cover
        """
        Function to XXX

        TODO
        """

        return None

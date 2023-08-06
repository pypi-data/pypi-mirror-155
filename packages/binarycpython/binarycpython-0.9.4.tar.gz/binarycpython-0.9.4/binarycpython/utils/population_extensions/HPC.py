"""
Module containing the functions to HPC functionality

These functions form a single API through which you can access HPC resources.

Generally, you should call an HPC function rather than the Slurm or Condor interface
directly. The HPC function then decides which interface to use, so that all the
other modules can use a single API rather than have to choose to use the Slurm or
Condor API.

This class object is an extension to the population grid object
"""

# pylint: disable=E1101

import glob
import json
import os

from binarycpython.utils.functions import (
    now,
)

from binarycpython.utils.population_extensions.slurm import slurm
from binarycpython.utils.population_extensions.condor import condor


class HPC(condor, slurm):
    """
    Extension to the population grid object that contains functionality to handle handle the Moe & distefano distributions
    """

    def __init__(self, **kwargs):
        """
        Init function for the gridcode class
        """

        condor.__init__(self)
        slurm.__init__(self)

    def HPC_njobs(self):
        """
        Function to return the number of jobs this HPC jobs will use, as an int.
        """

        if self.grid_options["slurm"] > 0:
            n = self.grid_options["slurm_njobs"]
        elif self.grid_options["condor"] > 0:
            n = self.grid_options["condor_njobs"]
        else:
            n = None
        return int(n)

    def HPC_make_joiningfile(
        self,
        hpc_jobid=None,
        hpc_dir=None,
        n=None,
        overwrite=False,
        error_on_overwrite=False,
    ):
        """
        Function to make the joiningfile file that contains the filenames of results from each job. When all these exist, we can join.

        Note: you normally don't need to set any of the option arguments.

        Args:
            hpc_jobid : the job ID number, or self.HPC_jobID_tuple()[0] if None (default=None).
            hpc_dir : the HPC directory, or self.HPC_dir() if None (default=None).
            n : the number of jobs, or self.HPC_njobs() if None (default=None).
            overwrite : if True, overwrite an existing joiningfile (default=False)
            error_on_overwite : if True, and we try to overwrite, issue and error and exit (default=False)

        Returns:
            True if the file is made, False otherwise.

        """

        # defaults
        if hpc_dir is None:
            hpc_dir = self.HPC_dir()
        if n is None:
            n = self.HPC_njobs()
        if hpc_jobid is None:
            hpc_jobid = self.HPC_jobID_tuple()[0]

        # make path and filename
        prefix = os.path.join(hpc_dir, "results")
        file = os.path.join(prefix, hpc_jobid + ".all")

        # make the output before checking anything, we do
        # this to remove any asynchronicity
        lines = []
        for i in self.HPC_job_id_range():
            lines += [
                os.path.join(
                    prefix, "{hpc_jobid}.{i}.gz\n".format(hpc_jobid=hpc_jobid, i=i)
                )
            ]
        string = "".join(lines)

        # check the joiningfile doesn't exist
        if not overwrite and os.path.isfile(file):
            # file already exists
            print(
                "Cannot make joiningfile at {file} because it already exists, instead I am waiting for it to be unlocked.".format(
                    file=file
                )
            )
            self.wait_for_unlock(file)
            joinfiles = self.HPC_load_joinfiles_list(joinlist=file)
            print(
                "Unlocked and got {} should be {}".format(
                    len(joinfiles), self.HPC_njobs()
                )
            )
            # perhaps exit here? (e.g. for debugging)
            if error_on_overwrite:
                self.exit(code=1)
            x = False
        else:
            # open the file, but locked so we have first unique access
            (f, lock) = self.locked_open_for_write(file)

            # write to it if we are first to obtain unique access
            if lock and f:
                print("Making joiningfile list range (0,{}) at {}".format(n, file))
                f.write(string)
                f.flush()
                os.fsync(f.fileno())
                x = True
                self.locked_close(f, lock)
                os.sync()
                self.NFS_flush_hack(file)

                print(
                    "Checking joiningfile {} length (size = {})".format(
                        file, os.path.getsize(file)
                    )
                )
                joinfiles = self.HPC_load_joinfiles_list(joinlist=file)
                print("Got {} should be {}".format(len(joinfiles), self.HPC_njobs()))

            else:
                x = False
                print("Joiningfile failed to get lock: waiting for it to be unlocked")
                self.wait_for_unlock(file)
        return x

    def HPC_joinlist(self, joinlist=None):
        """
        Function to return the default HPC joinlist file.
        """

        if joinlist is None:
            joinlist = self.grid_options["joinlist"]
        return joinlist

    def HPC_load_joinfiles_list(self, joinlist=None):
        """
        Function to load in the list of files we should join, and return it.

        If grid_options['HPC_rebuild_joinlist'] is True, we rebuild it.
        """

        prefix = os.path.join(self.HPC_dir(), "results")

        if self.grid_options["HPC_rebuild_joinlist"] == 1:
            # we should rebuild the joinlist from the
            # files we find at the prefix directory
            print("Rebuild joinlist from existing files")
            joinlist = glob.glob(str(prefix) + "/*.gz")
            return joinlist

        joinlist = self.HPC_joinlist(joinlist=joinlist)
        try:
            self.wait_for_unlock(joinlist)
            f = self.open(joinlist, "r", encoding="utf-8")
            joinlist = f.read().splitlines()
            f.close()

            if False:
                print(
                    "HPC_load_joinfiles_list read joinlist {joinlist} -> gave file joinlist of length {len_joinlist} with contents {joinlist}".format(
                        joinlist=joinlist, len_joinlist=len(joinlist)
                    )
                )
        except Exception as e:
            print(
                "Failed to open joinlist at {joinlist} : {e}".format(
                    joinlist=joinlist, e=e
                )
            )
            self.exit(code=1)

        return joinlist

    def HPC_join_from_files(self, newobj, joinfiles):
        """
        Merge the results from the list joinfiles into newobj.
        """
        for file in joinfiles:
            print("Join data in", file)
            self.merge_populations_from_file(newobj, file)
        return newobj

    def HPC_can_join(self, joinfiles, joiningfile, vb=False):
        """
        Check the joinfiles to make sure they all exist
        and their .saved equivalents also exist
        """

        print("HPC check if we can join at {}".format(now()))

        if self.grid_options["HPC_force_join"] == 0 and os.path.exists(joiningfile):
            if vb:
                print(
                    "cannot join : joiningfile exists at {} (check 1)".format(
                        joiningfile
                    )
                )
            return False
        else:
            if vb:
                print("joiningfile (at {}) does not exist".format(joiningfile))

        for file in joinfiles:
            if vb:
                print("check for {}".format(file))

            if os.path.exists(file) is False:
                if vb:
                    print('cannot join : file "{}" does not exist'.format(file))
                return False

            savedfile = file + ".saved"
            if vb:
                print("check for {}".format(savedfile))

            if os.path.exists(savedfile) is False:
                if vb:
                    print(
                        'cannot join : savedfile "{}" does not exist'.format(savedfile)
                    )
                return False

            # found both files
            if vb:
                print("found {} and {}".format(file, savedfile))

        # check for joiningfile again
        if self.grid_options["HPC_force_join"] == 1:
            print("Forcing join because HPC_force_join is set")
            x = True
        elif os.path.exists(joiningfile):
            if vb:
                print(
                    "cannot join: joiningfile exists at {} (check 2)".format(
                        joiningfile
                    )
                )
            x = False
        elif vb:
            print("joiningfile at {} does not exist : can join".format(joiningfile))
            x = True

        if vb:
            print("returning {} from HPC_can_join()".format(x))

        return x

    def HPC_job(self):
        """
        Function to return True if we're running an HPC (Slurm or Condor) job, False otherwise.
        """

        return bool(self.grid_options["slurm"] > 0 or self.grid_options["condor"] > 0)

    def HPC_job_task(self):
        """
        Function to return the HPC task number, which is 1 when setting
        up and running the scripts, 2 when joining data.
        """
        if self.grid_options["slurm"] > 0:
            x = self.grid_options["slurm"]
        elif self.grid_options["condor"] > 0:
            x = self.grid_options["condor"]
        else:
            x = 0
        return x

    def HPC_job_type(self):
        """
        Function to return a string telling us the type of an HPC job, i.e.
        "slurm", "condor" or "None".
        """
        if self.grid_options["slurm"] > 0:
            hpc_type = "slurm"
        elif self.grid_options["condor"] > 0:
            hpc_type = "condor"
        else:
            hpc_type = "None"
        return hpc_type

    def HPC_jobID(self):
        """
        Function to return an HPC (Slurm or Condor) job id in the form of a string, x.y. Returns None if not an HPC job.
        """

        if self.grid_options["slurm"] > 0:
            hpc_jobid = self.slurmID()
        elif self.grid_options["condor"] > 0:
            hpc_jobid = self.condorID()
        else:
            # not an HPC job
            hpc_jobid = None

        return hpc_jobid

    def HPC_jobID_tuple(self):
        """
        Return the job ID as a tuple of ints, (x,y), or (None,None) on failure
        """

        hpc_jobid = self.HPC_jobID()

        if hpc_jobid is None or hpc_jobid.startswith("None"):
            split_hpc_jobid = [None, None]
        else:
            split_hpc_jobid = hpc_jobid.split(".")
            if not split_hpc_jobid[0]:
                split_hpc_jobid[0] = None
            if not split_hpc_jobid[1]:
                split_hpc_jobid[1] = None
        return tuple(split_hpc_jobid)

    def HPC_set_status(self, string):
        """
        Set the appropriate HPC job (Condor or Slurm) status file to whatever is given in string.

        Arguments:
                 string : the new contents of the status file
        """

        if self.grid_options["slurm"] > 0:
            self.set_slurm_status(string)
        elif self.grid_options["condor"] > 0:
            self.set_condor_status(string)
        else:
            pass

    def HPC_get_status(self, job_id=None, job_index=None, hpc_dir=None):
        """
        Get and return the appropriate HPC job (Condor or Slurm) status string for this job (or, if given, the job at id.index)

        Args:
            hpc_dir : optional HPC run directory. If not set, the default (e.g. slurm_dir or condor_dir)
                  is used.
            job_id,job_index : the id and index of the job to be queried
        """

        if self.grid_options["slurm"] > 0:
            status = self.get_slurm_status(
                jobid=job_id, jobarrayindex=job_index, slurm_dir=hpc_dir
            )
        elif self.grid_options["condor"] > 0:
            status = self.get_condor_status(
                ClusterID=job_id, Process=job_index, condor_dir=hpc_dir
            )
        else:
            status = None

        return status

    def HPC_dirs(self):
        """
        Function to return a list of directories required for this HPC job.
        """
        if self.grid_options["slurm"] > 0:
            dirs = self.slurm_dirs()
        elif self.grid_options["condor"] > 0:
            dirs = self.condor_dirs()
        else:
            dirs = []
        return dirs

    def HPC_grid(self, makejoiningfile=True): # pragma: no cover
        """
        Function to call the appropriate HPC grid function
        (e.g. Slurm or Condor) and return what it returns.

        Args:
            makejoiningfile : if True, and we're the first job with self.HPC_task() == 2, we build the joiningfile. (default=True) This option exists in case you don't want to overwrite an existing joiningfile, or want to build it in another way (e.g. in the HPC scripts).

        TODO: Exclude this function from testing for now
        TODO: Comment this function better
        """

        jobid = self.HPC_jobID_tuple()[0]

        # give some current status about the HPC run
        self.HPC_dump_status("HPC grid before")

        if makejoiningfile and self.HPC_job_task() == 2 and jobid is not None:
            self.HPC_make_joiningfile()

        if self.grid_options["slurm"] > 0:
            x = self.slurm_grid()
        elif self.grid_options["condor"] > 0:
            x = self.condor_grid()
        else:
            x = None  # should not happen

        # give some current status about the HPC run
        self.HPC_dump_status("HPC grid after")

        return x

    def HPC_check_requirements(self):
        """
        Function to check HPC option requirements have been met. Returns a tuple: (True,"") if all is ok, (False,<warning string>) otherwise.
        """
        if self.grid_options["slurm"] > 0:
            t = self.slurm_check_requirements()
        elif self.grid_options["condor"] > 0:
            t = self.condor_check_requirements()
        else:
            t = (True, "")
        return t

    def HPC_id_filename(self):
        """
        HPC jobs have a filename in their directory which specifies the job id. This function returns the contents of that file as a string, or None on failure.
        """

        if self.grid_options["slurm"] > 0:
            filename = "jobid"
        elif self.grid_options["condor"] > 0:
            filename = "ClusterID"
        else:
            filename = None
        return filename

    def HPC_id_from_dir(self, hpc_dir):
        """
        Function to return the ID of an HPC run given its (already existing) directory.
        """

        filename = self.HPC_id_filename()
        if not filename:
            return None

        file = os.path.join(hpc_dir, filename)
        f = self.open(file, "r", encoding="utf-8")
        if not f:
            print(
                "Error: could not open {file} to read the HPC jobid of the directory {hpc_dir}".format(
                    file=file, hpc_dir=hpc_dir
                )
            )
            self.exit(code=1)

        oldjobid = f.read().strip()
        if not oldjobid:
            print("Error: could not find jobid in {hpc_dir}".format(hpc_dir=hpc_dir))
            self.exit(code=1)
        else:
            f.close()
            return oldjobid

    def HPC_restore(self):
        """
        Set grid_options['restore_from_snapshot_file'] so that we restore data from existing
        an HPC run if self.grid_options[hpc_job_type+'_restart_dir'], where hpc_job_type is "slurm" or "condor",
        is provided, otherwise do nothing. This only works if grid_options[hpc_job_type] == self.HPC_job_task() == 2, which is
        the run-grid stage of the process.
        """

        hpc_job_type = self.HPC_job_type()
        if hpc_job_type is None:
            return

        key = hpc_job_type + "_restart_dir"
        if key not in self.grid_options:
            return

        # get restart directory
        hpc_dir = self.grid_options[hpc_job_type + "_restart_dir"]
        if hpc_dir is None:
            return

        # get HPC job index
        index = self.HPC_jobID_tuple()[1]
        if index is None:
            return

        if self.HPC_job_task() == 2:  # (same as) self.grid_options[hpc_job_type] == 2:
            old_id = self.HPC_id_from_dir(hpc_dir)
            print(
                "Restart from hpc_dir {hpc_dir} which was has (old) ID {old_id}, we are job index {index}".format(
                    hpc_dir=hpc_dir, old_id=old_id, index=index
                )
            )

            # check status: if "finished", we don't have to do anything
            status = self.HPC_get_status(hpc_dir=hpc_dir)

            if status == "finished":
                print("Status is finished, cannot and do not need to restart.")
                self.exit(code=0)

            file = os.path.join(
                dir, "snapshots", "{id}.{index}.gz".format(id=old_id, index=index)
            )

            if os.path.exists(file):
                # have data from which we can restore, set it in
                # the appropriate grid option
                print("Restore this run from snapshot {file}".format(file=file))
                self.grid_options["restore_from_snapshot_file"] = file
            else:
                # no snapshot: so no need to restore, just exit
                print(
                    "Expected snapshot at {file} but none was found".format(file=file)
                )
                self.exit(code=0)
        return

    def HPC_join_previous(self):
        """
        Function to join previously generated datasets.
        """
        # check that our job has finished
        status = self.HPC_get_status()
        print("Job status", status)

        if self.grid_options["HPC_force_join"] == 0 and status != "finished":
            # job did not finish : save a snapshot
            print(
                "This job did not finish (status is {status}) : cannot join".format(
                    status=status
                )
            )
        else:
            # our job has finished
            HPC_status = self.HPC_status()

            # HPC_queue_stats = self.HPC_queue_stats()

            if HPC_status["status"]["finished"] != HPC_status["njobs"]:
                print(
                    "HPC_status reports {} finished jobs out of {}. We cannot join because not all the jobs are finished. Exiting.".format(
                        HPC_status["status"]["finished"], HPC_status["njobs"]
                    )
                )
                self.exit(1)

            joinfiles = self.HPC_load_joinfiles_list()
            joiningfile = self.HPC_path("joining")
            print(
                "Joinfile list n={n} (should be {m})".format(
                    n=len(joinfiles), m=self.HPC_njobs()
                )
            )
            print("Joingingfile path : ", joiningfile)

            if len(joinfiles) != self.HPC_njobs():
                print("Number of joinfiles != njobs : this is wrong, exiting.")
                self.exit(1)

            if self.HPC_can_join(joinfiles, joiningfile, vb=True):
                # join object files
                print("We can join")
                try:
                    # touch joiningfile
                    if self.grid_options["HPC_force_join"] == 0:
                        print("Making joiningfile at {}".format(joiningfile))
                        self.HPC_touch(joiningfile)
                    try:
                        print("Calling HPC_join_from_files()")
                        self.HPC_join_from_files(self, joinfiles)
                    except Exception as e:
                        print("Join gave exception", e)
                        # disable analytics calculations : use the
                        # values we just loaded
                    self.grid_options["do_analytics"] = False
                    return
                except Exception as e:
                    print("pass {}", e)
                    pass
            else:
                print("cannot join : other tasks are not yet finished\n")
                print("Finished this job : exiting")
        self.exit(code=1)

    def HPC_path(self, path):
        """
        Function to file the filename of this HPC job's file at path.
        """
        if self.grid_options["slurm"] > 0:
            p = self.slurmpath(path)
        elif self.grid_options["condor"] > 0:
            p = self.condorpath(path)
        else:
            p = None
        return p

    def HPC_snapshot_filename(self):
        """
        Function to return an HPC job's snapshot filename.
        """
        if self.HPC_job():
            file = os.path.join(self.HPC_dir, "snapshots", self.HPC_jobID() + ".gz")
        else:
            file = None
        return file

    def HPC_dir(self):
        """
        Function to return an HPC job's directory.
        """
        if self.grid_options["slurm"] > 0:
            d = self.grid_options["slurm_dir"]
        elif self.grid_options["condor"] > 0:
            d = self.grid_options["condor_dir"]
        else:
            d = None
        return d

    def HPC_touch(self, filename, string=None):
        """
        Function to touch the file at filename, put into it the job number
        and (if given) the string passed in.
        """

        try:
            f = self.open(filename, "w", encoding="utf-8")

            if f:
                job = self.HPC_jobID()
                jobtype = self.HPC_job_type()
                if job:
                    s = str(job)
                    if jobtype:
                        s += " " + str(jobtype)
                    f.write(s + "\n")
                if string:
                    f.write(string)
                f.flush()
                f.close()

            self.NFS_flush_hack(filename)
        except:
            pass

    def HPC_status(self):
        """
        Return a dict of useful information about the current status
        of this HPC run.
        """
        d = {}  # returned
        _id, _index = self.HPC_jobID_tuple()
        d["job_id"] = _id
        d["job_index"] = _index
        if _id and _index:
            n = self.HPC_njobs()
            d["njobs"] = n
            d["job_task"] = self.HPC_job_task()
            d["job_type"] = self.HPC_job_type()
            d["job_status"] = self.HPC_get_status()
            d["dir"] = self.HPC_dir()
            d["dirs"] = self.HPC_dirs()

            # get fellow jobs' status
            d["status"] = {}
            d["joblist"] = {}

            # default types
            for x in ["running", "starting", "finishing", "finished", "killed"]:
                d["status"][x] = 0
                d["joblist"][x] = []

            for i in self.HPC_job_id_range():
                s = self.HPC_get_status(job_id=_id, job_index=i)
                #print("HPC get job",_id,':',i," status=",s)
                if s is None:
                    s = "unknown"
                if not s in d["status"]:
                    d["status"][s] = 1
                else:
                    d["status"][s] += 1
                if not s in d["joblist"]:
                    d["joblist"][s] = [str(_id) + "." + str(i)]
                else:
                    d["joblist"][s] += [str(_id) + "." + str(i)]

        return d

    def HPC_dump_status(self, string=None):
        """
        Function to print the status of the HPC grid
        """

        if not string:
            string = ""

        d = self.HPC_status()

        print("############################################################")
        print("HPC job status " + string)
        print(json.dumps(d, indent=4))
        print("############################################################")

    def HPC_queue_stats(self): # pragma: no cover
        """
        Function that returns the queue stats for the HPC grid
        """

        if self.grid_options["slurm"] > 0:
            x = self.slurm_queue_stats()
        elif self.grid_options["condor"] > 0:
            x = self.condor_queue_stats()
        else:
            x = None

        return x

    def HPC_job_id_range(self):
        n = self.HPC_njobs()
        if self.grid_options["slurm"] > 0:
            return range(1, n+1)
        elif self.grid_options["condor"] > 0:
            return range(0, n)
        else:
            print("Called HPC_job_id_range when not running an HPC grid : you cannot do this.")
            raise

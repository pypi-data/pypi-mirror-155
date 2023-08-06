"""
File containing the class extension for the population object that contains data input-output (IO) functions
"""

# pylint: disable=E1101

import os
import bz2
import gzip
import copy
import json
import time
import datetime
import subprocess
from typing import Union

import msgpack
import flufl.lock
import compress_pickle

from binarycpython.utils.ensemble import ensemble_file_type, ensemble_compression
from binarycpython.utils.dicts import (
    merge_dicts,
)
from binarycpython.utils.functions import (
    verbose_print,
    now,
)


class dataIO:
    """
    Class extension for the population object that contains data input-output (IO) functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def dir_ok(self, directory):
        """
        Function to test if we can read and write to a directory that must exist. Return True if all is ok, False otherwise.
        """

        return os.access(directory, os.F_OK) and os.access(directory, os.R_OK | os.W_OK)

    def save_population_object(
        self,
        population_object=None,
        filename=None,
        confirmation=True,
        compression="gzip",
    ):
        """
        Save pickled Population object to file at filename or, if filename is None, whatever is set at self.grid_options['save_population_object']

        Args:
            population_object : the object to be saved to the file. If population_object is None, use self.
            filename : the name of the file to be saved. If not set, use self.grid_options['save_population_object']
            confirmation : if True, a file "filename.saved" is touched just after the dump, so we know it is finished. TODO: fix this
            compression (optional, default = "gzip"): TODO: fix this

        Compression is performed according to the filename, as stated in the
        compress_pickle documentation at
        https://lucianopaz.github.io/compress_pickle/html/

        Shared memory, stored in the population_object.shared_memory dict, is not saved.
        """

        if population_object is None:
            # default to using self
            population_object = self

        if filename is None:
            # get filename from self
            filename = self.grid_options["save_population_object"]

        if filename:
            print(
                "Save population {id}, probtot {probtot} to pickle in {filename}".format(
                    id=self.grid_options["_population_id"],
                    probtot=population_object.grid_options["_probtot"],
                    filename=filename,
                )
            )

            # Some parts of the population_object cannot be pickled:
            # remove them, and restore them after pickling

            # remove shared memory
            shared_memory = population_object.shared_memory
            population_object.shared_memory = None

            # delete system generator
            system_generator = population_object.grid_options["_system_generator"]
            population_object.grid_options["_system_generator"] = None

            # delete _store_memaddr
            _store_memaddr = population_object.grid_options["_store_memaddr"]
            population_object.grid_options["_store_memaddr"] = None

            # delete persistent_data_memory_dict
            persistent_data_memory_dict = population_object.persistent_data_memory_dict
            population_object.persistent_data_memory_dict = None

            # add metadata if it doesn't exist
            if not "metadata" in population_object.grid_ensemble_results:
                population_object.grid_ensemble_results["metadata"] = {}

            # add datestamp
            population_object.grid_ensemble_results["metadata"][
                "save_population_time"
            ] = now()

            # add extra metadata
            population_object.add_system_metadata()

            # add max memory use
            try:
                self.grid_ensemble_results["metadata"][
                    "max_memory_use"
                ] = copy.deepcopy(sum(shared_memory["max_memory_use_per_thread"]))
            except Exception as e:
                print("save_population_object : Error: ", e)
                raise Exception(e) from e

            # dump pickle file
            compress_pickle.dump(population_object, filename, pickler_method="dill")

            # restore data
            population_object.shared_memory = shared_memory
            population_object.grid_options["_system_generator"] = system_generator
            del population_object.grid_ensemble_results["metadata"][
                "save_population_time"
            ]
            population_object.grid_options["store_memaddr"] = _store_memaddr
            population_object.persistent_data_memory_dict = persistent_data_memory_dict

            self.NFS_flush_hack(filename)

            # touch 'saved' file
            saved = filename + ".saved"
            self.HPC_touch(saved)

    def load_population_object(self, filename):
        """
        returns the Population object loaded from filename
        """

        self.NFS_flush_hack(filename)
        if filename is None:
            obj = None
        else:
            try:
                obj = compress_pickle.load(filename, pickler_method="dill")
            except Exception as e:
                obj = None
                print("Loading of the compressed object went wrong: {}".format(e))
        return obj

    def merge_populations(self, refpop, newpop):
        """
        merge newpop's results data into refpop's results data

        Args:
            refpop : the original "reference" Population object to be added to
            newpop : Population object containing the new data

        Returns:
            nothing

        Note:
            The file should be saved using save_population_object()
        """
        
        # combine data
        refpop.grid_results = merge_dicts(refpop.grid_results,
                                          newpop.grid_results)
        
        # special cases
        maxmem = 0
        if "max_memory_use" in refpop.grid_ensemble_results.get(
            "metadata", {}
        ) and "max_memory_use" in newpop.grid_ensemble_results.get("metadata", {}):
            maxmem = max(
                refpop.grid_ensemble_results["metadata"]["max_memory_use"],
                newpop.grid_ensemble_results["metadata"]["max_memory_use"],
            )

        try:
            # special cases:
            # copy the settings
            settings = None
            if "settings" in newpop.grid_ensemble_results.get("metadata", {}):
                settings = copy.deepcopy(
                    newpop.grid_ensemble_results["metadata"]["settings"]
                )
            if settings:
                refpop.grid_ensemble_results["metadata"]["settings"] = settings

            # Copy the Xinit
            Xinit = None
            if "Xinit" in newpop.grid_ensemble_results.get("ensemble", {}):
                Xinit = copy.deepcopy(newpop.grid_ensemble_results["ensemble"]["Xinit"])
            if Xinit:
                refpop.grid_ensemble_results["ensemble"]["Xinit"] = Xinit

            # merge the ensemble dicts
            refpop.grid_ensemble_results = merge_dicts(
                refpop.grid_ensemble_results,
                newpop.grid_ensemble_results
            )

            # set special cases
            refpop.grid_ensemble_results["metadata"]["max_memory_use"] = maxmem

        except Exception as e:
            print("Error merging grid_ensemble_results:", e)
            raise Exception(e) from e

        for key in ["_probtot"]:
            refpop.grid_options[key] += newpop.grid_options[key]

        refpop.grid_options["_killed"] |= newpop.grid_options["_killed"]

    def merge_populations_from_file(self, refpop, filename):
        """
         Wrapper for merge_populations so it can be done directly
         from a file.

        Args:
            refpop : the original "reference" Population object to be added to
            filename : file containing the Population object containing the new data

        Note:
            The file should be saved using save_population_object()
        """

        mtime = time.localtime(os.path.getmtime(filename))
        modtime = time.strftime("%a, %d %b %Y %H:%M:%S", mtime)
        print(
            "Load data from {filename} : size {size}, modtime {modtime}".format(
                filename=filename,
                size=os.path.getsize(filename),
                modtime=modtime,
            )
        )

        newpop = self.load_population_object(filename)

        if "total_count" in newpop.grid_options:
            n = newpop.grid_options["total_count"]
        elif "_count" in newpop.grid_options:
            n = newpop.grid_options["_count"]
        elif (
            "metadata" in newpop.grid_ensemble_results
            and "_count" in newpop.grid_ensemble_results["metadata"]
        ):
            n = newpop.grid_ensemble_results["metadata"]["_count"]
        else:
            n = -1
        
        print("Loaded data from {n} stars".format(n=n))
        
        # merge with refpop
        self.merge_populations(refpop, newpop)

    def snapshot_filename(self):
        """
        Automatically choose the snapshot filename.
        """
        if self.HPC_job():
            return self.HPC_snapshot_filename()

        file = os.path.join(self.grid_options["tmp_dir"], "snapshot.gz")
        return file

    def load_snapshot(self, file):
        """
        Load a snapshot from file and set it in the preloaded_population placeholder.
        """
        newpop = self.load_population_object(file)

        # unset the _killed flag, in case it was set
        newpop.grid_options["_killed"] = False

        # set in preloaded_population for later  merge
        self.preloaded_population = newpop

        # set the start position for new stars
        self.grid_options["start_at"] = newpop.grid_options["start_at"]

        print(
            "Loaded from snapshot at {file} : {nstars} stars, start at star {nstart}".format(
                file=file,
                nstars=0,  # self.grid_options[''],
                nstart=self.grid_options["start_at"],
            )
        )
        return

    def save_snapshot(self, file=None):
        """
        Save the population object to a snapshot file, automatically choosing the filename if none is given.
        """
        if file is None:
            file = self.snapshot_filename()

        if "_count" in self.grid_options:
            n = self.grid_options["_count"]
        else:
            n = "?"

        print("Saving snapshot containing {} stars to {}".format(n, file))
        self.save_population_object(object=self, filename=file)

    def write_ensemble(
        self,
        output_file,
        data=None,
        sort_keys=True,
        indent=4,
        encoding="utf-8",
        ensure_ascii=False,
    ):
        """
            write_ensemble : Write ensemble results to a file.

        Args:
            output_file : the output filename.

                          If the filename has an extension that we recognise,
                          e.g. .gz or .bz2, we compress the output appropriately.

                          The filename should contain .json or .msgpack, the two
                          currently-supported formats.

                          Usually you'll want to output to JSON, but we can
                          also output to msgpack.

            data :   the data dictionary to be converted and written to the file.
                     If not set, this defaults to self.grid_ensemble_results.

            sort_keys : if True, and output is to JSON, the keys will be sorted.
                        (default: True, passed to json.dumps)

            indent : number of space characters used in the JSON indent. (Default: 4,
                     passed to json.dumps)

            encoding : file encoding method, usually defaults to 'utf-8'

            ensure_ascii : the ensure_ascii flag passed to json.dump and/or json.dumps
                           (Default: False)
        """

        # get the file type
        file_type = ensemble_file_type(output_file)

        # default to using grid_ensemble_results if no data is given
        if data is None:
            data = self.grid_ensemble_results

        if not file_type:
            print(
                "Unable to determine file type from ensemble filename {} : it should be .json or .msgpack.".format(
                    output_file
                )
            )
            self.exit(code=1)
        else:
            if file_type == "JSON":
                f = self.open(output_file, "wt", encoding=encoding)
                # JSON output
                f.write(
                    json.dumps(
                        data,
                        sort_keys=sort_keys,
                        indent=indent,
                        ensure_ascii=ensure_ascii,
                    )
                )
            elif file_type == "msgpack":
                f = self.open(
                    output_file, "w"
                )  # TODO: i think something is going wrong here. not sure but doing msgpack and .gz e.g gives an error about str input rather than bytes. i think this is because the self.open does not take into account that the msgpack stream requires different properties.

                # msgpack output
                msgpack.dump(data, f)

            f.close()

        print(
            "Thread {thread}: Wrote ensemble results to file: {colour}{file}{reset} (file type {file_type})".format(
                thread=self.process_ID,
                file=output_file,
                colour=self.ANSI_colours["green"],
                reset=self.ANSI_colours["reset"],
                file_type=file_type,
            )
        )

    def write_binary_c_calls_to_file(
        self,
        output_dir: Union[str, None] = None,
        output_filename: Union[str, None] = None,
        include_defaults: bool = False,
        encoding="utf-8",
    ) -> None:
        """
        Function that loops over the grid code and writes the generated parameters to a file.
        In the form of a command line call

        Only useful when you have a variable grid as system_generator. MC wouldn't be that useful

        Also, make sure that in this export there are the basic parameters
        like m1,m2,sep, orb-per, ecc, probability etc.

        On default this will write to the datadir, if it exists

        Args:
            output_dir: (optional, default = None) directory where to write the file to. If custom_options['data_dir'] is present, then that one will be used first, and then the output_dir
            output_filename: (optional, default = None) filename of the output. If not set it will be called "binary_c_calls.txt"
            include_defaults: (optional, default = None) whether to include the defaults of binary_c in the lines that are written. Beware that this will result in very long lines, and it might be better to just export the binary_c defaults and keep them in a separate file.

        Returns:
            filename: filename that was used to write the calls to
        """

        # Check if there is no compiled grid yet. If not, lets try to build it first.
        if not self.grid_options["_system_generator"]:

            ## check the settings:
            if self.bse_options.get("ensemble", None):
                if self.bse_options["ensemble"] == 1:
                    if not self.bse_options.get("ensemble_defer", 0) == 1:
                        verbose_print(
                            "Error, if you want to run an ensemble in a population, the output needs to be deferred",
                            self.grid_options["verbosity"],
                            0,
                        )
                        raise ValueError

            # Put in check
            if len(self.grid_options["_grid_variables"]) == 0:
                print("Error: you haven't defined any grid variables! Aborting")
                raise ValueError

            #
            self._generate_grid_code(dry_run=False)

            #
            self._load_grid_function()

        # then if the _system_generator is present, we go through it
        if self.grid_options["_system_generator"]:
            # Check if there is an output dir configured
            if self.custom_options.get("data_dir", None):
                binary_c_calls_output_dir = self.custom_options["data_dir"]
                # otherwise check if there's one passed to the function
            else:
                if not output_dir:
                    print(
                        "Error. No data_dir configured and you gave no output_dir. Aborting"
                    )
                    raise ValueError
                binary_c_calls_output_dir = output_dir

            # check if there's a filename passed to the function
            if output_filename:
                binary_c_calls_filename = output_filename
                # otherwise use default value
            else:
                binary_c_calls_filename = "binary_c_calls.txt"

            binary_c_calls_full_filename = os.path.join(
                binary_c_calls_output_dir, binary_c_calls_filename
            )
            print("Writing binary_c calls to {}".format(binary_c_calls_full_filename))

            # Write to file
            with self.open(
                binary_c_calls_full_filename, "w", encoding=encoding
            ) as file:
                # Get defaults and clean them, then overwrite them with the set values.
                if include_defaults:
                    # TODO: make sure that the defaults here are cleaned up properly
                    cleaned_up_defaults = self.cleaned_up_defaults
                    full_system_dict = cleaned_up_defaults.copy()
                    full_system_dict.update(self.bse_options.copy())
                else:
                    full_system_dict = self.bse_options.copy()

                for system in self.grid_options["_system_generator"](self):
                    # update values with current system values
                    full_system_dict.update(system)

                    binary_cmdline_string = self._return_argline(full_system_dict)
                    file.write(binary_cmdline_string + "\n")
        else:
            print("Error. No grid function found!")
            raise ValueError

        return binary_c_calls_full_filename

    def set_status(self, string, format_statment="process_{}.txt", ID=None):
        """
        Function to set the status string in its appropriate file
        """

        if ID is None:
            ID = self.process_ID

        if self.grid_options["status_dir"]:
            path = os.path.join(
                self.grid_options["status_dir"],
                format_statment.format(ID),
            )
            with self.open(path, "w", encoding="utf-8") as f:
                f.write(string)
                f.close()
                self.NFS_flush_hack(path)

        # custom logging functions for HPC jobs
        if self.HPC_job():
            self.HPC_set_status(string)

    def locked_close(self, file, lock):
        """
        Partner function to locked_open_for_write()

        Closes and unlocks the file
        """
        if file:
            file.close()
        if lock:
            lock.unlock()
        if file:
            self.NFS_flush_hack(file.name)

    def wait_for_unlock(self, filename, lock_suffix=".lock"):
        """
        Companion to locked_open_for_write that waits for a filename
        to a) exist and b) be unlocked.

        This should work because the lock file is created before the file
        is created.
        """
        while not os.path.isfile(filename):
            time.sleep(0.25)
        while os.path.isfile(filename + lock_suffix):
            time.sleep(0.25)

    def locked_open_for_write(
        self,
        filename,
        encoding="utf-8",
        lock_suffix=".lock",
        lock_timeout=5,
        lock_lifetime=60,
        exists_ok=False,
        fatal_open_errors=True,
        vb=False,
        **kwargs,
    ):
        """
        Wrapper for Python's open(filename) which opens a file at
        filename for writing (mode "w") and locks it.

        We check whether the file's lockfile already exists, in which
        case just return (None,None), and if we cannot obtain a
        lock on the file we also return (None,None).

        If the file does not exist, we keep trying to lock until it does.

        To do the locking, we use flufl.lock which is NFS safe.

        Args:
            lock_lifetime: (passed to flufl.lock.Lock()) default 60 seconds.
                           It should take less than this time to write the file.
            lock_timeout: (passed to flufl.lock.Lock()) default 5 seconds.
                          This should be non-zero.
            fatal_open_errors: if open() fails and fatal_open_errors is True, exit.
            exists_ok: if False and the file at filename exists, return (None,None) (default False)
            vb: verbose logging if True, defaults to False

        Returns:
            (file_object, lock_object) tuple.
            If the file was not opened, returns (None,None).
        """

        if exists_ok is False and os.path.isfile(filename):
            if vb:
                print("File at {} already exists: cannot write to it".format(filename))
            return (None, None)

        # set the lockfile path: this should be the same
        # for all processes, so it's just the original file
        # plus the lock_suffix
        lockfilename = filename + lock_suffix
        if vb:
            print("lockfile={}".format(lockfilename))

        while True:
            # if the file exists, just return
            if os.path.isfile(lockfilename):
                if vb:
                    print(
                        "lockfile at {} already exists (corresponding to file at {})".format(
                            lockfilename, filename
                        )
                    )
                return (None, None)

            # make the lock object by opening the lockfile
            lock = flufl.lock.Lock(lockfilename, default_timeout=lock_timeout)
            if vb:
                print("post-lock: {}".format(lock))

            if lock:
                # we have the lockfile, so set the lifetime and try to lock it
                lock.lifetime = datetime.timedelta(seconds=lock_lifetime)
                try:
                    if vb:
                        print("try to lock {}".format(lock))
                    lock.lock()
                    if vb:
                        if lock.is_locked:
                            print("locked {}".format(lock))
                        else:
                            print("failed to lock {}".format(lock))
                except:
                    pass

                # if we acquired the lock, try to open the file
                if lock.is_locked:
                    if vb:
                        print(
                            "{} is locked by {} to {}".format(
                                filename, lock, lockfilename
                            )
                        )

                    if exists_ok is False and os.path.isfile(filename):
                        if vb:
                            print(
                                "File at {} already exists (2): cannot write to it, unlocking and returning (None,None)".format(
                                    filename
                                )
                            )
                        lock.unlock()
                        return (None, None)

                    # All is apparently ok: file is locked
                    try:
                        if vb:
                            print("Try to open file at {}".format(filename))
                        f = self.open(filename, mode="w", encoding=encoding, **kwargs)
                        if vb:
                            print("Return locked file {}, {}".format(f, lock))
                        return (f, lock)

                    # error on open should be fatal
                    except Exception as e:
                        print("Error in locked_open_for_write() : {}".format(e))
                        if fatal_open_errors:
                            if vb:
                                print("fatal exit on open")
                            self.exit(1)
                        else:
                            if vb:
                                print("unlock {}".format(lock))
                            lock.unlock()
                            if vb:
                                print("unlocked {} return None,None".format(lock))
                            return (None, None)

            # failed to lock this time, keep trying
            # (we shouldn't lock up the CPU because the timeout is non-zero)
            continue

    def NFS_flush_hack(self, filename):
        """
        Use opendir()/closedir() to flush NFS access to a file.

        NOTE: this may or may not work!

        TODO: This function leads to a complaint about unclosed scandir operators. Check if that can be resolved.
        """
        os.sync()
        dirname = os.path.dirname(filename)

        for _ in os.scandir(dirname):
            pass

    def compression_type(self, filename):
        """
        Return the compression type of the ensemble file, based on its filename extension.
        """

        if filename.endswith(".bz2"):
            return "bzip2"
        if filename.endswith(".gz"):
            return "gzip"

        return None

    def open(
        self,
        file,
        mode="r",
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
        compression=None,
        compresslevel=None,
        vb=False,
    ):
        """
        Wrapper for open() with automatic compression based on the file extension.
        """

        if compression is None:
            compression = self.compression_type(file)

        if vb:
            print(
                'open() file at "{file}" with mode = {mode}, compression {compression}, compresslevel {compresslevel}'.format(
                    file=file,
                    compression=compression,
                    compresslevel=compresslevel,
                    mode=mode,
                )
            )

        if compression:
            if compresslevel is None:
                compresslevel = 9
            if "b" not in mode:
                # if we don't specify binary-mode, the gzip module
                # defaults to binary, which isn't compatible with JSON,
                # so default to text if not specified otherwise
                mode += "t"
                if vb:
                    print("open() adding text mode")
            else:
                encoding = None
                errors = None
                newline = None
                if vb:
                    print("open() setting encoding=errors=newline=None")
            if compression == "bzip2":
                file_object = bz2.open(
                    file,
                    mode=mode,
                    compresslevel=compresslevel,
                    encoding=encoding,
                    errors=errors,
                    newline=newline,
                )
            elif compression == "gzip":
                file_object = gzip.open(
                    file,
                    mode=mode,
                    compresslevel=compresslevel,
                    encoding=encoding,
                    errors=errors,
                    newline=newline,
                )
        else:
            file_object = open(
                file,
                mode=mode,
                buffering=buffering,
                encoding=encoding,
                errors=errors,
                newline=newline,
                closefd=closefd,
                opener=opener,
            )

        if vb:
            print("open() return file_object =", file_object)
        return file_object

    def NFSpath(self, path):
        """
        Test path to see if it's on an NFS mount.

        Args:
            path : the path to be tested

        Returns:
            True : if on an NFS mount point.
            False : if not.
            None : if the path does not exist.
        """

        if os.path.exists(path):
            cmd = 'stat -f -L -c %T "' + path + '"'
            return (
                "nfs"
                in subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                .stdout.read()
                .decode()
            )

        return None

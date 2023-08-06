"""
Unittests for slurm module

TODO: slurmpath
TODO: slurm_status_file
TODO: slurm_grid
TODO: slurm_queue_stats
"""

import os
import shutil
import unittest
from binarycpython.utils.functions import Capturing, temp_dir
from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test_slurm")
shutil.rmtree(TMP_DIR)
os.makedirs(TMP_DIR, exist_ok=True)


class test_slurmID(unittest.TestCase):
    """
    Unittests for function slurmID
    """

    def test_slurmID(self):
        with Capturing() as output:
            self._test_slurmID()

    def _test_slurmID(self):
        """
        Unit test for slurmID for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5

        self.assertEqual(
            slurm_pop.HPC_jobID(),
            "{jobid}.{jobarrayindex}".format(jobid=4, jobarrayindex=5),
        )


class test_slurm_dirs(unittest.TestCase):
    """
    Unittests for function slurm_dirs
    """

    def test_slurm_dirs(self):
        with Capturing() as output:
            self._test_slurm_dirs()

    def _test_slurm_dirs(self):
        """
        Unit test for slurm_dirs for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        self.assertEqual(slurm_pop.slurm_dirs(), ["slurm_dir"])


class test_slurm_check_requirements(unittest.TestCase):
    """
    Unittests for function slurm_check_requirements
    """

    def test_slurm_check_requirements(self):
        with Capturing() as output:
            self._test_slurm_check_requirements()

    def _test_slurm_check_requirements(self):
        """
        Unit test for slurm_check_requirements for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1

        # First the False test
        result_1 = slurm_pop.slurm_check_requirements()
        self.assertFalse(result_1[0])
        self.assertTrue(len(result_1[1]) > 0)

        # First the True test
        slurm_pop.grid_options["slurm_dir"] = TMP_DIR
        result_2 = slurm_pop.slurm_check_requirements()
        self.assertTrue(result_2[0])
        self.assertTrue(len(result_2[1]) == 0)


class test_set_slurm_status(unittest.TestCase):
    """
    Unittests for function set_slurm_status
    """

    def test_set_slurm_status(self):
        with Capturing() as output:
            self._test_set_slurm_status()

    def _test_set_slurm_status(self):
        """
        Unit test for set_slurm_status for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5
        slurm_pop.grid_options["slurm_dir"] = TMP_DIR

        id_filename = os.path.isfile(
            os.path.join(slurm_pop.grid_options["slurm_dir"], "jobid")
        )
        if os.path.isfile(id_filename):
            os.remove(id_filename)

        #
        os.makedirs(
            os.path.dirname(
                slurm_pop.slurm_status_file(
                    slurm_dir=slurm_pop.grid_options["slurm_dir"]
                )
            ),
            exist_ok=True,
        )
        slurm_pop.set_slurm_status("test_set_slurm_status")

        # Check if ID file exists
        self.assertTrue(os.path.exists(id_filename))

        # Check if status file exists
        self.assertTrue(
            os.path.isfile(
                slurm_pop.slurm_status_file(
                    slurm_dir=slurm_pop.grid_options["slurm_dir"]
                )
            )
        )

        with open(
            slurm_pop.slurm_status_file(slurm_dir=slurm_pop.grid_options["slurm_dir"]),
            "r",
        ) as f:
            content_file = f.read()
        self.assertTrue(content_file == "test_set_slurm_status")


class test_get_slurm_status(unittest.TestCase):
    """
    Unittests for function get_slurm_status
    """

    def test_get_slurm_status(self):
        with Capturing() as output:
            self._test_get_slurm_status()

    def _test_get_slurm_status(self):
        """
        Unit test for get_slurm_status for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5
        slurm_pop.grid_options["slurm_dir"] = TMP_DIR

        #
        os.makedirs(
            os.path.dirname(
                slurm_pop.slurm_status_file(
                    slurm_dir=slurm_pop.grid_options["slurm_dir"]
                )
            ),
            exist_ok=True,
        )
        slurm_pop.set_slurm_status("test_set_slurm_status")

        status = slurm_pop.get_slurm_status()
        self.assertEqual(status, "test_set_slurm_status")


class test_slurm_outfile(unittest.TestCase):
    """
    Unittests for function slurm_outfile
    """

    def test_slurm_outfile(self):
        with Capturing() as output:
            self._test_slurm_outfile()

    def _test_slurm_outfile(self):
        """
        Unit test for slurm_outfile for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5
        slurm_pop.grid_options["slurm_dir"] = TMP_DIR

        outfile = slurm_pop.slurm_outfile()
        slurm_id = slurm_pop.slurmID()
        self.assertEqual(outfile, os.path.abspath(os.path.join(slurm_pop.grid_options["slurm_dir"], "results", "{}.gz".format(slurm_id))))


class test_make_slurm_dirs(unittest.TestCase):
    """
    Unittests for function slurm_outfile
    """

    def test_make_slurm_dirs(self):
        with Capturing() as output:
            self._test_make_slurm_dirs()

    def _test_make_slurm_dirs(self):
        """
        Unit test for slurm_outfile for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5
        slurm_pop.grid_options["slurm_dir"] = TMP_DIR

        shutil.rmtree(TMP_DIR)
        os.makedirs(TMP_DIR)

        #
        slurm_pop.make_slurm_dirs()

        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "stdout")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "stderr")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "results")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "status")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "snapshots")))

if __name__ == "__main__":
    unittest.main()

"""
Unit classes for the _condor module population extension

TODO: condorpath
TODO: condor_status_file
TODO: condor_grid
TODO: condor_queue_stats
"""

import os
import shutil
import unittest
from binarycpython.utils.functions import Capturing, temp_dir
from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test_condor")
shutil.rmtree(TMP_DIR)
os.makedirs(TMP_DIR, exist_ok=True)


class test_condorID(unittest.TestCase):
    """
    Unittests for function HPC_jobID
    """

    def test_condorID(self):
        with Capturing() as output:
            self._test_condorID()

    def _test_condorID(self):
        """
        Unit test for condorID for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3

        self.assertEqual(
            condor_pop.condorID(),
            "{ClusterID}.{Process}".format(ClusterID=2, Process=3),
        )


class test_condor_dirs(unittest.TestCase):
    """
    Unittests for function condor_dirs
    """

    def test_condor_dirs(self):
        with Capturing() as output:
            self._test_condor_dirs()

    def _test_condor_dirs(self):
        """
        Unit test for condor_dirs for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        self.assertEqual(condor_pop.condor_dirs(), ["condor_dir"])


class test_condor_check_requirements(unittest.TestCase):
    """
    Unittests for function condor_check_requirements
    """

    def test_condor_check_requirements(self):
        with Capturing() as output:
            self._test_condor_check_requirements()

    def _test_condor_check_requirements(self):
        """
        Unit test for condor_check_requirements for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1

        # First the False test
        result_1 = condor_pop.condor_check_requirements()
        self.assertFalse(result_1[0])
        self.assertTrue(len(result_1[1]) > 0)

        # First the True test
        condor_pop.grid_options["condor_dir"] = TMP_DIR
        result_2 = condor_pop.condor_check_requirements()
        self.assertTrue(result_2[0])
        self.assertTrue(len(result_2[1]) == 0)


class test_set_condor_status(unittest.TestCase):
    """
    Unittests for function HPC_jobID
    """

    def test_set_condor_status(self):
        with Capturing() as output:
            self._test_set_condor_status()

    def _test_set_condor_status(self):
        """
        Unit test for set_condor_status for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3
        condor_pop.grid_options["condor_dir"] = TMP_DIR

        id_filename = os.path.isfile(
            os.path.join(condor_pop.grid_options["condor_dir"], "ClusterID")
        )
        if os.path.isfile(id_filename):
            os.remove(id_filename)

        #
        os.makedirs(
            os.path.dirname(
                condor_pop.condor_status_file(
                    condor_dir=condor_pop.grid_options["condor_dir"]
                )
            ),
            exist_ok=True,
        )
        condor_pop.set_condor_status("test_set_condor_status")

        # Check if ID file exists
        self.assertTrue(os.path.exists(id_filename))

        # Check if status file exists
        self.assertTrue(
            os.path.isfile(
                condor_pop.condor_status_file(
                    condor_dir=condor_pop.grid_options["condor_dir"]
                )
            )
        )

        with open(
            condor_pop.condor_status_file(
                condor_dir=condor_pop.grid_options["condor_dir"]
            ),
            "r",
        ) as f:
            content_file = f.read()
        self.assertTrue(content_file == "test_set_condor_status")


class test_get_condor_status(unittest.TestCase):
    """
    Unittests for function get_condor_status
    """

    def test_get_condor_status(self):
        with Capturing() as output:
            self._test_get_condor_status()

    def _test_get_condor_status(self):
        """
        Unit test for get_condor_status for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3
        condor_pop.grid_options["condor_dir"] = TMP_DIR

        #
        os.makedirs(
            os.path.dirname(
                condor_pop.condor_status_file(
                    condor_dir=condor_pop.grid_options["condor_dir"]
                )
            ),
            exist_ok=True,
        )
        condor_pop.set_condor_status("test_get_condor_status")

        #
        status = condor_pop.get_condor_status()
        self.assertEqual(status, "test_get_condor_status")


class test_condor_outfile(unittest.TestCase):
    """
    Unittests for function condor_outfile
    """

    def test_condor_outfile(self):
        with Capturing() as output:
            self._test_condor_outfile()

    def _test_condor_outfile(self):
        """
        Unit test for condor_outfile for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3
        condor_pop.grid_options["condor_dir"] = TMP_DIR

        outfile = condor_pop.condor_outfile()
        condor_id = condor_pop.condorID()
        self.assertEqual(outfile, os.path.abspath(os.path.join(condor_pop.grid_options["condor_dir"], "results", "{}.gz".format(condor_id))))


class test_make_condor_dirs(unittest.TestCase):
    """
    Unittests for function make_condor_dirs
    """

    def test_make_condor_dirs(self):
        with Capturing() as output:
            self._test_make_condor_dirs()

    def _test_make_condor_dirs(self):
        """
        Unit test for make_condor_dirs for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3
        condor_pop.grid_options["condor_dir"] = TMP_DIR

        shutil.rmtree(TMP_DIR)
        os.makedirs(TMP_DIR)

        #
        condor_pop.make_condor_dirs()

        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "stdout")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "stderr")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "log")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "results")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "status")))
        self.assertTrue(os.path.isdir(os.path.join(TMP_DIR, "snapshots")))


if __name__ == "__main__":
    unittest.main()

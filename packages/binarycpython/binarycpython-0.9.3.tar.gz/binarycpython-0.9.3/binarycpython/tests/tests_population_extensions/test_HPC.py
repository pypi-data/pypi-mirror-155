"""
Unit tests for the HPC module

TODO: HPC_make_joiningfile
TODO: HPC_joinlist
TODO: HPC_load_joinfiles_list
TODO: HPC_join_from_files
TODO: HPC_can_join
TODO: HPC_job_task
TODO: HPC_grid
TODO: HPC_id_from_dir
TODO: HPC_restore
TODO: HPC_join_previous
TODO: HPC_path
TODO: HPC_snapshot_filename
TODO: HPC_dir
TODO: HPC_touch
TODO: HPC_status
TODO: HPC_dump_status
TODO: HPC_queue_stats
"""

import os
import shutil
import unittest
from binarycpython.utils.functions import Capturing, temp_dir
from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test_HPC")
shutil.rmtree(TMP_DIR)
os.makedirs(TMP_DIR, exist_ok=True)


class test_HPC_njobs(unittest.TestCase):
    """
    Unittests for function HPC_njobs
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_nJobs for condor
        """

        condor_pop = Population()
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_njobs"] = 10

        result_condor = condor_pop.HPC_njobs()

        self.assertEqual(result_condor, 10)

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_nJobs for slurm
        """

        slurm_pop = Population()
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_njobs"] = 11

        result_slurm = slurm_pop.HPC_njobs()

        self.assertEqual(result_slurm, 11)

    def test_none(self):
        with Capturing() as output:
            self._test_none()

    def _test_none(self):
        """
        Unit test for HPC_nJobs when nothing is set
        """

        none_pop = Population()
        self.assertRaises(TypeError, none_pop.HPC_njobs)


class test_HPC_job(unittest.TestCase):
    """
    Unittests for function HPC_job
    """

    def test_HPC_job(self):
        with Capturing() as output:
            self._test_HPC_job()

    def _test_HPC_job(self):
        """
        Test to see if its busy with a job
        """

        slurm_pop = Population()
        slurm_pop.grid_options["slurm"] = 1

        self.assertTrue(slurm_pop.HPC_job())


class test_HPC_job_type(unittest.TestCase):
    """
    Unittests for function HPC_job_type
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_nJobs for condor
        """

        condor_pop = Population()
        condor_pop.grid_options["condor"] = 1
        result_condor = condor_pop.HPC_job_type()

        self.assertEqual(result_condor, "condor")

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_nJobs for slurm
        """

        slurm_pop = Population()
        slurm_pop.grid_options["slurm"] = 1
        result_slurm = slurm_pop.HPC_job_type()

        self.assertEqual(result_slurm, "slurm")

    def test_none(self):
        with Capturing() as output:
            self._test_none()

    def _test_none(self):
        """
        Unit test for HPC_nJobs when nothing is set
        """

        none_pop = Population()
        result_none = none_pop.HPC_job_type()
        self.assertEqual(result_none, "None")


class test_HPC_jobID(unittest.TestCase):
    """
    Unittests for function HPC_jobID
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_jobID for condor
        """

        condor_pop = Population()
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3

        self.assertEqual(
            condor_pop.HPC_jobID(),
            "{ClusterID}.{Process}".format(ClusterID=2, Process=3),
        )

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_jobID for slurm
        """

        slurm_pop = Population()
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5

        self.assertEqual(
            slurm_pop.HPC_jobID(),
            "{jobid}.{jobarrayindex}".format(jobid=4, jobarrayindex=5),
        )

    def test_none(self):
        with Capturing() as output:
            self._test_none()

    def _test_none(self):
        """
        Unit test for HPC_nJobs when nothing is set
        """

        none_pop = Population()
        result_none = none_pop.HPC_jobID()
        self.assertEqual(result_none, None)


class test_HPC_jobID_tuple(unittest.TestCase):
    """
    Unittests for function HPC_jobID_tuple
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_jobID_tuple for condor
        """

        condor_pop = Population()
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3

        self.assertEqual(condor_pop.HPC_jobID_tuple(), ("2", "3"))

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_jobID for slurm
        """

        slurm_pop = Population()
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5

        self.assertEqual(slurm_pop.HPC_jobID_tuple(), ("4", "5"))

    def test_none(self):
        with Capturing() as output:
            self._test_none()

    def _test_none(self):
        """
        Unit test for HPC_nJobs when nothing is set
        """

        none_pop = Population()
        self.assertEqual(none_pop.HPC_jobID_tuple(), (None, None))


class test_HPC_dirs(unittest.TestCase):
    """
    Unittests for function HPC_jobID_tuple
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_dirs for condor
        """

        condor_pop = Population()
        condor_pop.grid_options["condor"] = 1
        self.assertEqual(condor_pop.HPC_dirs(), ["condor_dir"])

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_jobID for slurm
        """

        slurm_pop = Population()
        slurm_pop.grid_options["slurm"] = 1
        self.assertEqual(slurm_pop.HPC_dirs(), ["slurm_dir"])

    def test_none(self):
        with Capturing() as output:
            self._test_none()

    def _test_none(self):
        """
        Unit test for HPC_nJobs when nothing is set
        """

        none_pop = Population()
        self.assertEqual(none_pop.HPC_dirs(), [])


class test_HPC_id_filename(unittest.TestCase):
    """
    Unittests for function HPC_id_filename
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_id_filename for condor
        """

        condor_pop = Population()
        condor_pop.grid_options["condor"] = 1
        self.assertEqual(condor_pop.HPC_id_filename(), "ClusterID")

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_id_filename for slurm
        """

        slurm_pop = Population()
        slurm_pop.grid_options["slurm"] = 1
        self.assertEqual(slurm_pop.HPC_id_filename(), "jobid")

    def test_none(self):
        with Capturing() as output:
            self._test_none()

    def _test_none(self):
        """
        Unit test for HPC_id_filename when nothing is set
        """

        none_pop = Population()
        self.assertEqual(none_pop.HPC_id_filename(), None)


class test_HPC_check_requirements(unittest.TestCase):
    """
    Unittests for function HPC_check_requirements
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_check_requirements for condor
        """

        condor_pop = Population()
        condor_pop.grid_options["condor"] = 1
        self.assertEqual(condor_pop.HPC_id_filename(), "ClusterID")

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1

        # First the False test
        result_1 = condor_pop.HPC_check_requirements()
        self.assertFalse(result_1[0])
        self.assertTrue(len(result_1[1]) > 0)

        # First the True test
        condor_pop.grid_options["condor_dir"] = TMP_DIR
        result_2 = condor_pop.HPC_check_requirements()
        self.assertTrue(result_2[0])
        self.assertTrue(len(result_2[1]) == 0)

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_check_requirements for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1

        # First the False test
        result_1 = slurm_pop.HPC_check_requirements()
        self.assertFalse(result_1[0])
        self.assertTrue(len(result_1[1]) > 0)

        # First the True test
        slurm_pop.grid_options["slurm_dir"] = TMP_DIR
        result_2 = slurm_pop.HPC_check_requirements()
        self.assertTrue(result_2[0])
        self.assertTrue(len(result_2[1]) == 0)

    def test_none(self):
        with Capturing() as output:
            self._test_none()

    def _test_none(self):
        """
        Unit test for HPC_check_requirements when nothing is set
        """

        none_pop = Population(tmp_dir=TMP_DIR)
        result_none = none_pop.HPC_check_requirements()
        self.assertTrue(result_none[0])
        self.assertTrue(len(result_none[1]) == 0)


class test_HPC_set_status(unittest.TestCase):
    """
    Unittests for function HPC_set_status
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_set_status for condor
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
        condor_pop.HPC_set_status("test_set_condor_status")

        # Check if ID file exists
        self.assertTrue(
            os.path.isfile(
                os.path.join(condor_pop.grid_options["condor_dir"], "ClusterID")
            )
        )

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

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_set_status for slurm
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
        slurm_pop.HPC_set_status("test_set_slurm_status")

        # Check if ID file exists
        self.assertTrue(
            os.path.isfile(os.path.join(slurm_pop.grid_options["slurm_dir"], "jobid"))
        )

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


class test_HPC_get_status(unittest.TestCase):
    """
    Unittests for function HPC_get_status
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_get_status for condor
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
        condor_pop.HPC_set_status("test_get_condor_status")

        #
        status = condor_pop.HPC_get_status()
        self.assertEqual(status, "test_get_condor_status")

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_set_status for slurm
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
        slurm_pop.HPC_set_status("test_set_slurm_status")

        status = slurm_pop.HPC_get_status()
        self.assertEqual(status, "test_set_slurm_status")


class test_HPC_job_task(unittest.TestCase):
    """
    Unittests for function HPC_get_status
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_job_task for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3
        condor_pop.grid_options["condor_dir"] = TMP_DIR

        #
        job_task = condor_pop.HPC_job_task()
        self.assertEqual(job_task, 1)


    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_set_status for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5
        slurm_pop.grid_options["slurm_dir"] = TMP_DIR

        #
        job_task = slurm_pop.HPC_job_task()
        self.assertEqual(job_task, 1)


class test_HPC_dir(unittest.TestCase):
    """
    Unittests for function HPC_dir
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_dir for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3
        condor_pop.grid_options["condor_dir"] = os.path.join(TMP_DIR, "condor")

        #
        self.assertEqual(condor_pop.HPC_dir(), os.path.join(TMP_DIR, "condor"))


    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_dir for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5
        slurm_pop.grid_options["slurm_dir"] = os.path.join(TMP_DIR, "slurm")

        #
        self.assertEqual(slurm_pop.HPC_dir(), os.path.join(TMP_DIR, "slurm"))

    def test_none(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_none(self):
        """
        Unit test for HPC_dir for none
        """

        none_pop = Population(tmp_dir=TMP_DIR)

        #
        self.assertEqual(none_pop.HPC_dir(), None)


class test_HPC_id_from_dir(unittest.TestCase):
    """
    Unittests for function HPC_id_from_dir
    """

    def test_condor(self):
        with Capturing() as output:
            self._test_condor()

    def _test_condor(self):
        """
        Unit test for HPC_id_from_dir for condor
        """

        condor_pop = Population(tmp_dir=TMP_DIR)
        condor_pop.grid_options["condor"] = 1
        condor_pop.grid_options["condor_ClusterID"] = 2
        condor_pop.grid_options["condor_Process"] = 3
        condor_pop.grid_options["condor_dir"] = TMP_DIR

        # id
        id_from_dir = condor_pop.HPC_id_from_dir(condor_pop.HPC_dir())

        self.assertEqual(id_from_dir.strip(), str(2))

    def test_slurm(self):
        with Capturing() as output:
            self._test_slurm()

    def _test_slurm(self):
        """
        Unit test for HPC_id_from_dir for slurm
        """

        slurm_pop = Population(tmp_dir=TMP_DIR)
        slurm_pop.grid_options["slurm"] = 1
        slurm_pop.grid_options["slurm_jobid"] = 4
        slurm_pop.grid_options["slurm_jobarrayindex"] = 5
        slurm_pop.grid_options["slurm_dir"] = os.path.join(TMP_DIR)

        # id
        id_from_dir = slurm_pop.HPC_id_from_dir(slurm_pop.HPC_dir())

        self.assertEqual(id_from_dir.strip(), str(4))


if __name__ == "__main__":
    unittest.main()

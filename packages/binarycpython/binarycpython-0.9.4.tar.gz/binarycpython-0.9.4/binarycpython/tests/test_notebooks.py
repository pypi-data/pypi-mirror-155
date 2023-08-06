import unittest


import nbformat
import os

from nbconvert.preprocessors import ExecutePreprocessor

from binarycpython.utils.functions import temp_dir

TMP_DIR = temp_dir("testing", "test_notebooks")
NOTEBOOKS_DIR = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "../../../examples")
)


def run_notebook(notebook_path):
    """
    Function to run notebooks and get the errors
    """

    # https://www.blog.pythonlibrary.org/2018/10/16/testing-jupyter-notebooks/
    nb_name, _ = os.path.splitext(os.path.basename(notebook_path))
    dirname = os.path.dirname(notebook_path)

    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    proc = ExecutePreprocessor(timeout=600, kernel_name="python3")
    proc.allow_errors = True

    proc.preprocess(nb, {"metadata": {"path": "/"}})

    output_path = os.path.join(TMP_DIR, "{}_all_output.ipynb".format(nb_name))

    with open(output_path, mode="wt") as f:
        nbformat.write(nb, f)
    errors = []
    for cell in nb.cells:
        if "outputs" in cell:
            for output in cell["outputs"]:
                if output.output_type == "error":
                    errors.append(output)

    return nb, errors


class TestNotebook(unittest.TestCase):
    """
    Class that contains the notebook test calls
    """

    def test_notebook_api_functionality(self):
        notebook_name = "notebook_api_functionality.ipynb"
        full_notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
        nb, errors = run_notebook(full_notebook_path)
        msg = "\nNotebook: {}\n\n".format(notebook_name) + "\n".join(
            [
                "{}: {}\n{}".format(
                    el["ename"], el["evalue"], "\n".join(el["traceback"])
                )
                for el in errors
            ]
        )
        self.assertEqual(errors, [], msg=msg)

    def test_notebook_population(self):
        notebook_name = "notebook_population.ipynb"
        full_notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
        nb, errors = run_notebook(full_notebook_path)
        msg = "\nNotebook: {}\n\n".format(notebook_name) + "\n".join(
            [
                "{}: {}\n{}".format(
                    el["ename"], el["evalue"], "\n".join(el["traceback"])
                )
                for el in errors
            ]
        )
        self.assertEqual(errors, [], msg=msg)

    def test_notebook_individual_systems(self):
        notebook_name = "notebook_individual_systems.ipynb"
        full_notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
        nb, errors = run_notebook(full_notebook_path)
        msg = "\nNotebook: {}\n\n".format(notebook_name) + "\n".join(
            [
                "{}: {}\n{}".format(
                    el["ename"], el["evalue"], "\n".join(el["traceback"])
                )
                for el in errors
            ]
        )
        self.assertEqual(errors, [], msg=msg)

    def test_notebook_custom_logging(self):
        notebook_name = "notebook_custom_logging.ipynb"
        full_notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
        nb, errors = run_notebook(full_notebook_path)
        msg = "\nNotebook: {}\n\n".format(notebook_name) + "\n".join(
            [
                "{}: {}\n{}".format(
                    el["ename"], el["evalue"], "\n".join(el["traceback"])
                )
                for el in errors
            ]
        )
        self.assertEqual(errors, [], msg=msg)

    def test_notebook_extra_features(self):
        notebook_name = "notebook_extra_features.ipynb"
        full_notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
        nb, errors = run_notebook(full_notebook_path)
        msg = "\nNotebook: {}\n\n".format(notebook_name) + "\n".join(
            [
                "{}: {}\n{}".format(
                    el["ename"], el["evalue"], "\n".join(el["traceback"])
                )
                for el in errors
            ]
        )
        self.assertEqual(errors, [], msg=msg)

    def test_notebook_luminosity_function_single(self):
        notebook_name = "notebook_luminosity_function_single.ipynb"
        full_notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
        nb, errors = run_notebook(full_notebook_path)
        msg = "\nNotebook: {}\n\n".format(notebook_name) + "\n".join(
            [
                "{}: {}\n{}".format(
                    el["ename"], el["evalue"], "\n".join(el["traceback"])
                )
                for el in errors
            ]
        )
        self.assertEqual(errors, [], msg=msg)


if __name__ == "__main__":
    unittest.main()

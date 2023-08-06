import os
import subprocess

import angreal
from angreal import Git, VirtualEnv

HERE = os.path.dirname(__file__)

one_up = os.path.join(HERE, "..")

environment_name = "{{angreal._cleaned_name}}"

setup_py_path = os.path.realpath(os.path.join(one_up, "{{angreal._cleaned_name}}"))

@angreal.command()
def init():
    """
    initialize a python project
    """

    angreal.warn(f"Virtual environment {environment_name} being created.")

    venv = VirtualEnv(name=environment_name, python="python3")
    venv._activate()
    angreal.win(f"Virtual environment {environment_name} created")

    # Initialize the git repo
    git = Git()
    git.init()
    git.add(".")

    # install dependencies
    subprocess.run(
        "pip install -e .[dev]", shell=True, cwd=one_up
    )

    # initialize hooks
    subprocess.run("pre-commit install", shell=True, cwd=one_up)
    subprocess.run("pre-commit run --all-files", shell=True, cwd=one_up)

    angreal.win(f"{environment_name} successfully created !")
    git.commit("-am", "Project initialized via angreal")
    git.branch("-m", "master", "main")
    return

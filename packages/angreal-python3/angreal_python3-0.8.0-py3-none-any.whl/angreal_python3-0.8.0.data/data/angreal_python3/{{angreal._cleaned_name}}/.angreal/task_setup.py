import os


import angreal
from angreal import VirtualEnv, venv_required


here = os.path.dirname(__file__)


@angreal.command()
@angreal.option('--no_dev', is_flag=True, help='Do not setup a dev environment.')
@venv_required('{{angreal._cleaned_name}}')
def angreal_cmd(no_dev):
    """
    update/create the {{angreal.name}} environment.
    """

    venv = VirtualEnv(name=environment_name, python="python3")
    venv._activate()
    # install dependencies
    subprocess.run(
        "pip install -e .[dev]", shell=True, cwd=one_up
    )

    # initialize hooks
    subprocess.run("pre-commit install", shell=True, cwd=one_up)
    subprocess.run("pre-commit run --all-files", shell=True, cwd=one_up)

    return

import json
from pathlib import Path


from ._version import __version__
from .handlers import setup_handlers


HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": data["name"]}]


def _jupyter_server_extension_paths():
    return [{"module": "bodo_jupyterlab"}]


def _load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.
    Args:
      nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    nb_server_app.log.info("Registering Bodo JupyterLab Server Extension...")
    nb_server_app.log.info(
        "Setting up handlers for Bodo JupyterLab Server Extension..."
    )
    setup_handlers(nb_server_app.web_app)
    nb_server_app.log.info(
        "Successfully set up handlers for Bodo JupyterLab Server Extension..."
    )
    nb_server_app.log.info(
        "Successfully registering Bodo JupyterLab Server Extension..."
    )


# For backward compatibility with the classical notebook
load_jupyter_server_extension = _load_jupyter_server_extension

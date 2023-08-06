from cmath import log
import os
import platform
from pathlib import Path
from rm2trash.core import logging


RM2TRASH_TRASH_PATH = os.environ.get("RM2TRASH_TRASH_PATH", None)
if RM2TRASH_TRASH_PATH is None:
    _system = platform.system()
    if _system == "Darwin":
        RM2TRASH_TRASH_PATH = Path.home() / ".Trash"
    elif _system == "Linux":
        RM2TRASH_TRASH_PATH = Path.home() / ".local/share/Trash"
    else:
        raise ValueError(
            "RM2TRASH_TRASH_PATH not set. No default trash dir for OS {}".format(
                _system
            )
        )
else:
    RM2TRASH_TRASH_PATH = Path(RM2TRASH_TRASH_PATH)
if not RM2TRASH_TRASH_PATH.exists():
    logging.info("{} not exists, will make this directory.", RM2TRASH_TRASH_PATH)
    RM2TRASH_TRASH_PATH.mkdir(parents=True, exist_ok=True)

RM2TRASH_DATA_PATH = os.environ.get("RM2TRASH_DATA_PATH")
RM2TRASH_DATA_PATH = Path(RM2TRASH_DATA_PATH or Path.home() / ".local/share/rm2trash")
if not RM2TRASH_DATA_PATH.exists():
    logging.info("{} not exists, will make this directory.", RM2TRASH_DATA_PATH)
    RM2TRASH_DATA_PATH.mkdir(parents=True, exist_ok=True)

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def seq_create(filename: str, range_start: int = 0, range_end: int = 20, padding: int = 4, step: int = 1,
               path: str = "./"):
    """
    Create a sequence of files to be used as input to lsslib.
    """
    for i in range(range_start, range_end + 1, step):
        Path(path + filename + "." + str.rjust(str(i), padding, "0") + ".exr").touch()
    logger.info(f"  Created {filename}")


def seq_rename():
    """
    Rename a sequence of files.
    """
    return None

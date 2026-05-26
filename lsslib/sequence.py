import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def seq_create(stem: str, start_frame: int = 0, end_frame: int = 20, padding: int = 4, step: int = 1, path: str = "./") -> None:
    """
    Create a sequence of files to be used as input to lsslib.
    """
    for i in range(start_frame, end_frame + 1, step):
        Path(path + stem + "." + str(i).zfill(padding) + ".exr").touch()
    logger.info(f"Created {stem}")

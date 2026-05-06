# __init__.py
__version__ = "0.1.0"

import logging

from .sequence import seq_create, seq_rename
from .core import (get_padding, get_stepnumber, get_missing_frames, is_contiguous, get_step_size,
                   get_endframe, get_startframe, find_key)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

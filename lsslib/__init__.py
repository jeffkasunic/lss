# __init__.py
__version__ = "0.1.0"

import logging

from .sequence import seq_create, seq_rename
from .core import (get_padding, get_stepnumber, get_missing_frames, is_contiguous, 
                   get_endframe, get_startframe, get_frame_range_total)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

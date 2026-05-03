# __init__.py
__version__ = "0.1.0"

import logging

from .sequence import seq_create, seq_rename
from .core import (get_unpadded_framenumber, get_padding, get_startframe, get_endframe, get_stepnumber, 
                   is_missing_frame, is_contiguous)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

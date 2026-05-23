# __init__.py
__version__ = "0.2.0"

import logging

from .core_v2 import (Sequence, SequenceParser, SequenceFormatter)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# __init__.py
__version__ = "0.1.0"

import logging

from .sequence import seq_create, seq_rename


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

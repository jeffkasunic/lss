# __init__.py
__version__ = "0.2.0"

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

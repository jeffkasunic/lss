#!/usr/bin/env python3
# Displays file sequences in a compact representation.

import sys
from pathlib import Path
import logging

logger = logging.getLogger("MAIN")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s %(name)s]: %(message)s")


# Get file path from command line
try:
    path = sys.argv[1]
except IndexError:
    path = "./"
logger.info("Reading files: " + path)

# Read files into List
files = sorted(list(Path(path).iterdir()))

# Sort files into groups
for file in files:
    print(file.name)

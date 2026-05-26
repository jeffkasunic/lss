#!/usr/bin/env python3

"""
Displays file sequences in a compact representation.

Running the command will operate on the current working directory if called without an explicit path.
Otherwise, it can take a path as input.

Assumes the filename is formatted: name.framenumber.extension

Examples:
    FooA.0000.exr
    seq3800.0001.exr
    2000.0220.bty_env_01.0001.exr
"""

import sys
import logging
from lsslib.core import SequenceParser, SequenceFormatter

logging.basicConfig(level=logging.WARN, format="[%(levelname)s %(name)s]: %(message)s")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "./"

    parser = SequenceParser()
    formatter = SequenceFormatter()

    for sequence in parser.parse_directory(path):
        print(formatter.format(sequence))

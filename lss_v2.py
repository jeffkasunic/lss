#!/usr/bin/env python3

"""
Displays file sequences in a compact representation. For example:

Files in directory:
    seq3800.0000.exr
    seq3800.0001.exr
    seq3800.0002.exr
    seq3800.0003.exr

Display as:
    seq3800.0-3#4.exr

The tool will display files in the current working directory if called without an explicit path. Otherwise, it will take a path as input.

Assumes the filename is formatted: name.framenumber.extension

Examples:
    FooA.0000.exr
    seq3800.0001.exr
    2000.0220.bty_env_01.0001.exr
"""

import sys
import os
from pathlib import Path
from collections import defaultdict
import logging
from lsslib import core_v2












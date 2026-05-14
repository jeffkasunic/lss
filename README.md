# Tools


## lss
Displays file sequences in a compact representation. For example:

Files in directory:
* seq3800.0000.exr
* seq3800.0001.exr
* seq3800.0002.exr
* seq3800.0003.exr

Display as:
* seq3800.####.0-3.exr

The tool will display files in the current working directory if called without an explicit path. Otherwise, it will take a path as input.

Assumes the filename is formatted: name.framenumber.extension

Examples:
* FooA.0000.exr 
* seq3800.0001.exr 
* 2000.0220.bty_env_01.0001.exr

This script will work on multiple sequences types in the same directory. All three of the above sequences would
parse just fine together. 

## sequence_create
Creates a sequence of files to be used as test input with the lss tool.

The tool will create files in the current working directory if called without an explicit path. Otherwise, it will take a path as input.

It will create five small sequences of files:
* A contigous sequenece of files with 4-padded frames.
* A discontigous sequence of files with 4-padded frames.
* A sequence of files with step of 5.
* A sequence of files with frames of different padding.
* A sequence a non-padded sequence.


# Requirements
The script assumes Python3 is installed.

For Linux and MacOS, execute from the command line: ``lss`` or ``sequence_create``.

For Windows, execute from the command line ``python lss`` or ``python sequence_create``.


# Notes
All tools formatted using the PEP8 style guide.

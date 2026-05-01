# Tools

## lss
Displays file sequences in a compact representation.

The tool will display files in the current working directory if called without an explicit path. Otherwise, it will take a path as input.

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
Assumes Python3 is installed on your system.

# Notes
All tools formatted using the PEP8 style guide.

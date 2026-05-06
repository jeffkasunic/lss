import logging
from unittest import TestResult

logger = logging.getLogger(__name__)

# Public

def get_padding(files):
    """
    Get the padding amount of a frame.
    Tests first frame only. Assumes that the is_contiguous check was run first
    """
    
    padding = []
    for file in files:
        frame_number = file.stem.split('.')[-1]
        padding.append(frame_number)

    if len(padding[0]) == 1 or len(padding[0]) == "0":
        p = 0 #Zero-padded
    elif len(padding[0]) > 1 and not padding[0].startswith('0'):
        p = 0  #Zero-padded
    else:
        p = len(padding[0])
    logger.info(f"The padding is {p}")
    
    return p

def is_contiguous(files):
    """
    Is this a contiguous sequence?
    """
    frame_range_total = _get_frame_range_total(files)
    
    if frame_range_total != len(files):
        contiguous = False
        logger.info("There are missing frames.")
    else:
        contiguous = True
        logger.info("The sequence is contiguous.")
    
    return contiguous


def get_step_size(files):
    """
    Is this a stepped sequence?
    There has to be a more elegant way to do this function.
    
    TO FIX: When paddding is 0 and seqience range is > 9, step detection fails.
    Example: on a sequence frames, 0-12
    The difference between frames is: [1, 9, 1, 1, -10, 1, 1, 1, 1, 1, 1, 1].
    The problem is that my files are being sorted lexicographically.
    This doesn't cause any issues with the program because of the way I use the function.
    
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file.stem))

    # Find the difference between frame numbers
    differences = []
    for i in range(1, len(frames)):
        differences.append(frames[i] - frames[i-1])
    logger.info(f"The difference between frames is: {differences}")

    # Test to make sure the difference is the same for all frames
    comparisons = []
    for diff in differences:
        comparisons.append(diff == differences[0])  # Generate a True or False list
    if all(comparisons):  # If all comparisons are True
        logger.info(f"The step size is: {differences[0]} ")
        return differences[0]
    else:
        logger.info("The sequence is not stepped.")
        return False

def get_missing_frames(files):
    """
    Get the missing frame in an array of integers.
    
    TO FIX: On a stepped sequence it only detects the missing frame before the current frame.
    For example: Missing frame numbers: [4, 9, 14] is the result for stepped sequence of 5.
    It does not break the stepped check, but it won't not work for sequences with more than one
    contiguous missing file.
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file.stem))
        
    missing_frames = []
    for i in range(1, len(frames)):
        if frames[i] == frames[i-1] + 1:
            continue
        else:
            missing_frames.append(frames[i] - 1)
    logger.info(f"Missing frame numbers: {missing_frames}")
    return missing_frames


def get_stepnumber(frame_range):
    """
    Get the step number in an array of integers.
    """
    return None


def get_startframe(files):
    """
    Get the min value in an array of integers.
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file.stem))
    startframe = min(frames)
    logger.info(f"The startframe is {startframe}")

    return startframe


def get_endframe(files):
    """
    Get the max value in an array of integers.
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file.stem))
    endframe = max(frames)
    logger.info(f"The endframe is {endframe}")
    
    return endframe

def find_key(files):
    """
    Find the longest common prefix in a sequence of files.
    """
    # This uses a vertical scanning approach where I compare chars in one element to the next
    # element, one at a time, until I find a change between two. This only works on a sorted list.
    # 
    # My initial attempts inolved a sliding window algorithm, but then realized only the right pointer
    # moves in this case. The solution morphed into a simpler Longest Common Prefix algorithm 
    
    logger.info(f"Finding key.")
    logger.info(f"The number of files is {len(files)}")
    
    frames = []
    for file in files:
        frames.append(file.name)

    logger.info(f"The file are {frames}")
    logger.info(f"length of frame[0]: {len(frames[0])} ")
    logger.info(f"frame[0]: {frames[0]} ")

    longest_filename_in_dir = _get_longest_filename(files)
    logger.info(f"The longest filename is {longest_filename_in_dir} chars")

    for i in range(0, longest_filename_in_dir):  # get the length of the first element
        char = frames[0][i]  # Get first char of first string
        for j in range(1, len(frames)):  # Start at second element in the list and compare to first
            if frames[j][i] != char or i == len(frames[j]):  
                seq_key = frames[0][0:i]  # assign all chars that are same
                return seq_key
            else:
                continue
    return None

def group_keys(keys):
    
    return None


# Private

def _get_unpadded_framenumber(filename):
    """
    Get the current frame number with padding removed.
    """
    frame_number = int(filename.split('.')[-1])

    return frame_number

def _get_frame_range_total (files):
    frame_range_total = (get_endframe(files) - get_startframe(files) + 1)
    logger.info(f"The frame range total is {frame_range_total}")

    return frame_range_total

def _get_longest_filename(files):
    return max(len(file.stem) for file in files)

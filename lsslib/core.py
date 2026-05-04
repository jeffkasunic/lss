import logging
from difflib import Differ

logger = logging.getLogger(__name__)


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
    frame_range_total = get_frame_range_total(files)
    
    if frame_range_total != len(files):
        contiguous = False
        logger.info("There are missing frames.")
    else:
        contiguous = True
        logger.info("The sequence is contiguous.")
    
    return contiguous


def is_stepped(files):
    """
    Is this a stepped sequence?
    There has to be a more elegant way to do this function.
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file.stem))
    logger.info(frames)

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
        logger.info("The sequence is stepped.")
        return differences[0]
    else:
        logger.info("The sequence is not stepped.")
        return False

def get_missing_frames(files):
    """
    Get the missing frame in an array of integers.
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
    logger.info(f"Missing frame(s) {missing_frames}")
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


def get_frame_range_total (files):
    frame_range_total = (get_endframe(files) - get_startframe(files) + 1)
    logger.info(f"The frame range total is {frame_range_total}")

    return frame_range_total


# Private

def _get_unpadded_framenumber(filename):
    """
    Get the current frame number with padding removed.
    """
    frame_number = int(filename.split('.')[-1])

    return frame_number

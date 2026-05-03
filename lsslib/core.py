import logging

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


def get_missing_frames(files):
    """
    Get the missing frame in an array of integers.
    """
    #frame_range_total = get_frame_range_total(files)
    frames = _get_unpadded_framenumber(files)
    
    missing_frames = []
    i = 0
    
    """
    while i < frame_range_total:
        if files[frames] == files[frames + 1] - 1:
            frames += 1
        else:
            missing_frames.append(i+1)
    """    
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

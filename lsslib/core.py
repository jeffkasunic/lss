import logging

logger = logging.getLogger(__name__)


def get_unpadded_framenumber(filename):
    """
    Get the current frame number with padding removed.
    """
    frame_number = int(filename.split('.')[-1])

    return frame_number


def get_padding(filename):
    """
    Get the padding number in an array of integers.
    """
    frame_number = filename.split('.')[-1]
    number_length = len(filename.split('.')[-1])

    if number_length == 1 or frame_number == "0":
        return 0  #Zero-padded
    elif number_length > 1 and not frame_number.startswith('0'):
        return 0  #Zero-padded
    else:
        return number_length


def get_startframe(files):
    """
    Get the min value in an array of integers.
    """
    frames = []
    for file in files:
        frames.append(get_unpadded_framenumber(file.stem))
    return min(frames)


def get_endframe(files):
    """
    Get the max value in an array of integers.
    """
    frames = []
    for file in files:
        frames.append(get_unpadded_framenumber(file.stem))
    return max(frames)

def get_frame_range_total (files):
    frame_range_total = (get_endframe(files) - get_startframe(files) + 1)
    logger.info(f"The frame range total is {frame_range_total}")
    
    return frame_range_total


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
    frames = get_unpadded_framenumber(files)
    
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

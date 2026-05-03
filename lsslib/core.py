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


def get_stepnumber():
    """
    Get the step number in an array of integers.
    """
    return None


def is_contiguous():
    """
    Is this a contiguous sequence?
    """
    return None


def is_missing_frame():
    """
    Get the missing frame in an array of integers.
    """
    return None


def get_identical_string():
    """
    Find left justified identical, matching chars. Used to find grouping.
    It compares the current item to the previous item in the array.
    """


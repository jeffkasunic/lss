import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# Public

def get_padding(files):
    """
    Get the padding amount of a frame.
    Tests first frame only. Assumes that the is_contiguous check was run first
    """
    
    padding = []
    for file in files:
        frame_number = file.split('.')[-2]
        padding.append(frame_number)

    if len(padding[0]) == 1 or len(padding[0]) == "0":
        p = 0 #Zero-padded
    elif len(padding[0]) > 1 and not padding[0].startswith('0'):
        p = 0  #Zero-padded
    else:
        p = len(padding[0])
    logger.info(f"The padding for {padding} is {p}")
    
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

def is_mixed_padding(files):
    """
    Is there more than one padding-length in the directory?
    """
    padding = []
    for f in files:
        padding.append(len(f.rsplit('.', 2)[-2]))
    padding = set(padding)  # Use a set to hold only unique values.
    logger.info(f"The set of padding lengths is {padding}")

    # If there is more than one padding length, this is True. False if not.
    if len(padding) > 1:
        is_mixed = True
    else:
        is_mixed = False

    logger.info(f"Is padding mixed: {is_mixed}")
    
    return is_mixed

def get_step_size(files):
    """
    Is this a stepped sequence?
    """
        
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file))

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
    """

    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file))
    
    frame_range = _get_frame_range_total(files)
    
    logger.info(f"The length of frames is {len(frames)}")
    logger.info(f"The frame range is {frame_range}")
    logger.info(f"The frames are: {frames}")

    missing_frames = []
    for i in range(1, frame_range):
        if i not in frames:
            missing_frames.append(i)
    
    logger.info(f"Missing frame numbers: {missing_frames}")
    return missing_frames


def get_startframe(files):
    """
    Get the min value in an array of integers.
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file))
    startframe = min(frames)
    logger.info(f"The startframe for {frames} is {startframe}")

    return startframe


def get_endframe(files):
    """
    Get the max value in an array of integers.
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file))
    endframe = max(frames)
    logger.info(f"The endframe {frames} is {endframe}")
    
    return endframe


def group_keys(files):
    """
    Group sequences of files into a hash table / dictionary.
    """
    # Iterates from the end of the filename, using "." as the delimiter. Everything after the
    # first two "." encountered is the key.

    grouped_keys = defaultdict(list)

    frames = []
    for file in files:
        frames.append(file.name)
    logger.info(f"The file are {frames}")

    for frame in frames:
        key = frame.rsplit('.', 2)[0]
        grouped_keys[key].append(frame)
        
    return grouped_keys


def find_key(files):
    """
    Find the longest common prefix in a sequence of files.
    """
    # My initial attempts inolved a sliding window algorithm, using a vertical scanning approach where I compare
    # chars in one element to the next element, one at a time, until I find a change between two. This only works on a sorted list. 
    # 
    # But then I realized only the right pointer moves in this case. The solution morphed into a simpler Longest Common Prefix algorithm.
    # 
    # But in the end, I realized all I had to do was iterate from the end of the filename, using "." as the delimiter.
    # Everything before the first two "." encountered is the key.
    #
    # I was trying to account for all possible naming conventions and delimiters, but settled on enforcing this: filename.anyting.anything
    # That will be version 2.0.
    #
    # This function is no longer used in this script.


    logger.info(f"Finding key.")
    logger.info(f"The number of files is {len(files)}")

    frames = []
    for file in files:
        frames.append(file.name)

    logger.info(f"The file are {frames}")
    logger.info(f"length of frame[0]: {len(frames[0])} ")
    logger.info(f"frame[0]: {frames[0]} ")

    longest_filename_in_dir = _get_longest_filename(frames)
    logger.info(f"The longest filename is {longest_filename_in_dir} chars")

    for i in range(0, longest_filename_in_dir):
        char = frames[0][i]
        for j in range(1, len(frames)):
            if frames[j][i] != char or i == len(frames[j]):
                seq_key = frames[0][0:i]
                return seq_key
            else:
                continue
    return None


# Private

def _get_unpadded_framenumber(filename):
    """
    Get the current frame number with padding removed.
    """
    frame_number = int(filename.split('.')[-2])
    # logger.info(f"The unpadded frame_number for {filename} is {frame_number}")

    return frame_number

def _get_frame_range_total (files):
    frame_range_total = (get_endframe(files) - get_startframe(files) + 1)
    logger.info(f"The frame range total is {frame_range_total}")

    return frame_range_total

def _get_longest_filename(files):
    
    return max(len(file) for file in files)

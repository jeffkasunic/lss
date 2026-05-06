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
        frames.append(_get_unpadded_framenumber(file))
    startframe = min(frames)
    logger.info(f"The startframe is {startframe}")

    return startframe


def get_endframe(files):
    """
    Get the max value in an array of integers.
    """
    frames = []
    for file in files:
        frames.append(_get_unpadded_framenumber(file))
    endframe = max(frames)
    logger.info(f"The endframe is {endframe}")
    
    return endframe

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

    longest_filename_in_dir = _get_longest_filename(files)
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

def group_keys(files):
    """
    Group sequences of files into a hash table / dictionary.
    
    Assumes the filename is formatted: any_text_delimter_or_numer.number.filetension
        Examples:
            FooA.0000.exr
            2000.0220.bty_env_01.0001.exr
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
            #logger.info(f"The key is {key}")
            #logger.info(f"The grouped key is {grouped_keys}")
        
    return grouped_keys


# Private

def _get_unpadded_framenumber(filename):
    """
    Get the current frame number with padding removed.
    """
    frame_number = int(filename.split('.')[-2])
    logger.info(f"The unpadded frame_number is {frame_number}")

    return frame_number

def _get_frame_range_total (files):
    frame_range_total = (get_endframe(files) - get_startframe(files) + 1)
    logger.info(f"The frame range total is {frame_range_total}")

    return frame_range_total

def _get_longest_filename(files):
    
    return max(len(file.stem) for file in files)

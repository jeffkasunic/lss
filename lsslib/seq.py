from pathlib import Path

def seq_create(filename:str, range_start:int = 1, range_end:int = 7, padding:int = 4, step:int = 1, path:str = "./"):
    """
    Create a sequence of files to be used as input to lsslib.
    """
    for i in range(range_start, range_end + 1, step):
        Path(path + filename + "." + str.rjust(str(i),padding,"0") + ".exr").touch()
def seq_rename():
    """
    Rename a sequence of files.
    """
    return None

def seq_delete():
    """
    Delete a sequence of files.
    """
    return None

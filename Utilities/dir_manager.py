import os


def find_mp3_files(src_dir):
    """
    A function to list all mp3 files under a given source directory.

    Parameters:
        src_dir (String): Source directory.

    Returns:
         List : List of paths for all mp3 files.

    """
    mp3_files = []
    for r, d, f in os.walk(src_dir):
        for file in f:
            if '.mp3' in file:
                mp3_files.append(os.path.join(r, file))
    return mp3_files


def find_wav_files(src_dir):
    """
    A function to list all wav files under a given source directory.

    Parameters:
        src_dir (String): Absolute/Relative path of source directory.

    Returns:
        List : List of all wav files.

    """
    wav_files = []
    for r, d, f in os.walk(src_dir):
        for file in f:
            if '.wav' in file:
                wav_files.append(os.path.join(r, file))
    return wav_files


def create_dir(src_dir):
    """
    A function to create a directory given its path.

    Parameters:
        src_dir (String): Directory path.

    """
    if not os.path.exists(src_dir):
        os.makedirs(src_dir)

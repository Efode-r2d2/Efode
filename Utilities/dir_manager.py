import os


def find_mp3_files(src_dir):
    """

    :type src_dir: object
    """
    mp3_files = []
    for r, d, f in os.walk(src_dir):
        for file in f:
            if '.mp3' in file:
                mp3_files.append(os.path.join(r, file))
    return mp3_files


def find_wav_files(src_dir):
    """

    :type src_dir: object
    """
    wav_files = []
    for r, d, f in os.walk(src_dir):
        for file in f:
            if '.wav' in file:
                wav_files.append(os.path.join(r, file))
    return wav_files


def create_dir(src_dir):
    """

    :type src_dir: object
    """
    if not os.path.exists(src_dir):
        os.makedirs(src_dir)

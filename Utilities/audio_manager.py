import librosa


def load_audio(audio_path, sr=7000, offset=None, duration=None):
    """
    A function to load a monophonic time series audio data sampled at a given sampling rate.

    Parameters:
        audio_path (String): Absolute/Relative path of the audio.
        sr (int): Sampling rate.
        offset (float): Where the reading starts.
        duration (float): Duration of the reading.

    Returns:
         numpy.ndarray : Time series audio data.

    """
    if offset is not None and duration is not None:
        audio_data, sr = librosa.load(path=audio_path,
                                      sr=sr, offset=offset, duration=duration)
        return audio_data
    else:
        audio_data, sr = librosa.load(path=audio_path,
                                      sr=sr)
        return audio_data

import librosa
import numpy as np


class STFT(object):
    """
    STFT class to compute the time-frequency representation (Spectrogram) of an audio given
    its monophonic time-series audio data. Short time fourier transform is used as a transform
    function.

    Attributes:
        n_fft (int) : Defines number of DFT bins, i.e number of bins = n_fft/2 +1.
        hop_length (int): Hop length.
        sr (int): Sampling rate.
    """
    def __init__(self, n_fft=1024, hop_length=32, sr=7000):
        """
        A constructor for STFT class.

        Parameters:
             n_fft (int) : Defines number of DFT bins, i.e number of bins = n_fft/2 +1.
             hop_length (int): Hop length.
             sr (int): Sampling rate.

        """
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.sr = sr

    def __compute_spectrogram(self, audio_data):
        """
        A method to compute the spectrogram of an audio from its time series representation.

        Parameters:
            audio_data (numpy.ndarray): Time series representation of a given audio.

        Returns:
            numpy.ndarray: Time-frequency representation of of given time series audio data.

        """
        spectrogram = librosa.stft(y=audio_data, n_fft=self.n_fft, hop_length=self.hop_length)
        return spectrogram

    def __compute_spectrogram_magnitude(self, audio_data):
        """
        A method to compute a a spectrogram magnitude of give time series audio data.

        Parameters:
            audio_data (numpy.ndarray): Monophonic time series representation of audio data.

        Returns:
            numpy.ndarray: Magnitude of spectrogram of a give audio data.

        """
        spectrogram = self.__compute_spectrogram(audio_data)
        spectrogram_magnitude = np.abs(spectrogram)
        return spectrogram_magnitude

    def compute_spectrogram_magnitude_in_db(self, audio_data):
        """
        A method to compute a magnitude of spectrogram of an audio in db.

        Parameters:
            audio_data (numpy.ndarray): Monophonic time series representation of a given audio.

        Returns:
            numpy.ndarray: magnitude of spectrogram of an audio in db.

        """
        spectrogram_magnitude = self.__compute_spectrogram_magnitude(audio_data)
        spectrogram_magnitude_in_db = librosa.amplitude_to_db(spectrogram_magnitude, ref=np.max)
        return spectrogram_magnitude_in_db

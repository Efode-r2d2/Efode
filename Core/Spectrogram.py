"""
    < This program reproduced a work published in https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf>
    Copyright (C) <2019>  <Efriem Desalew Gebie>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import librosa
import numpy as np


class Spectrogram(object):

    def __init__(self, n_fft=1024, hop_length=256):
        """

        :param n_fft:
        :param hop_length:
        """
        self.n_fft = n_fft
        self.hop_length = hop_length

    def compute_stft(self, audio_data):
        """

        :param audio_data:
        :return:
        """
        stft = librosa.stft(y=audio_data, n_fft=self.n_fft, hop_length=self.hop_length)
        return stft

    def compute_stft_magnitude(self, audio_data):
        """

        :param audio_data:
        :return:
        """
        stft = self.compute_stft(audio_data)
        stft_magnitude = np.abs(stft)
        return stft_magnitude

    def compute_stft_magnitude_in_db(self, audio_data):
        """

        :param audio_data:
        :return:
        """
        stft_magnitude = self.compute_stft_magnitude(audio_data)
        stft_magnitude_in_db = librosa.amplitude_to_db(stft_magnitude, ref=np.max)
        return stft_magnitude_in_db

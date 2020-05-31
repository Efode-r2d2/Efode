"""
    < Efode is an an open source audio fingerprinting system>
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

    def __init__(self, n_fft=1024, hop_length=256, sr=7000):
        """

        :param n_fft:
        :param hop_length:
        """
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.sr = sr

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

    def compute_cqt(self, audio_data):
        return librosa.cqt(y=audio_data, sr=self.sr, fmin=27.3)

    def compute_cqt_magnitude(self, audio_data):
        cqt = self.compute_cqt(audio_data=audio_data)
        return np.abs(cqt)

    def compute_cqt_magnitude_in_db(self, audio_data):
        cqt_magnitude = self.compute_cqt_magnitude(audio_data=audio_data)
        return librosa.amplitude_to_db(cqt_magnitude, ref=np.max)

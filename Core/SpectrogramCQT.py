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


class CQT(object):

    def __init__(self, sr=7000, hop_length=32, n_bins=84, bins_per_octave=24, f_min=27.3):
        self.sr = sr
        self.hop_length = hop_length
        self.n_bins = n_bins
        self.bins_per_octave = bins_per_octave
        self.f_min = f_min

    def compute_cqt(self, audio_data):
        return librosa.cqt(y=audio_data,
                           sr=self.sr,
                           hop_length=self.hop_length,
                           n_bins=self.n_bins,
                           bins_per_octave=self.bins_per_octave,
                           fmin=self.f_min)

    def compute_cqt_magnitude(self, audio_data):
        cqt = self.compute_cqt(audio_data=audio_data)
        return np.abs(cqt)

    def compute_cqt_magnitude_in_db(self, audio_data):
        cqt_magnitude = self.compute_cqt_magnitude(audio_data=audio_data)
        return librosa.amplitude_to_db(cqt_magnitude, ref=np.max)

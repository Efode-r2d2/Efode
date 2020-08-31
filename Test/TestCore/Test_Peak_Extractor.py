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
from Core import STFT
from Core import PeakExtractor
from Utilities import audio_manager
from Utilities import dir_manager
from Utilities import graph_manager

# source directory
src_dir = "../../../Test_Data/Reference_Audios"
# spectrogram and peak extractor objects
stft = STFT(hop_length=128)
peak_extractor = PeakExtractor(maximum_filter_width=20, maximum_filter_height=10)
# searching for all .mp3 files under given source dir
mp3_files = dir_manager.find_mp3_files(src_dir=src_dir)
# reading time series audio data re-sampled at 7KHz for a given audio portion specified by offset and duration
# parameters
audio_data = audio_manager.load_audio(audio_path=mp3_files[0], offset=10.0, duration=3.0)
# compute spectrogram
spectrogram = stft.compute_stft_magnitude_in_db(audio_data=audio_data)
# extract spectral peaks
spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=spectrogram)
# display spectrogram along with extracted spectral peaks
graph_manager.display_spectrogram_peaks(spectrogram=spectrogram,
                                        spectral_peaks_x=spectral_peaks[1],
                                        spectral_peaks_y=spectral_peaks[2])

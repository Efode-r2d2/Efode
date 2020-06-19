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
from Core import CQT
from Core import PeakExtractor
from Utilities import AudioManager
from Utilities import DirManager
from Utilities import GraphManager

# source directory
src_dir = "../../../Test_Data/Reference_Audios"
# spectrogram and peak extractor objects
cqt = CQT(hop_length=128)
peak_extractor = PeakExtractor(maximum_filter_width=20, maximum_filter_height=10)
# searching for all .mp3 files under given source dir
mp3_files = DirManager.find_mp3_files(src_dir=src_dir)
# time series audio data
audio_data = AudioManager.load_audio(audio_path=mp3_files[0], offset=10.0, duration=3.0)
# compute spectrogram
spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=audio_data)
# extract spectral peaks
spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=spectrogram)
# display spectrogram along with extracted spectral peaks
GraphManager.display_spectrogram_peaks(spectrogram=spectrogram,
                                       spectral_peaks_x=spectral_peaks[1],
                                       spectral_peaks_y=spectral_peaks[2])

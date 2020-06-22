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
from Utilities import AudioManager
from Utilities import GraphManager
from Utilities import DirManager
from Core import STFT
from Core import PeakExtractor
from Core import FingerprintGenerator
from RTreeManager import RTreeManager
from RawDataManager import RawDataManager
from ConfigManager import ConfigManager

# source dir
src_dir = "../../../Test_Data/Query_Audios/Speed_Change"
# r_tree path
r_tree_path = "../../../Hashes/Efode/R_Tree_STFT"
# raw_data_path
raw_data_path = "../../../Raw_Data/Efode/Raw_Data_STFT"
# config file path
config_file_path = "../../Config/Config_STFT.ini"
# spectrogram, peak  extractor and fingerprint generator objects
stft = STFT(hop_length=128)
peak_extractor = PeakExtractor(maximum_filter_width=50, maximum_filter_height=25)
fingerprint_generator = FingerprintGenerator()
# searching for all .mp3 files under specified source dir
query_audios = DirManager.find_wav_files(src_dir=src_dir)
# get r_tree_index
# r_tree_index = RTreeManager.get_rtree_index(rtree_path=r_tree_path)
# shelf index
# shelf_index = RawDataManager.get_shelf_file_index(shelf_path=raw_data_path)
# fingerprinting files

original_audio_data = AudioManager.load_audio(audio_path=query_audios[0], sampling_rate=7000)
modified_audio_data = AudioManager.load_audio(audio_path=query_audios[1], sampling_rate=7000)

original_stft = stft.compute_stft_magnitude_in_db(audio_data=original_audio_data)
modified_stft = stft.compute_stft_magnitude_in_db(audio_data=modified_audio_data)

original_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=original_stft)
modified_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=modified_stft)

GraphManager.display_spectrogram_peaks_2(original_stft,
                                         original_peaks[1],
                                         original_peaks[2],
                                         modified_peaks[1],
                                         modified_peaks[2],
                                         "Original Vs Modified")

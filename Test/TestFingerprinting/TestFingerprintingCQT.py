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
from Core import CQT
from Core import PeakExtractor
from Core import FingerprintGenerator
from RTreeManager import RTreeManager
from RawDataManager import RawDataManager
from ConfigManager import ConfigManager
import tkinter as tk

# source dir
src_dir = "../../../Test_Data/Query_Audios/Speed_Change"
# r_tree path
r_tree_path = "../../../Hashes/Efode/R_Tree_CQT"
# raw_data_path
raw_data_path = "../../../Raw_Data/Efode/Raw_Data_CQT"
# config file path
config_file_path = "../../Config/Config_CQT.ini"
# spectrogram, peak  extractor and fingerprint generator objects
spectrogram = CQT(hop_length=64)
peak_extractor = PeakExtractor(maximum_filter_height=25, maximum_filter_width=50)
fingerprint_generator = FingerprintGenerator()
# searching for all .mp3 files under specified source dir
query_audios = DirManager.find_wav_files(src_dir=src_dir)
# get r_tree_index
r_tree_index = RTreeManager.get_rtree_index(rtree_path=r_tree_path)
# shelf index
shelf_index = RawDataManager.get_shelf_file_index(shelf_path=raw_data_path)
# fingerprinting files
print(query_audios[0])
audio_data = AudioManager.load_audio(audio_path=query_audios[0],
                                     sampling_rate=7000)

print(audio_data.size)
# GraphManager.display_audio_waveform(audio_data=audio_data,
#                                     sampling_rate=7000,
#                                     plot_title="Audio Waveform")
cqt_in_db = spectrogram.compute_cqt_magnitude_in_db(audio_data=audio_data)
modified_audio_data = AudioManager.load_audio(audio_path=query_audios[1], sampling_rate=7000)
modified_cqt_in_db = spectrogram.compute_cqt_magnitude_in_db(audio_data=modified_audio_data)
print(cqt_in_db.shape)
spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=cqt_in_db)
spectral_peaks_2 = peak_extractor.extract_spectral_peaks_2(spectrogram=modified_cqt_in_db)
audio_fingerprints = list()
audio_fingerprints_info = list()

fingerprint_generator.generate_fingerprints(spectral_peaks=spectral_peaks[0],
                                            audio_fingerprints=audio_fingerprints,
                                            audio_fingerprints_info=audio_fingerprints_info,
                                            r=1.0,
                                            c=1,
                                            fixed=False,
                                            no_groups=2)

print(audio_fingerprints)
#fingerprints = fingerprint_generator.generate_fingerprints(f)
# GraphManager.display_spectrogram(spectrogram=cqt_in_db,plot_title="CQT")
GraphManager.display_spectrogram_peaks_2(cqt_in_db, spectral_peaks[1], spectral_peaks[2], spectral_peaks_2[1],
                                         spectral_peaks_2[2], "Modified Vs Original")
# GraphManager.display_spectrogram_peaks(cqt_in_db, spectral_peaks[1], spectral_peaks[2], "CQT")
print("Spectral Peaks Dimension", spectral_peaks)

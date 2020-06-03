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
src_dir = "../../../Test_Data/Reference_Audios"
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
reference_audios = DirManager.find_mp3_files(src_dir=src_dir)
# get r_tree_index
r_tree_index = RTreeManager.get_rtree_index(rtree_path=r_tree_path)
# shelf index
shelf_index = RawDataManager.get_shelf_file_index(shelf_path=raw_data_path)
# fingerprinting files
iter =0
for i in reference_audios:
    # list to store audio fingerprints and raw info about audio fingerprints
    audio_fingerprints = list()
    audio_fingerprints_info = list()
    # audio id
    audio_id = i.split("/")[5].split(".")[0]
    # time series audio data
    audio_data = AudioManager.load_audio(audio_path=i, sampling_rate=7000)
    # transformed audio data using constant q transform
    cqt_in_db = spectrogram.compute_cqt_magnitude_in_db(audio_data=audio_data)
    # spectral peaks extracted from transformed audio data
    spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=cqt_in_db)

    fingerprint_generator.generate_fingerprints(spectral_peaks=spectral_peaks[0],
                                                audio_fingerprints=audio_fingerprints,
                                                audio_fingerprints_info=audio_fingerprints_info,
                                                r=1.0,
                                                c=1,
                                                fixed=False,
                                                no_groups=2)
    raw_index = int(ConfigManager.read_config(config_file_path=config_file_path,
                                              section="Default", sub_section="Raw_Index"))
    fingerprint_index = 0
    for j in audio_fingerprints:
        row = [audio_id] + audio_fingerprints_info[fingerprint_index]
        RTreeManager.insert_node(rtree_index=r_tree_index, node_id=raw_index, geo_hash=j)
        RawDataManager.insert_data(shelf=shelf_index, key=raw_index, value=row)
        raw_index += 1
        fingerprint_index += 1
    ConfigManager.write_config(config_file_path=config_file_path,
                               section="Default",
                               sub_section="Raw_Index",
                               value=str(raw_index))
    print("Done With Fingerprinting ", iter)
    iter += 1
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
from Core import Spectrogram
from Core import PeakExtractor
from Core import FingerprintGenerator
from RTreeManager import RTreeManager
from RawDataManager import RawDataManager
from ConfigManager import ConfigManager

# source dir
src_dir = "../../../Test_Data/Reference_Audios"
# r_tree path
r_tree_path = "../../../Hashes/Efode/R_Tree"
# raw_data_path
raw_data_path = "../../../Raw_Data/Efode/Raw_Data"
# spectrogram, peak  extractor and fingerprint generator objects
stft = Spectrogram(hop_length=32)
peak_extractor = PeakExtractor()
fingerprint_generator = FingerprintGenerator()
# searching for all .mp3 files under specified source dir
mp3_files = DirManager.find_mp3_files(src_dir=src_dir)

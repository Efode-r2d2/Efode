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

from Utilities import DirManager
from Utilities import AudioManager
from Core import CQT
from Core import PeakExtractor
from Core import Fingerprint
from FingerprintManager import FingerprintManager

# defining constants
SAMPLING_RATE = 7000  # sampling rate
HOP_LENGTH = 32  # hop length
MAXIMUM_FILTER_WIDTH = 50  # maximum filter width
MAXIMUM_FILTER_HEIGHT = 25  # maximum filter height
FRAMES_PER_SECOND = 219  # number of audio frames for one second audio duration
TARGET_ZONE_WIDTH = 1  # width of the target zone in seconds
TARGET_ZONE_CENTER = 2  # center of the target zone in seconds
TOLERANCE = 0.0  # maximum allowed tolerance for both pitch shifting and time stretching

# source directory for reference audios
src_dir = "../../../Test_Data/Reference_Audios"
r_tree = "../../../Hashes/Efode/CQT_Test"
# raw_data_path
shelf = "../../../Raw_Data/Efode/CQT_Test"
# config file path
config = "../../Config/Config_CQT_Test.ini"

'''
    Instantiating an object for constant q transform. 
    A constant q transform function is applied to a time series audio data to compute 
    time-frequency representation of a given reference audio
'''
cqt = CQT(sr=SAMPLING_RATE, hop_length=HOP_LENGTH)
'''
    Instantiating an object for peak extraction.
    A peak extraction function will accept a spectrogram of a given reference audio and 
    it will return its respective spectral peaks based on predefined peak extraction
    parameters. Here, a spectral peak is defined in terms of its tempo and frequency information.
'''
peak_extractor = PeakExtractor(maximum_filter_width=MAXIMUM_FILTER_WIDTH,
                               maximum_filter_height=MAXIMUM_FILTER_HEIGHT)
'''
    Instantiating an object for fingerprint extraction.
    A fingerprint extraction function will accept spectral peaks of a given reference audio
    and it will return its computed audio fingerprint along with necessary raw information's 
    by applying geometric hashing. Here, the hashes are defined in terms of X and Y values. 
'''
fingerprint = Fingerprint(frames_per_second=FRAMES_PER_SECOND, target_zone_width=TARGET_ZONE_WIDTH,
                          target_zone_center=TARGET_ZONE_CENTER, tolerance=TOLERANCE)
'''
    Instantiating a fingerprint manager object. Fingerprint manager object is used to 
    store fingerprints and match fingerprints.
'''
fingerprint_manager = FingerprintManager(r_tree=r_tree, shelf=shelf, config=config)

# finding all reference audios
reference_audios = DirManager.find_mp3_files(src_dir=src_dir)

# fingerprinting all reference audios
for i in reference_audios:
    audio_id = i.split("/")[5].split(".")[0]
    audio_data = AudioManager.load_audio(audio_path=i, sampling_rate=SAMPLING_RATE)
    spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=audio_data)
    spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=spectrogram)
    audio_fingerprints = fingerprint.__generate_fingerprints__(spectral_peaks=spectral_peaks[0])
    fingerprint_manager.__store_fingerprints__(audio_fingerprints=audio_fingerprints, audio_id=audio_id)
    print("Done Fingerprinting", audio_id)

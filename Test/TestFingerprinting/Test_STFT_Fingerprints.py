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

from Utilities import dir_manager
from Utilities import audio_manager
from Core import STFT
from Core import PeakExtractor
from Core import Fingerprint
from FingerprintManager import FingerprintManager

# defining constants
SAMPLING_RATE = 7000  # sampling rate
HOP_LENGTH = 32  # hop length
MAXIMUM_FILTER_WIDTH = 150  # maximum filter width
MAXIMUM_FILTER_HEIGHT = 75  # maximum filter height
FRAMES_PER_SECOND = 219  # number of audio frames for one second audio duration
TARGET_ZONE_WIDTH = 1  # width of the target zone in seconds
TARGET_ZONE_CENTER = 2  # center of the target zone in seconds
TOLERANCE = 0.0  # maximum allowed tolerance for both pitch shifting and time stretching
# source directory for reference audios
src_dir = "../../../Test_Data/Reference_Audios"
r_tree = "../../../Hashes/Efode/STFT_Test"
# raw_data_path
shelf = "../../../Raw_Data/Efode/STFT_Test"
# config file path
config = "../../Config/Config_STFT_Test.ini"

'''
    Instantiating an object for short time fourier transform. 
    Short time fourier transform function is applied to a time series audio data to compute 
    time-frequency representation of a given reference audio
'''
stft = STFT(hop_length=HOP_LENGTH, sr=SAMPLING_RATE)
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
reference_audios = dir_manager.find_mp3_files(src_dir=src_dir)

# fingerprinting all reference audios
for i in reference_audios:
    audio_id = i.split("/")[5].split(".")[0]
    audio_data = audio_manager.load_audio(audio_path=i, sr=SAMPLING_RATE)
    spectrogram = stft.compute_spectrogram_magnitude_in_db(audio_data=audio_data)
    spectral_peaks = peak_extractor.extract_spectral_peaks(spectrogram=spectrogram)
    audio_fingerprints = fingerprint.__generate_fingerprints__(spectral_peaks=spectral_peaks[0])
    fingerprint_manager.__store_fingerprints__(audio_fingerprints=audio_fingerprints, audio_id=audio_id)
    print("Done Fingerprinting", audio_id)

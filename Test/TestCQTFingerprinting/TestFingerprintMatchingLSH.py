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
from Utilities import audio_manager
from Utilities import dir_manager
from Core import CQT
from Core import PeakExtractor
from Core import FingerprintGenerator
from FingerprintMatching import MatchFingerprints
from FingerprintMatching import VerifyMatches
from FingerprintMatching import Matching
import pickle
import time
import csv

# source dir
src_dir = "../../../Test_Data/Modified_Audios/Speed_Change/"
# lsh path
lsh_path = "../../../Hashes/Efode/lsh.dat"
with open(lsh_path, 'rb') as filehandle:
    # read the data as binary data stream
    lsh = pickle.load(filehandle)
# spectrogram, peak extractor and fingerprint generator objects
cqt = CQT(hop_length=64)
peak_extractor = PeakExtractor(maximum_filter_height=25, maximum_filter_width=50)
fingerprint_generator = FingerprintGenerator()
matching = Matching(lsh_path=lsh_path)
# traversing through  all modified query audio directories
for d in range(90, 102, 2):
    # retrieving wav files from each query audio directories
    wav_files = dir_manager.find_wav_files(src_dir=src_dir + str(d))
    for k in range(30, 35, 5):
        # searching for all .wav files under specified source dir
        count = 1
        # wav_files = DirManager.find_wav_files(src_dir=src_dir + str(k))
        for i in wav_files[0:10]:
            audio_fingerprints = list()
            audio_fingerprints_info = list()
            audio_id = i.split("/")[7].split(".")[0]
            # reading time series audio data re-sampled at 7KHz
            audio_data = audio_manager.load_audio(audio_path=i, sr=7000, offset=0.0, duration=k)
            # computing spectrogram
            start = time.time()
            spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=audio_data)
            # extracting spectral peaks
            spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=spectrogram)
            # generating fingerprints
            fingerprint_generator.generate_fingerprints(spectral_peaks=spectral_peaks[0],
                                                        audio_fingerprints=audio_fingerprints,
                                                        audio_fingerprints_info=audio_fingerprints_info,
                                                        r=1,
                                                        c=1,
                                                        fixed=False,
                                                        no_groups=100,
                                                        tolerance=0.31)
            matches_in_bins = matching.__match__(audio_fingerprints=audio_fingerprints,
                                                 audio_fingerprints_info=audio_fingerprints_info)
            # print(matches_in_bins)
            match = VerifyMatches.verify_matches(matches_in_bins=matches_in_bins)
            print(match, audio_id)

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
from RTreeManager import RTreeManager
from DataManager import RawDataManager
import time
import csv

# source dir
src_dir = "../../../Test_Data/Modified_Audios_12/White_Noise/"
# r_tree path
r_tree_path = "../../../Hashes/Efode/R_Tree_CQT"
# raw data path
raw_data_path = "../../../Raw_Data/Efode/Raw_Data_CQT"
result_path = "../../../Results_1/Robustness/Efode/White_Noise/"
# spectrogram, peak extractor and fingerprint generator objects
cqt = CQT(hop_length=64)
peak_extractor = PeakExtractor(maximum_filter_height=25, maximum_filter_width=50)
fingerprint_generator = FingerprintGenerator()

r_tree_index = RTreeManager.get_rtree_index(rtree_path=r_tree_path)
# raw data index
raw_data_index = RawDataManager.get_shelf_file_index(shelf_path=raw_data_path)

# traversing through  all modified query audio directories
for d in range(-5, 25, 5):
    # retrieving wav files from each query audio directories
    wav_files = dir_manager.find_wav_files(src_dir=src_dir + str(d))
    dir_manager.create_dir(result_path + str(d))
    for k in range(30, 35, 5):
        # searching for all .wav files under specified source dir
        count = 151
        # wav_files = DirManager.find_wav_files(src_dir=src_dir + str(k))
        for i in wav_files:
            audio_fingerprints = list()
            audio_fingerprints_info = list()
            audio_id = i.split("/")[7].split(".")[0]
            # reading time series audio data re-sampled at 7KHz
            audio_data = audio_manager.load_audio(audio_path=i, sr=7000, offset=0.0, duration=k)
            # computing spectrogram
            start = time.time()
            spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=audio_data)
            # extracting spectral peaks
            spectral_peaks = peak_extractor.extract_spectral_peaks(spectrogram=spectrogram)
            # generating fingerprints
            fingerprint_generator.generate_fingerprints(spectral_peaks=spectral_peaks[0],
                                                        audio_fingerprints=audio_fingerprints,
                                                        audio_fingerprints_info=audio_fingerprints_info,
                                                        r=1,
                                                        c=1,
                                                        fixed=False,
                                                        no_groups=100,
                                                        tolerance=0.31)
            # matching fingerprints
            matches_in_bins = MatchFingerprints.match_fingerprints(rtree_index=r_tree_index,
                                                                   raw_data_index=raw_data_index,
                                                                   audio_fingerprints=audio_fingerprints,
                                                                   audio_fingerprints_info=audio_fingerprints_info,
                                                                   tolerance=0.31)
            # verifying matches
            match = VerifyMatches.verify_matches(matches_in_bins=matches_in_bins)
            #print(match, audio_id)
            end = time.time()
            result = None
            if match[0] == "No Match":
                result = "False Negative"
            else:
                if audio_id == match[0]:
                    result = "True Positive"
                else:
                    result = "False Positive"
            row = [count, audio_id, match[0], result, end - start, match[1]]
            with open(result_path + str(d)+"/"+str(k) + "_sec.csv", 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            print("Seq", "Requested With; ", "Response; ", "Result Tag;", "Execution Time;",
                  "Number of Matched Hashes;")
            print(count, audio_id, match[0], result, end - start, match[1])
            count += 1


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
from Core import FingerprintGenerator
from Core import PeakExtractor
from Utilities import audio_manager
from Utilities import dir_manager
from LSH import LSH
import pickle

# source dir
src_dir = "../../../Test_Data/Reference_Audios"
# lsh path
lsh_path = "../../../Hashes/Efode/lsh.dat"
# spectrogram
spectrogram = CQT(hop_length=64)
# peak extractor
peak_extractor = PeakExtractor(maximum_filter_height=25, maximum_filter_width=50)
# fingerprint generator
fingerprint_generator = FingerprintGenerator()
# locality sensitive hashing
lsh = LSH(1,32, 2)
# searching for all .mp3 files under specified source dir
reference_audios = dir_manager.find_mp3_files(src_dir=src_dir)
# fingerprinting files
iter = 0
for i in reference_audios[0:10]:
    # list to store audio fingerprints and raw info about audio fingerprints
    audio_fingerprints = list()
    audio_fingerprints_info = list()
    # audio id
    audio_id = i.split("/")[5].split(".")[0]
    # time series audio data
    audio_data = audio_manager.load_audio(audio_path=i, sr=7000)
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

    fingerprint_index = 0
    for j in audio_fingerprints:
        row = [audio_id] + audio_fingerprints_info[fingerprint_index]
        print(row)
        print(j)
        lsh.__setitem__(j, row)
        fingerprint_index += 1
    print("Done With Fingerprinting ", iter)
    iter += 1
with open(lsh_path, 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(lsh, filehandle)

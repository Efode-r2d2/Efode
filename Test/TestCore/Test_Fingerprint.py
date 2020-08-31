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
from Core import Fingerprint
from Core import CQT
from Core import PeakExtractor
from Utilities import audio_manager
from Utilities import dir_manager

# audios test directory
src_dir = "../../../Test_Data/Reference_Audios"
# constant q transform
cqt = CQT(sr=700, hop_length=32, n_bins=84, bins_per_octave=24, f_min=27.3)
# instantiating an object for peak extraction
peak_extractor = PeakExtractor(maximum_filter_height=25, maximum_filter_width=50)
# instantiating an object for fingerprinting
fingerprint = Fingerprint(frames_per_second=219,
                          target_zone_width=1,
                          target_zone_center=4,
                          tolerance=0.0)
# finding all .mp3 audios from reference audios directory
mp3_files = dir_manager.find_mp3_files(src_dir=src_dir)
# loading an audio file
audio_data = audio_manager.load_audio(audio_path=mp3_files[0], offset=10.0, duration=10.0)
print(audio_data)
spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=audio_data)
print(spectrogram.shape)
spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=spectrogram)
print(spectral_peaks)
audio_fingerprints = fingerprint.__generate_fingerprints__(spectral_peaks=spectral_peaks[0])
print(audio_fingerprints)

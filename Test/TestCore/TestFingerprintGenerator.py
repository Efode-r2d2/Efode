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
from Core import Spectrogram
from Core import PeakExtractor
from Core import FingerprintGenerator
from Utilities import AudioManager
from Utilities import DirManager
from Utilities import GraphManager

# source directory
src_dir = "../../../Test_Data/Reference_Audios"
# spectrogram, peak extractor, fingerprint generator objects
stft = Spectrogram(hop_length=32)
peak_extractor = PeakExtractor()
fingerprint_generator = FingerprintGenerator()
# searching for all .mp3 files under a given source dir
mp3_files = DirManager.find_mp3_files(src_dir=src_dir)
# reading time series audio data re-sampled at 7KHz for a given audio portion specified with offset and duration
# parameters
audio_data = AudioManager.load_audio(audio_path=mp3_files[0], offset=10.0, duration=10.0)
# computing spectrogram
spectrogram = stft.compute_stft_magnitude_in_db(audio_data=audio_data)
# extracting spectral peaks
spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=spectrogram)
# generate fingerprints
audio_fingerprints = list()
audio_fingerprints_info = list()
fingerprint_generator.generate_fingerprints(spectral_peaks=spectral_peaks[0],
                                            audio_fingerprints=audio_fingerprints,
                                            audio_fingerprints_info=audio_fingerprints_info)
# generated fingerprints
print(audio_fingerprints)

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
from Core import STFT
from Core import PeakExtractor
from Utilities import AudioManager
from Utilities import DirManager
from Utilities import GraphManager

# source directory for reference audios
ref_dir = "../../../Test_Data/Ref_Audios"
# source directory for query audios
query_dir = "../../../Test_Data/Query_Audios/Time_Stretched/106"
# spectrogram and peak extractor objects
cqt = CQT(hop_length=128)
stft = STFT(hop_length=32)
# peak extractor for cqt
peak_extractor = PeakExtractor(maximum_filter_width=20, maximum_filter_height=10)
# peak extractor for stft
peak_extractor_2 = PeakExtractor(maximum_filter_width=150, maximum_filter_height=75)
# reference audios
reference_audios = DirManager.find_wav_files(src_dir=ref_dir)
# query audios
query_audios = DirManager.find_wav_files(src_dir=query_dir)
# time series audio data of reference audio
reference_audio_data = AudioManager.load_audio(audio_path=reference_audios[0])
# time series audio data of query audio
query_audio_data = AudioManager.load_audio(audio_path=query_audios[0])
# computing cqt based spectrogram of reference audio
reference_cqt_spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=reference_audio_data)
# computing stft based spectrogram of reference audio
reference_stft_spectrogram = stft.compute_stft_magnitude_in_db(audio_data=reference_audio_data)
# computing cqt based spectrogram of query audio
query_cqt_spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=query_audio_data)
# computing stft based spectrogram of reference audio
query_stft_spectrogram = stft.compute_stft_magnitude_in_db(audio_data=query_audio_data)
# extract spectral peaks from cqt based spectrogram of reference audio
reference_cqt_spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=reference_cqt_spectrogram)
# extract spectral peaks from stft based spectrogram of reference audio
reference_stft_spectral_peaks = peak_extractor_2.extract_spectral_peaks_2(spectrogram=reference_stft_spectrogram)
# extracting spectral peaks from cqt based spectrogram of query audio
query_cqt_spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=query_cqt_spectrogram)
# extracting spectral peaks from stft based spectrogram of query audio
query_stft_spectral_peaks = peak_extractor_2.extract_spectral_peaks_2(spectrogram=query_stft_spectrogram)

# display spectrogram along with extracted spectral peaks
GraphManager.display_spectrogram_peaks_2(spectrogram=reference_cqt_spectrogram,
                                         spectral_peaks_x=reference_cqt_spectral_peaks[1],
                                         spectral_peaks_y=reference_cqt_spectral_peaks[2],
                                         spectral_peaks_x_2=query_cqt_spectral_peaks[1],
                                         spectral_peaks_y_2=query_cqt_spectral_peaks[2])
GraphManager.display_spectrogram_peaks_2(spectrogram=reference_stft_spectrogram,
                                         spectral_peaks_x=reference_stft_spectral_peaks[1],
                                         spectral_peaks_y=reference_stft_spectral_peaks[2],
                                         spectral_peaks_x_2=query_stft_spectral_peaks[1],
                                         spectral_peaks_y_2=query_stft_spectral_peaks[2])

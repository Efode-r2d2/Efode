from Utilities import dir_manager
from Utilities import audio_manager
from Core import STFT
from Core import PeakExtractor
from Core import Fingerprint
from DataManager import DataManager
import time

# source directory for query audios
src_dir = "../../../Test_Data/Modified_Audios/Speed_Change/94"
# retrieving all query audios under specified directory
query_audios = dir_manager.find_wav_files(src_dir=src_dir)
# an object for computing stft based spectrogram
stft = STFT(n_fft=1024, hop_length=32, sr=700)
# an object to extract spectral peaks from stft based spectrogram
peak_extractor = PeakExtractor(maximum_filter_width=150, maximum_filter_height=75)
# an object to generate quad based audio fingerprints
fingerprint_generator = Fingerprint(target_zone_width=1, target_zone_center=2, tolerance=0.31)
# DataManager object
data_manager = DataManager(db_path="../../../Hashes/Efode/Efode.db")
for i in query_audios:
    print(i)
    # loading a time series audio data from one of the query audio

    audio_data = audio_manager.load_audio(audio_path=i,
                                          sr=7000,
                                          offset=10.0,
                                          duration=30.0)
    # computing stft based spectrogram of time series audio data

    spectrogram = stft.compute_stft_magnitude_in_db(audio_data=audio_data)
    # extracting spectral peaks from STFT based spectrogram
    spectral_peaks = peak_extractor.extract_spectral_peaks_2(spectrogram=spectrogram)
    # generate quad based fingerprints

    audio_fingerprints = fingerprint_generator.__generate_fingerprints__(spectral_peaks=spectral_peaks[0],
                                                                         spectrogram=spectrogram, n=100)
    # query matches
    start = time.time()
    data_manager.__query__(audio_fingerprints=audio_fingerprints, spectral_peaks=spectral_peaks[0], vThreshold=0.3)
    print(time.time()-start)

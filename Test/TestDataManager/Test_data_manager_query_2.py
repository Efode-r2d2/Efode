from Utilities import dir_manager
from Utilities import audio_manager
from Core import STFT
from Core import PeakExtractor
from Core import Fingerprint
from DataManager import DataManager
import time

# source directory for query audios
src_dir = "../../../Test_Data/Modified_Audios/Pitch_Shifted/100/"
# retrieving all query audios under specified source directory
query_audios = dir_manager.find_wav_files(src_dir=src_dir)
# STFT based spectrogram object
stft = STFT(n_fft=1024, hop_length=32, sr=7000)
# peak extractor object
peak_extractor = PeakExtractor(maximum_filter_width=150, maximum_filter_height=75)
# fingerprint generator object
fingerprint_generator = Fingerprint(
    frames_per_second=219,
    target_zone_width=2,
    target_zone_center=4,
    number_of_triplets_per_second=36,
    tolerance=0.17)
# fingerprint manager object
data_manager = DataManager(db_path="../../../Databases/Efode_Test_1.db")
for i in query_audios:
    audio_data = audio_manager.load_audio(audio_path=i, sr=7000, offset=0.0, duration=30.0)
    spectrogram = stft.compute_spectrogram_magnitude_in_db(audio_data=audio_data)
    spectral_peaks = peak_extractor.extract_spectral_peaks(spectrogram=spectrogram)
    audio_fingerprints = fingerprint_generator.generate_fingerprints(spectral_peaks=spectral_peaks[0],
                                                                     spectrogram=spectrogram)
    start = time.time()
    match = data_manager.query_audio(audio_fingerprints=audio_fingerprints,spectral_peaks=spectral_peaks[0])
    end = time.time()
    print(i, match, end - start)

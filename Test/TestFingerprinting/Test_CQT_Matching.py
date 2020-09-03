from Core import CQT
from Core import Fingerprint
from Core import PeakExtractor
from Utilities import audio_manager
from Utilities import dir_manager
from DataManager import RawDataManager
from RTreeManager import RTreeManager
from FingerprintMatching import MatchFingerprints
from FingerprintMatching import VerifyMatches
import time

# defining constants

# defining constants
SAMPLING_RATE = 7000  # sampling rate
HOP_LENGTH = 64  # hop length
MAXIMUM_FILTER_WIDTH = 50  # maximum filter width
MAXIMUM_FILTER_HEIGHT = 20  # maximum filter height
FRAMES_PER_SECOND = 219  # number of audio frames for one second audio duration
TARGET_ZONE_WIDTH = 1  # width of the target zone in seconds
TARGET_ZONE_CENTER = 1  # center of the target zone in seconds
TOLERANCE = 0.31  # maximum allowed tolerance for both pitch shifting and time stretching

# source directory for reference audios
src_dir = "../../../Test_Data/Modified_Audios/Speed_Change/"
r_tree = "../../../Hashes/Efode/CQT_Test"
# raw_data_path
shelf = "../../../Raw_Data/Efode/CQT_Test"
# r_tree index
r_tree_index = RTreeManager.get_rtree_index(rtree_path=r_tree)
# raw data index
raw_data_index = RawDataManager.get_shelf_file_index(shelf_path=shelf)

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
    Running through all directories in a given audio effect. 
    For these experiments we will start with speed change and finalize the experiment 
    by using noise added query audios
'''
for i in range(80, 132, 2):
    # retrieving all query audios under a give directory
    query_audios = dir_manager.find_wav_files(src_dir=src_dir + str(i))
    for j in query_audios:
        start = time.time()
        # loading a 30 second time series audio data
        audio_data = audio_manager.load_audio(audio_path=j, sr=SAMPLING_RATE, offset=0.0, duration=30.0)
        # computing the spectrogram for a given time series audio data
        spectrogram = cqt.compute_cqt_magnitude_in_db(audio_data=audio_data)
        # extracting spectral peaks from a given spectrogram
        spectral_peaks = peak_extractor.extract_spectral_peaks(spectrogram=spectrogram)
        # applying geometric hashing based fingerprinting on extracted spectral peaks
        fingerprints = fingerprint.generate_fingerprints(spectral_peaks=spectral_peaks[0])
        # matching fingerprints
        matches_in_bins = MatchFingerprints.match_fingerprints(rtree_index=r_tree_index, raw_data_index=raw_data_index,
                                                               fingerprints=fingerprints, tolerance=TOLERANCE)
        # verifying matches
        match = VerifyMatches.verify_matches(matches_in_bins=matches_in_bins)
        end = time.time()
        print(match, j, end - start)

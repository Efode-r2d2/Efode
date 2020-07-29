from Utilities import DirManager
from Utilities import AudioManager
from Core import CQT
from Core import PeakExtractor
from Core import Fingerprint

# defining constants
SAMPLING_RATE = 700  # sampling rate
HOP_LENGTH = 32  # hop length
MAXIMUM_FILTER_WIDTH = 50  # maximum filter width
MAXIMUM_FILTER_HEIGHT = 25  # maximum filter height
FRAMES_PER_SECOND = 219  # number of audio frames for one second audio duration
TARGET_ZONE_WIDTH = 1  # width of the target zone in seconds
TARGET_ZONE_CENTER = 2  # center of the target zone in seconds
TOLERANCE = 0.0  # maximum allowed tolerance for both pitch shifting and time stretching

# source directory for reference audios
src_dir = "../../../Test_Data/Reference_Audios"
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


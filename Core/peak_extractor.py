import numpy as np
from operator import itemgetter
from skimage.feature import peak_local_max
from scipy.ndimage import maximum_filter
from scipy.ndimage import minimum_filter


class PeakExtractor(object):
    def __init__(self, filter_dim=10, minimum_amp_in_db=-60, num_peaks=60
                 , maximum_filter_height=75, minimum_filter_height=3,
                 maximum_filter_width=150, minimum_filter_width=3):
        """

        :param filter_dim:
        :param minimum_amp_in_db:
        :param num_peaks:
        :param maximum_filter_height:
        :param minimum_filter_height:
        :param maximum_filter_width:
        :param minimum_filter_width:
        """
        self.filter_dim = filter_dim
        self.minimum_amp_in_db = minimum_amp_in_db
        self.num_peaks = num_peaks
        self.spectral_peaks = None
        self.time_indices = None
        self.frequency_indices = None
        self.maximum_filter_height = maximum_filter_height
        self.maximum_filter_width = maximum_filter_width
        self.minimum_filter_height = minimum_filter_height
        self.minimum_filter_width = minimum_filter_width

    def extract_spectral_peaks_1(self, spectrogram):
        """

        :param spectrogram:
        :return:
        """
        local_max_values = peak_local_max(image=spectrogram,
                                          min_distance=self.filter_dim,
                                          indices=False,
                                          threshold_abs=self.minimum_amp_in_db)
        self.frequency_indices, self.time_indices = np.where(local_max_values)
        self.spectral_peaks = list(zip(self.time_indices, self.frequency_indices))
        self.spectral_peaks.sort(key=itemgetter(0))
        return self.spectral_peaks, self.time_indices, self.frequency_indices

    def extract_spectral_peaks_2(self, spectrogram):
        """

        :param spectrogram:
        :return:
        """
        # computing local maximum points with the specified maximum filter dimension
        local_max_values = maximum_filter(input=spectrogram, size=(self.maximum_filter_height,
                                                                   self.maximum_filter_width))
        # extracting time and frequency information for local maximum points
        j, i = np.where(spectrogram == local_max_values)
        peaks = list(zip(i, j))
        # computing local minimum points with specified minimum filter dimension
        local_min_values = minimum_filter(input=spectrogram, size=(self.minimum_filter_height,
                                                                   self.minimum_filter_width))
        # extracting time and frequency information for local minimums
        k, m = np.where(spectrogram == local_min_values)
        lows = list(zip(m, k))
        # avoiding spectral points with are both local maximum and local minimum
        spectral_peaks = list(set(peaks) - set(lows))
        # time and frequency information for extracted spectral peaks
        time_indices = [i[0] for i in spectral_peaks]
        freq_indices = [i[1] for i in spectral_peaks]
        spectral_peaks.sort(key=itemgetter(0))
        return spectral_peaks, time_indices, freq_indices

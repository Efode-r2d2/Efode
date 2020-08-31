from operator import itemgetter
import numpy as np
from scipy.ndimage import maximum_filter
from scipy.ndimage import minimum_filter


class PeakExtractor(object):
    """
    A class to extract spectral peaks given spectrogram of an audio.

    Attributes:
        maximum_filter_width (int): Width of maximum filter.
        maximum_filter_height (int): Height of maximum filter.
        minimum_filter_width (int): Width of minimum filter.
        minimum_filter_height (int): Height of minimum filter.

    """
    def __init__(self, maximum_filter_height=75, minimum_filter_height=3,
                 maximum_filter_width=150, minimum_filter_width=3):
        """
        A constructor for PeakExtractor class.

        Parameters:
            maximum_filter_width (int): Width of maximum filter.
            maximum_filter_height (int): Height of maximum filter.
            minimum_filter_width (int): Width of minimum filter.
            minimum_filter_height (int): Height of minimum filter.

        """
        self.maximum_filter_height = maximum_filter_height
        self.maximum_filter_width = maximum_filter_width
        self.minimum_filter_height = minimum_filter_height
        self.minimum_filter_width = minimum_filter_width

    def extract_spectral_peaks(self, spectrogram):
        """
        A method to extract spectral peaks given a spectrogram of an audio. In this method
        a maximum filter is applied to extract all local maxima's with in a given filter
        size and a minimum filter with a filter dimensions smaller than the maximum filter
        is applied to extract all the local minima's. Finally spectral peaks are computed by
        subtracting the results of the minimum filter from the results of the maximum filter.

        Parameters:
            spectrogram (numpy.ndarray): Time-frequency representation of an audio.

        Returns:
            List : List of spectral peaks.
            List : List of time indices.
            List : List of frequency indices.

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

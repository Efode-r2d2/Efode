from itertools import combinations
from bisect import bisect_left
from heapq import nlargest


class Fingerprint(object):
    """
    A class to generate audio fingerprints based on the association of three spectral peaks.

    Attributes:
        frames_per_second (int): Number of frames per second.
        target_zone_width (int): Width of the target zone.
        target_zone_center (int): Center of the target zone from the root peak called P1.
        number_of_triplets_per_second (int): Number of strong triplets per second.
        tolerance (float): Maximum allowed tempo and pitch modifications.
        min_frame_number (int): The minimum frame number to be included in the target zone.
        max_frame_number (int): The maximum frame number to be included in the target zone.

    """

    def __init__(self, frames_per_second=219, target_zone_width=1, target_zone_center=4,
                 number_of_triplets_per_second=9, tolerance=0.31):
        """
        A constructor for Fingerprint Class.

        Parameters:
            frames_per_second (int): Number of frames per second.
            target_zone_width (int): Width of the target zone.
            target_zone_center (int): Center of the target zone from the root peak P1.
            number_of_triplets_per_second (int): Number of strong triplets per second.
            tolerance (float): Maximum allowed modification both along tempo and pitch axis.

        """
        self.frames_per_second = frames_per_second
        self.target_zone_width = target_zone_width
        self.target_zone_center = target_zone_center
        self.number_of_triplets_per_second = number_of_triplets_per_second
        self.tolerance = tolerance
        self.min_frame_number = ((self.target_zone_center - self.target_zone_width / 2) * self.frames_per_second) / (
                1 + self.tolerance)
        self.max_frame_number = ((self.target_zone_center + self.target_zone_width / 2) * self.frames_per_second) / (
                1 - self.tolerance)

    def generate_fingerprints(self, spectral_peaks, spectrogram):
        """
        A method to generate audio fingerprints based on the association of three spectral peaks.

        Parameters:
            spectral_peaks (List): List of spectral peaks extracted from spectrogram of an audio.
            spectrogram (numpy.ndarray): Time-frequency representation of an audio.

        Returns:
            List : List of audio fingerprinting.

        """
        valid_triplets = self.__validate_triplets(spectral_peaks=spectral_peaks)
        strong_triplets = self.__n_strongest_triplets(spectrogram=spectrogram, valid_triplets=valid_triplets)
        audio_fingerprints = self.__geometric_hash(strong_triplets=strong_triplets)
        return audio_fingerprints

    def __validate_triplets(self, spectral_peaks):
        """
        A method to validate triplets based on a pre-defined conditions.

        Parameters:
            spectral_peaks (List): List of spectral peaks extracted from STFT based audio spectrogram.

        Returns:
            List : List of valid triplets.

        """
        valid_triplets = list()
        for i in spectral_peaks:
            # a target zone for a given spectral peak
            target_zone = [j for j in spectral_peaks if
                           i[0] + self.min_frame_number <= j[0] <= i[
                               0] + self.max_frame_number]
            # all triplets formed from a given target zone
            all_triplets = list(combinations(target_zone, 2))
            for j in all_triplets:
                p1 = i
                p3 = j[0]
                p2 = j[1]
                if p1[1] < p3[1] < p2[1]:
                    valid_triplets.append((p1,) + i)
        return valid_triplets

    def __find_partitions(self, valid_triplets):
        """
        A method to partition valid triplets into one second duration.

        Parameters:
            valid_triplets (List): List of valid triplets.

        Returns:
            List : List of triplets chunked into one second duration.

        """
        b_l = bisect_left
        last_x = valid_triplets[-1][0][0]
        num_partitions = last_x // self.number_of_triplets_per_second
        # creates a tuple of same form as the Quad namedtuple for bisecting
        q = lambda x: ((x,), (), (), ())
        partitions = [b_l(valid_triplets, q(i * self.number_of_triplets_per_second)) for i in range(num_partitions)]
        partitions.append(len(valid_triplets))
        return partitions

    def __n_strongest_triplets(self, spectrogram, valid_triplets):
        """
        A method to select only specified number of strong triplets per a second of audio.

        Parameters:
            spectrogram (numpy.ndarray): Time-frequency representation of an audio.
            valid_triplets (List): list of valid triplets.

        Returns:
            List : list of specified number of triplets per second of audio.

        """
        strongest = []
        partitions = self.__find_partitions(valid_triplets=valid_triplets)
        key = lambda p: (spectrogram[p[1][1]][p[1][0]])
        for i in range(1, len(partitions)):
            start = partitions[i - 1]
            end = partitions[i]
            strongest += nlargest(self.number_of_triplets_per_second, valid_triplets[start:end], key)
        return strongest

    def __geometric_hash(self, strong_triplets):
        """
        A method to generate hash of a triplet using a technique called geometric hashing.

        Parameters:
            strong_triplets (List): List of strong triplets.

        Returns:
            List : List of hashes of triplets along with their raw data.

        """
        audio_fingerprints = list()
        for i in strong_triplets:
            p1 = i[0]
            p2 = i[2]
            p3 = i[1]
            # calculate the new value of p3x
            p3x_new = round(((p3[0] - p1[0]) / (p2[0] - p1[0])), 3)
            # calculate the new value of p3y
            p3y_new = round(((p3[1] - p1[1]) / (p2[1] - p1[1])), 3)
            # filtering fingerprints based on the
            if p3x_new > (self.min_frame_number / self.max_frame_number) - 0.02:
                audio_fingerprints.append([[p3x_new, p3y_new], [p1[0], p1[1], p2[0], p2[1]]])
        return audio_fingerprints

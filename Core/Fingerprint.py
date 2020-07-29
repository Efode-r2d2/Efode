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
from itertools import combinations


def __validate_triplets__(root_peak, all_triplets, valid_triplets):
    for i in all_triplets:
        p1 = root_peak
        p3 = i[0]
        p2 = i[1]
        if p1[0] < p3[0] < p2[0] and p1[1] < p3[1] < p2[1]:
            valid_triplets.append(i)


class Fingerprint(object):
    def __init__(self, frames_per_second=219, target_zone_width=1, target_zone_center=4, tolerance=0.31):
        self.frames_per_second = frames_per_second
        self.target_zone_width = target_zone_width
        self.target_zone_center = target_zone_center
        self.tolerance = tolerance
        self.min_frame_number = ((self.target_zone_center - self.target_zone_width / 2) * self.frames_per_second) / (
                1 + self.tolerance)
        self.max_frame_number = ((self.target_zone_center + self.target_zone_width / 2) * self.frames_per_second) / (
                1 - self.tolerance)

    def __generate_fingerprints__(self, spectral_peaks):
        audio_fingerprints = list()
        for i in spectral_peaks:
            # list object to hold all valid triplets with in a given target zone
            valid_triplets = list()
            # a target zone for a given spectral peak
            target_zone = [j for j in spectral_peaks if
                           i[0] + self.min_frame_number <= j[0] <= i[
                               0] + self.max_frame_number]
            # all triplets formed from a given target zone
            all_triplets = list(combinations(target_zone, 2))
            # validate triplets formed form a given target zone and identify the valid ones
            if len(all_triplets) > 0:
                __validate_triplets__(root_peak=i, all_triplets=all_triplets, valid_triplets=valid_triplets)
            if len(valid_triplets) > 0:
                self.__geometric_hash__(root_peak=i, valid_triplets=valid_triplets,
                                        audio_fingerprints=audio_fingerprints)
        return audio_fingerprints

    def __geometric_hash__(self, root_peak, valid_triplets, audio_fingerprints):
        for i in valid_triplets:
            p1 = root_peak
            p2 = i[1]
            p3 = i[0]
            # calculate the new value of p3x
            p3x_new = round(((p3[0] - p1[0]) / (p2[0] - p1[0])), 3)
            # calculate the new value of p3y
            p3y_new = round(((p3[1] - p1[1]) / (p2[1] - p1[1])), 3)
            # filtering fingerprints based on the
            if p3x_new > (self.min_frame_number / self.max_frame_number) - 0.02:
                audio_fingerprints.append([[p3x_new, p3y_new], [p1[0], p1[1], p2[0], p2[1]]])

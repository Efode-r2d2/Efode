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


class FingerprintGenerator(object):
    def __init__(self):
        pass

    def generate_fingerprints(self, spectral_peaks,
                              audio_fingerprints,
                              audio_fingerprints_info,
                              frames_per_sec=219,
                              r=1,
                              c=4,
                              fixed=False,
                              tolerance=0.0,
                              no_groups=2):
        min_frame = ((c - r / 2) * frames_per_sec) / (1 + tolerance)
        max_frame = ((c + r / 2) * frames_per_sec) / (1 - tolerance)
        for i in range(len(spectral_peaks)):
            valid_triplets = list()
            target_zone = [j for j in spectral_peaks if
                           spectral_peaks[i][0] + min_frame <= j[0] <= spectral_peaks[i][0] + max_frame]
            triplets = list(combinations(target_zone, 2))
            if len(triplets) > 0:
                self.generate_valid_triplets(spectral_peaks[i], triplets, valid_triplets, fixed=fixed, no_groups=no_groups)
            if len(valid_triplets) > 0:
                self.geometric_hashing(spectral_peaks[i], valid_triplets, audio_fingerprints=audio_fingerprints,
                                       audio_fingerprints_info=audio_fingerprints_info, min_frame=min_frame, max_frame=max_frame)

    def generate_valid_triplets(self,
                                anchor,
                                combs,
                                valid_triplets,
                                fixed=False,
                                no_groups=2):
        count = 0
        for i in combs:
            a = anchor
            c = i[0]
            b = i[1]
            condition1 = False
            condition2 = False
            if a[0] < c[0] < b[0]:
                condition1 = True
            if a[1] < c[1] < b[1]:
                condition2 = True
            if condition1 and condition2:
                if fixed:
                    valid_triplets.append(i)
                    count += 1
                    if count > no_groups:
                        return
                else:
                    valid_triplets.append(i)

    def geometric_hashing(self,
                          anchor,
                          valid_triplets,
                          audio_fingerprints,
                          audio_fingerprints_info,
                          min_frame,
                          max_frame):
        for i in valid_triplets:
            a = anchor
            b = i[1]
            c = i[0]
            cx_new = round(((c[0] - a[0]) / (b[0] - a[0])), 3)
            cy_new = round(((c[1] - a[1]) / (b[1] - a[1])), 3)
            if cx_new > (min_frame / max_frame) - 0.02:
                audio_fingerprints.append([cx_new, cy_new])
                audio_fingerprints_info.append([a[0], a[1], b[0], b[1]])

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
from collections import defaultdict
from RTreeManager import RTreeManager
import numpy as np


def match_fingerprints(rtree_index, raw_data_manager, audio_fingerprints, audio_fingerprints_info, tolerance=0.31):
    """

    :param rtree_index:
    :param raw_data_manager:
    :param audio_fingerprints:
    :param audio_fingerprints_info:
    :param tolerance:
    :return:
    """
    count = 0
    matches_in_bins = defaultdict(list)
    for i in audio_fingerprints:
        # getting raw data form query hashes
        ax_q = audio_fingerprints_info[count][0]
        ay_q = audio_fingerprints_info[count][1]
        bx_q = audio_fingerprints_info[count][2]
        by_q = audio_fingerprints_info[count][3]
        candidate_matches = RTreeManager.get_nearest_node(rtree_index, i)
        for m in candidate_matches:
            raw_data = raw_data_manager.get_data(m)
            ax_r = raw_data[1]
            ay_r = raw_data[2]
            bx_r = raw_data[3]
            by_r = raw_data[4]
            min_t_delta = 1 / (1 + tolerance)
            max_t_delta = 1 / (1 - tolerance)
            min_f_delta = 1 / (1 + tolerance)
            max_f_delta = 1 / (1 - tolerance)
            s_time = (bx_q - ax_q) / (bx_r - ax_r)
            s_freq = (by_q - ay_q) / (by_r - ay_r)
            if ay_r == 0:
                pass
            else:
                pitch_cho = ay_q / ay_r
            # first filter
            if min_t_delta < s_time < max_t_delta and min_f_delta < s_freq < max_f_delta:
                # second filter
                if 1 / (1 + tolerance) <= pitch_cho <= 1 / (1 - tolerance):
                    # third filter
                    if np.abs(ay_q - ay_r * s_freq) < 20.0:
                        matches_in_bins[raw_data[0]].append(ax_r - ax_q * s_time)
        count += 1
    return matches_in_bins

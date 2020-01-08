import threading
from RTreeManager import RTreeManager
from RawDataManager import RawDataManager
import numpy as np
import time


class Match(threading.Thread):
    def run(self, matches_in_bins, rtree_index, raw_data_index, audio_fingerprints, audio_fingerprints_info,
            tolerance=0.31):
        count = 0
        for i in audio_fingerprints:
            # getting raw data form query hashes
            ax_q = audio_fingerprints_info[count][0]
            ay_q = audio_fingerprints_info[count][1]
            bx_q = audio_fingerprints_info[count][2]
            by_q = audio_fingerprints_info[count][3]
            candidate_matches = RTreeManager.get_nearest_node(rtree_index, i)
            for m in candidate_matches:
                raw_data = RawDataManager.get_data(shelf=raw_data_index, key=m)
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
                    pitch_cho = 100
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

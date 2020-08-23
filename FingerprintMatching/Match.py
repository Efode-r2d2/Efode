import threading
from RTreeManager import RTreeManager
from DataManager import RawDataManager
import numpy as np


class Match(threading.Thread):
    def run(self, matches_in_bins, rtree_index, raw_data_index, fingerprints, tolerance=0.31):
        for i in fingerprints:
            # getting raw data form query hashes
            p1x_q = i[1][0]
            p1y_q = i[1][1]
            p2x_q = i[1][2]
            p2y_q = i[1][3]

            min_t_delta = 1 / (1 + tolerance)
            max_t_delta = 1 / (1 - tolerance)
            min_f_delta = 1 / (1 + tolerance)
            max_f_delta = 1 / (1 - tolerance)

            candidate_matches = RTreeManager.get_nearest_node(rtree_index, i[0])
            for m in candidate_matches:
                raw_data = RawDataManager.get_data(shelf=raw_data_index, key=m)
                p1x_r = raw_data[1]
                p1y_r = raw_data[2]
                p2x_r = raw_data[3]
                p2y_r = raw_data[4]

                s_time = (p2x_q - p1x_q) / (p2x_r - p1x_r)
                s_freq = (p2y_q - p1y_q) / (p2y_r - p1y_r)
                if p1y_r == 0:
                    pitch_cho = 100
                else:
                    pitch_cho = p1y_q / p1y_r
                # first filter
                if min_t_delta < s_time < max_t_delta and min_f_delta < s_freq < max_f_delta:
                    # second filter
                    if 1 / (1 + tolerance) <= pitch_cho <= 1 / (1 - tolerance):
                        # third filter
                        if np.abs(p1y_q - p1y_r * s_freq) < 20.0:
                            matches_in_bins[raw_data[0]].append(p1x_r - p1x_q * s_time)

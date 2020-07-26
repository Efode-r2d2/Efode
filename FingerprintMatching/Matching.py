import pickle
import numpy as np
from LSH import ManageLSH
from collections import defaultdict


class Matching:
    def __init__(self, lsh_path):
        self.lsh = ManageLSH.__loadlsh__(lsh_path=lsh_path)

    def __match__(self, audio_fingerprints, audio_fingerprints_info, tolerance=0.1):
        count = 0
        matches_in_bins = defaultdict(list)
        for i in audio_fingerprints:
            # getting raw data form query hashes
            ax_q = audio_fingerprints_info[count][0]
            ay_q = audio_fingerprints_info[count][1]
            bx_q = audio_fingerprints_info[count][2]
            by_q = audio_fingerprints_info[count][3]
            candidate_matches = self.lsh.__getitem__(i)
            for m in candidate_matches:
                ax_r = m[1]
                ay_r = m[2]
                bx_r = m[3]
                by_r = m[4]
                #vec2 = m[5]
                #similarity = self.__cosine_sim(i,vec2)
                similarity=0.91
                if similarity > 0.9:
                    min_t_delta = 1 / (1 + tolerance)
                    max_t_delta = 1 / (1 - tolerance)
                    min_f_delta = 1 / (1 + tolerance)
                    max_f_delta = 1 / (1 - tolerance)
                    s_time = (bx_q - ax_q) / (bx_r - ax_r)
                    s_freq = (by_q - ay_q) / (by_r - ay_r)
                    if ay_r == 0:
                        pitch_cho = 10
                    else:
                        pitch_cho = ay_q / ay_r
                    # first filter
                    if min_t_delta < s_time < max_t_delta and min_f_delta < s_freq < max_f_delta:
                        # second filter
                        if 1 / (1 + tolerance) <= pitch_cho <= 1 / (1 - tolerance):
                            # third filter
                            if np.abs(ay_q - ay_r * s_freq) < 20.0:
                                matches_in_bins[m[0]].append(ax_r - ax_q * s_time)
            count += 1
        return matches_in_bins

    def __cosine_sim(self,vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

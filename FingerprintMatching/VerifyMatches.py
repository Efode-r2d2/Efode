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
import numpy as np


def verify_matches(matches_in_bins):
    """

    :param matches_in_bins:
    :return:
    """
    candidate_audios = list()
    final_audios = list()
    for i in matches_in_bins:
        if len(matches_in_bins[i]) >= 10:
            candidate_audios.append(i)
    for y in candidate_audios:
        n, b = np.histogram(matches_in_bins[y], bins=10)
        final_audios.append((y, n.max(), list(n).index(n.max())))
    if len(final_audios) > 0:
        final_audios = sorted(final_audios, key=lambda x: int(x[1]), reverse=True)
        if final_audios[0][1] >= 5:
            return final_audios[0][0], final_audios[0][1]
        return "No Match", final_audios[0][1]
    else:
        return "No Match", 0

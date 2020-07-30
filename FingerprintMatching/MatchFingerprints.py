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

from FingerprintMatching.Match import Match


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def match_fingerprints(rtree_index, raw_data_index, fingerprints, tolerance=0.31):
    """

    :param fingerprints:
    :param rtree_index:
    :param raw_data_index:
    :param tolerance:
    :return:
    """
    fingerprint_chunks = list(divide_chunks(fingerprints, 100))
    matches_in_bins = defaultdict(list)
    for i in fingerprint_chunks:
        match = Match()
        match.run(matches_in_bins=matches_in_bins, rtree_index=rtree_index, raw_data_index=raw_data_index,
                  fingerprints=i, tolerance=tolerance)
    return matches_in_bins

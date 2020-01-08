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
from rtree import index
import rtree


def get_rtree_index(rtree_path):
    """

    :param rtree_path:
    :return:
    """
    p = rtree.index.Property()
    file_idx = index.Index(rtree_path, properties=p)
    return file_idx


def insert_node(rtree_index, node_id, geo_hash):
    """

    :param rtree_index:
    :param node_id:
    :param geo_hash:
    """
    rtree_index.insert(node_id, (geo_hash[0], geo_hash[1], geo_hash[0], geo_hash[1]))


def get_nearest_node(rtree_index, geo_hash):
    """

    :param rtree_index:
    :param geo_hash:
    :return:
    """
    return list(rtree_index.nearest((geo_hash[0], geo_hash[1], geo_hash[0], geo_hash[1]), 5))

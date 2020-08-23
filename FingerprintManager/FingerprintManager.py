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
from ConfigManager import ConfigManager
from DataManager import RawDataManager
from RTreeManager import RTreeManager


class FingerprintManager(object):
    def __init__(self, r_tree, shelf, config):
        self.r_tree = r_tree
        self.shelf = shelf
        self.config = config
        # r tree index
        self.r_tree_index = RTreeManager.get_rtree_index(rtree_path=self.r_tree)
        # shelf index
        self.shelf_index = RawDataManager.get_shelf_file_index(shelf_path=self.shelf)

    def __store_fingerprints__(self, audio_fingerprints, audio_id):
        """
        :param audio_fingerprints:
        :param audio_id:
        :return:
        """
        # node_id is used to identify each entry of the r_tree
        node_id = int(ConfigManager.read_config(config_file_path=self.config,
                                                section="Default",
                                                sub_section="Node_ID"))

        for i in audio_fingerprints:
            row = [audio_id] + i[1]
            RTreeManager.insert_node(rtree_index=self.r_tree_index, node_id=node_id, geo_hash=i[0])
            RawDataManager.insert_data(shelf=self.shelf_index, key=node_id, value=row)
            node_id += 1
        # updating the last node_id
        ConfigManager.write_config(config_file_path=self.config,
                                   section="Default",
                                   sub_section="Node_ID",
                                   value=str(node_id))

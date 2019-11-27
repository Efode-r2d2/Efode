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
import shelve


def get_shelf_file_index(shelf_path):
    """

    :param shelf_path:
    :return:
    """
    return shelve.open(shelf_path)


def insert_data(shelf, key, value):
    """

    :param shelf:
    :param key:
    :param value:
    """
    shelf[str(key)] = value


def insert_bulk_data(shelf, audio_id, hash_info):
    """

    :param shelf:
    :param audio_id:
    :param hash_info:
    """
    count = 0
    for i in hash_info:
        key = audio_id + "_" + count
        insert_data(key, i)
        count += 1


def get_data(shelf, key):
    """

    :param shelf:
    :param key:
    :return:
    """
    return shelf[str(key)]

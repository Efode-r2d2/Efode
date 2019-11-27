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
import configparser


def write_config(config_file_path, section, sub_section, value):
    """

    :param config_file_path:
    :param section:
    :param sub_section:
    :param value:
    """
    config = configparser.ConfigParser()
    config[section] = {}
    config[section][sub_section] = str(value)
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)


def read_config(config_file_path, section, sub_section):
    """

    :param config_file_path:
    :param section:
    :param sub_section:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config[section][sub_section]

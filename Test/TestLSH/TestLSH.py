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
from LSH import LSH
import pickle

lsh = LSH(1, 64, 2)
vec = [[0.1, 0.1], [0.15, 0.1], [0.14, 0.1], [0.2, 0.1], [0.19, 0.1], [0.3, 0.7], [0.3, 0.65]]
for i in vec:
    lsh.__setitem__(i, i)
for i in vec:
    print(lsh.__getitem__(i))
#lsh.__dumplsh__()
with open('hash2.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(lsh, filehandle)
with open('hash2.data', 'rb') as filehandle:
    # read the data as binary data stream
    lsh2 = pickle.load(filehandle)
print(lsh2.__getitem__([0.1, 0.1]))

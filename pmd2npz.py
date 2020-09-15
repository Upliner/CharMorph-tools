#!/usr/bin/python3
#############################################################################
#
# ---------- GNU-License Standardtext ---------------------------------------
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------
#
# You can find a copy of the GNU-License here:
# http://www.gnu.org/licenses/licenses.html#GPL
#
#############################################################################

import struct, re, sys, os, time, numpy
from collections import namedtuple, OrderedDict
import uuid

VERTEX = namedtuple("VERTEX", "x y z")
DELTA = namedtuple("DELTA", "index, vertex")

class PoserPmdFile(object):
    # Author of the class: Fredi Hartmann, Germany, aka ADP
    # Email : adp@mailbox.org
    def __init__(self, fh=None):
        if isinstance(fh, str):
            fh = open(fh, "rb")

        if fh is not None:
            self.filename = fh.name
            self.fh = fh  # Filehandle to read from.
            self.read_header()  # Check file-signature
        else:
            self.filename = self.fh = None

        self.num_targets = None  # No target read yet.
        self.targets = OrderedDict()  # storage for Morph-Structure

    def read_header(self):
        """
        Check file-signature.
        Raise IOError if signature is not "PZMD".
        :return: True
        """
        self.fh.seek(0)
        s = self.fh.read(4)
        if s != b"PZMD":
            raise IOError("Not a Poser PMD file")
        return True

    def _unpack(self, fmt, size):
        result = struct.unpack("!" + fmt, self.fh.read(size))
        return result[0]

    def read_all(self):
        """
        Calls read_target() and read_deltas()
        :return: None
        """
        self.read_targets()
        self.read_deltas()

    def read_targets(self):
        """
        Read all morphtargets from open file (filehandle in self.fh)
        :return: <OrderedDict>self.targets
        """
        if self.fh.closed:
            raise IOError("File '%s' is closed" % self.fh.name)

        self.fh.seek(0x10)
        self.num_targets = self._read_uint(4)

        self.targets.clear()

        for i in range(self.num_targets):
            morphname = self._read_str()
            actorname = self._read_str()
            target = self.targets.setdefault(morphname, OrderedDict())
            actor = target.setdefault(actorname, OrderedDict())
            actor["numb_deltas"] = self._read_uint(4)
            actor["morphpos"] = self._read_uint(4)

        self.read_uuids(self.fh.tell())

        return self.targets

    def read_deltas(self):
        """
        Read deltas from open file (filehandle in self.fh)
        into self.targets.

        :return: None
        """
        if self.targets is None:
            self.read_targets()

        def read_one(pos):
            result = list()
            self.fh.seek(pos)
            indexes = self._read_uint(4)
            for i in range(indexes):
                result.append(DELTA(self._read_uint(4), VERTEX(*self._read_vector())))

            return result

        for morphname, v in self.targets.items():
            for actor, data in v.items():
                data["deltas"] = read_one(data["morphpos"])

    def read_uuids(self, pos):
        """
        Read all uuids starting at file-position <pos>.
        :param pos: fileposition
        :return: None
        """
        self.fh.seek(pos)
        for name, target in self.targets.items():
            for actorname, actordata in target.items():
                actordata["UUID"] = self._read_str()

    def _read_str(self, length=1):
        strlen = self._read_uint(length)
        return self.fh.read(strlen).decode("latin1")

    def _read_int(self, size):
        if size == 1:
            return self._unpack("b", size)
        if size == 2:
            return self._unpack("h", size)
        if size == 4:
            return self._unpack("i", size)
        raise ValueError("invalid int size: " + size)

    def _read_uint(self, size):
        if size == 1:
            return self._unpack("B", size)
        if size == 2:
            return self._unpack("H", size)
        if size == 4:
            return self._unpack("I", size)
        raise ValueError("invalid int size: " + size)

    def _read_vector(self):
        return struct.unpack("!fff", self.fh.read(12))

    def _read_float(self):
        return self._unpack("f", 4)

d = PoserPmdFile(sys.argv[1])
d.read_targets()
d.read_deltas()

# Use obj2lists.py to generate lists.py
import lists

verts = numpy.zeros((lists.vertex_count,3))
for mname, mdata in d.targets.items():
    print(mname)
    idx = []
    delta = []
    for actor, data in mdata.items():
        lst = getattr(lists, actor)
        for v in data["deltas"]:
            idx.append(lst[v[0]])
            delta.append(v[1])
    numpy.savez("morphs/" + mname + ".npz", idx=numpy.array(idx,dtype=numpy.uint16), delta=numpy.array(delta,dtype=numpy.float32))

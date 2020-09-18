#!/usr/bin/python3

import sys, os, json, numpy

for fn in sys.argv[1:]:
    with open(fn, "r") as f:
        data = json.load(f)
    name, ext = os.path.splitext(fn)
    numpy.save(name+".npy", numpy.array(data, dtype=numpy.float32))


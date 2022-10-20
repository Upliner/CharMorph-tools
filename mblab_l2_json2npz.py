#!/usr/bin/python3

import sys, json, numpy

if len(sys.argv) < 3:
    print("Usage: mblab_l2_json2npz.py outdir/ file1.json [file2.json...]")
    exit()

outdir = sys.argv[1]

for fname in sys.argv[2:]:
    with open(fname, "r") as f:
        data = json.load(f)
    for name, morph in data.items():
        idx = numpy.empty(len(morph), dtype=numpy.uint16)
        delta = numpy.empty((len(morph),3), dtype=numpy.float32)
        for i, val in enumerate(morph):
            idx[i] = val[0]
            delta[i] = val[1:]
        numpy.savez(outdir + name, idx=idx, delta=delta)

#!/usr/bin/python3

import os, sys, json, numpy

if len(sys.argv) < 2:
    print("Usage: mblab_l2_json2npz.py infile.json [outfile.npz]")
    exit()

with open(sys.argv[1], "r", encoding="ascii") as f:
    d = json.load(f)

if len(sys.argv)>2:
    outfile = sys.argv[2]
else:
    outfile = os.path.splitext(sys.argv[1])[0] + ".npz"

numpy.savez(outfile,
    idx=numpy.array(list(d.keys()), dtype=numpy.uint16),
    bbox=numpy.array(list(d.values()), dtype=numpy.uint16),
)

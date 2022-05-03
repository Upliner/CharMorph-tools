#!/usr/bin/python3

import os, sys, json, numpy

if len(sys.argv) < 2:
    print("Usage: mblab_l2_json2npz_pack.py infile.json [outfile.npz]")
    exit()

names = bytearray()
cnt = []
idx = []
delta = []
#full = []


with open(sys.argv[1], "r", encoding="ascii") as f:
    data = json.load(f)

for name, morph in sorted(data.items()):
    if name.startswith("Expressions_"):
        name = name[12:]
    if len(names)>0:
        names.append(0)
    names.extend(name.encode("ascii"))
    cnt.append(len(morph))
    for i, val in enumerate(morph):
        idx.append(val[0])
        delta.append(val[1:])

if len(sys.argv)>2:
    outfile = sys.argv[2]
else:
    outfile = os.path.splitext(sys.argv[1])[0] + ".npz"

data = {
    "names": names,
    "cnt": numpy.array(cnt, dtype=numpy.int16),
    "idx": numpy.array(idx, dtype=numpy.uint16),
    "delta": numpy.array(delta, dtype=numpy.float32),
}
numpy.savez(outfile, **data)

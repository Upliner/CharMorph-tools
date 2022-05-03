#!/usr/bin/python3

import os, sys, numpy

verts_cnt = None
if len(sys.argv)>1:
    verts_cnt=int(sys.argv[1])

names = bytearray()
cnt = []
idx = []
delta = []
full = []


for file in sorted(os.listdir(".")):
    if not file.endswith(".npz") and not file.endswith(".npy"):
        continue
    z = numpy.load(file)

    if len(names)>0:
        names.append(0)
    names.extend(file[:-4].encode("ascii"))

    if isinstance(z, numpy.ndarray):
        cnt.append(-1)
        full.append(z)
    else:
        curcnt = len(z["idx"])
        if verts_cnt and curcnt>=verts_cnt*0.80:
            result = numpy.zeros((verts_cnt, 3), dtype=numpy.float32)
            result[z["idx"]] = z["delta"]
            cnt.append(-1)
            full.append(result)
        else:
            cnt.append(curcnt)
            idx.extend(z["idx"])
            delta.extend(z["delta"])

data = {
    "names": names,
    "cnt": numpy.array(cnt, dtype=numpy.int16),
    "idx": numpy.array(idx, dtype=numpy.uint16),
    "delta": numpy.array(delta, dtype=numpy.float32),
}
if full:
    data["full"] = full

numpy.savez("__pack__.npz", **data)

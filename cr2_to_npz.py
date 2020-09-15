#!/usr/bin/python3

import os, sys, numpy

act = {}
actname = None
morphs = None
morph = None

lst = None

# Use obj2lists.py to generate lists.py
import lists

with open(sys.argv[1],"r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("actor "):
            name = line[6:-2]
            morphs = {}
            morph = None
            act[name] = morphs
            lst = getattr(lists, name)
        if morphs is None:
            continue
        if line.startswith("targetGeom "):
            name = line[11:]
            morph = ([],[])
            morphs[name] = morph
        if morph is None:
            continue
        if not line.startswith("d "):
            continue
        vals = line[2:].split(" ")
        morph[0].append(lst[int(vals[0])])
        morph[1].append((float(vals[1]),float(vals[2]),float(vals[3])))

morphs = {}

for aname, adata in act.items():
    for mname, morph in adata.items():
        if len(morph[0]) == 0:
            continue
        m2 = morphs.get(mname,([],[]))
        m2[0].extend(morph[0])
        m2[1].extend(morph[1])
        morphs[mname] = m2
        #os.makedirs("act/" + aname, exist_ok=True)
        #numpy.savez("act/" + aname + "/" + mname + ".npz", idx = numpy.array(morph[0],dtype=numpy.uint32), delta = numpy.array(morph[1],dtype=numpy.float32))

for mname, morph in morphs.items():
    numpy.savez("morphs2/" + mname + ".npz", idx = numpy.array(morph[0],dtype=numpy.uint16), delta = numpy.array(morph[1],dtype=numpy.float32))

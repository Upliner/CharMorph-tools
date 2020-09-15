#!/usr/bin/python3

# Use this script to generate lists.py from obj file

import sys

verts = None
vertsl = None
grps = {}
vcount = 0

with open(sys.argv[1],"r") as f:
    for line in f:
        vals = line.split(" ")
        if vals[0] == "v":
            vcount += 1
        elif vals[0] == "g":
            verts = set()
            vertsl = []
            grps[vals[1].strip()] = vertsl
        if verts is None:
            continue
        if vals[0] != "f":
            continue
        vals = vals[1:]
        for val in vals:
            v = int(val[:val.index("/")])-1
            if v not in verts:
                verts.add(v)
                vertsl.append(v)

print("vertex_count = %d" % vcount)
for k,v in grps.items():
    print(k + " = " + repr(sorted(v)))

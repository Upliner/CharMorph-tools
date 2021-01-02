#!/usr/bin/python3

import os, sys

bones = {}
root = None

current = None

def parseVector(s):
   items = s.split(" ")
   return (float(items[0]),float(items[1]),float(items[2]))

with open(sys.argv[1],"r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("actor "):
            name = line[6:-2]
            current = [name,None,None,[]]
            bones[name]=current
        elif line.startswith("parent "):
            name = line[7:]
            if name == "UNIVERSE":
                root = current
            else:
                name = name[:-2]
                bones[name][3].append(current)
        elif line.startswith("origin "):
            current[1] = parseVector(line[7:])
        elif line.startswith("endPoint "):
            current[2] = parseVector(line[9:])

print("HIERARCHY\nROOT %s\n{" % root[0]);
def printBone(bone, endpoint, level):
   print("    " * level + "OFFSET {} {} {}".format(bone[1][0]-endpoint[0],bone[1][1]-endpoint[1],bone[1][2]-endpoint[2]))
   print("    " * level + "CHANNELS 3 Zrotation Xrotation Yrotation")
   for child in bone[3]:
       print("    " * level + "JOINT %s" % child[0])
       print("    " * level + "{")
       printBone(child, bone[1], level+1)
   if len(bone[3]) == 0:
       print("    " * level + "End Site")
       print("    " * level + "{")
       print("    " * (level+1) + "OFFSET {} {} {}".format(bone[2][0]-bone[1][0],bone[2][1]-bone[1][1],bone[2][2]-bone[1][2]))
       print("    " * level + "}")
   print("    " * (level-1) + "}")

printBone(root,(0,0,0),1)
print("MOTION\nFrames: 1\nFrame Time: 0.04")
print("0 0 0 " * len(bones))

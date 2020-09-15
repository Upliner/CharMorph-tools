#Import MB-Lab json files as shape keys
import bpy
import json

obj = bpy.context.object

baseDir = ""

ftypes = ["af01","an03","as01","ca01","ft01","la01"]

#obj.shape_key_add(name="basis", from_mix=False)
def loadL1():
    for fn in ftypes:
        with open(baseDir + "data/vertices/f_{}_verts.json".format(fn),"r") as f:
            data = json.load(f)
        if len(data) != len(obj.data.vertices):
            print("{} is not compatble!".format(fn))
            continue
        sk = obj.shape_key_add(name="L1_{}".format(fn), from_mix=False)
        for idx, val in enumerate(data):
            sk.data[idx].co = val

def clear_shape_keys():
    try:
        for sk in obj.data.shape_keys.key_blocks:
            if sk != obj.data.shape_keys.reference_key:
                obj.shape_key_remove(sk)
        obj.shape_key_remove(obj.data.shape_keys.reference_key)
    except:
        pass
    obj.shape_key_add(name="basis", from_mix=False)

def clear_vg():
    for vg in obj.vertex_groups:
        obj.vertex_groups.remove(vg)

def get_shape_key(name):
    try:
        return obj.data.shape_keys.key_blocks[name]
    except:
        return None

def loadL2():
    for fn in ["f_af01_morphs","f_an03_morphs","f_an03_morphs_extra","f_as01_morphs","f_ca01_morphs","f_ft01_morphs","f_ft01_morphs_extra","f_la01_morphs","human_female_morphs","human_female_morphs_extra"]:
        si = fn.find("_")+1
        parentName = fn[si:fn.find("_",si)]
        #print(baseName,get_shape_key(baseName))
        parentKey = get_shape_key("L1_" +parentName)
        if parentKey == None:
            parentName = ""
            parentKey = obj.data.shape_keys.key_blocks["basis"]
        with open(baseDir + "data/morphs/{}.json".format(fn),"r") as f:
            data = json.load(f)
        for key, morph in sorted(data.items()):
            name = "L2_{}_{}".format(parentName,key)
            if parentName != "": parentKey.value=1
            sk = obj.shape_key_add(name=name, from_mix=True)
            if parentName != "": parentKey.value=0
            sk.relative_key=parentKey
            #for idx, val in enumerate(parentKey.data):
            #    sk.data[idx].co = val.co
            for v in morph:
                pv = parentKey.data[v[0]].co
                sk.data[v[0]].co = [pv[0]+v[1],pv[1]+v[2],pv[2]+v[3]]

def loadJoints():
    with open(baseDir + "data/joints/human_female_joints.json","r") as f:
        data = json.load(f)
    for k, v in data.items():
        if k.startswith("IK_") or k.startswith("struct") or  "_muscle" in k or "_helper" in k:
            continue
        vg = obj.vertex_groups.new(name="joint_"+k)
        vg.add(v,1,'REPLACE')

def loadVg():
    with open(baseDir + "data/vgroups/human_female_vgroups_base.json","r") as f:
        data = json.load(f)
    for k, v in data.items():
        vg = obj.vertex_groups.new(name=k)
        for vert in v:
            vg.add([vert[0]],vert[1],'REPLACE')

def loadPf():
    with open(baseDir + "data/pgroups/human_female_polygs.json","r") as f:
        data = json.load(f)
    vg = obj.vertex_groups.new(name="proxyfit")
    for f in data:
        vg.add(obj.data.polygons[f].vertices,1,'REPLACE')

def loadHair():
    for fn in ftypes:
        with open(baseDir + "data/Particle_Hair/f_{}_hair.json".format(fn),"r") as f:
            data = json.load(f)
        vg = obj.vertex_groups.new(name="hair_"+fn)
        for f in data:
            vg.add(obj.data.polygons[f].vertices,1,'REPLACE')

clear_vg()
clear_shape_keys()
loadL1()
loadL2()
loadJoints()
loadVg()
loadPf()
loadHair()

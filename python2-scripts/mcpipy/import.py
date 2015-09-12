#
# Import .schematic file
# Copyright (c) 2015 Alexander Pruss
#
# Under MIT License
#

from mc import *
from sys import argv
import _nbt as nbt
import json

def getValue(v):
    if isinstance(v,nbt.TAG_Compound):
       return getCompound(v)
    elif isinstance(v,nbt.TAG_List):
       out = []
       for a in v:
           out.append(getValue(a))
       return out
    else:
       return v.value

def getCompound(nbt):
    out = {}
    for key in nbt:
        out[key] = getValue(nbt[key])
    return out

def nbtToJson(nbt):
    return json.dumps(getCompound(nbt))

def importSchematic(mc,path,x0,y0,z0,centerX=False,centerY=False,centerZ=False,clear=False):
    schematic = nbt.NBTFile(path, "rb")
    sizeX = schematic["Width"].value
    sizeY = schematic["Height"].value
    sizeZ = schematic["Length"].value

    def offset(x,y,z):
        return x + (y*sizeZ + z)*sizeX

    if centerX:
        x0 -= sizeX // 2
    if centerY:
        y0 -= sizeY // 2
    if centerZ:
        z0 -= sizeZ // 2

    corner1 = (x0,y0,z0)
    corner2 = (x0+sizeX-1,y0+sizeY-1,z0+sizeZ-1)

    if clear:
        mc.setBlocks(corner1,corner2,AIR)

    blocks = schematic["Blocks"].value
    data = schematic["Data"].value
    tileEntities = schematic["TileEntities"]
    tileEntityDict = {}
    for e in tileEntities:
        origCoords = e['x'],e['y'],e['z']
        e['x'].value += x0
        e['y'].value += y0
        e['z'].value += z0
        tileEntityDict[origCoords] = e
    for y in range(sizeY):
        for x in range(sizeX):
            for z in range(sizeZ):
                i = offset(x,y,z)
                b = blocks[i]
                if b == AIR.id:
                    continue
                d = data[i]
                if (x,y,z) in tileEntityDict:
                    mc.setBlockWithNBT(x0+x,y0+y,z0+z,b,d,nbtToJson(tileEntityDict[(x,y,z0)]))
                else:
                    mc.setBlock(x0+x,y0+y,z0+z,b,d)
    # TODO: entities
    return corner1,corner2

if __name__=='__main__':
    if len(argv) >= 2:
        path = argv[1]
    else:
        import Tkinter
        from tkFileDialog import askopenfilename
        master = Tkinter.Tk()
        master.attributes("-topmost", True)
        path = askopenfilename(filetypes=['vehicle {*.schematic}'],title="Open")
        master.destroy()

    mc = Minecraft()
    pos = mc.player.getTilePos()
    (corner0,corner1)=importSchematic(mc,path,pos.x,pos.y,pos.z,centerX=True,centerZ=True)
    mc.postToChat("Done drawing, putting player on top")
    y = corner1[1]
    while y > -256 and mc.getBlock(pos.x,y-1,pos.z) == AIR.id:
        y -= 1
    mc.player.setTilePos(pos.x,y,pos.z)

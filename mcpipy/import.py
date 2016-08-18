from __future__ import print_function
#
# Import .schematic file
#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
from sys import argv,version
import mcpi.nbt as nbt
import json

NEED_SUPPORT = set((block.SAPLING.id,block.WATER_FLOWING.id,block.LAVA_FLOWING.id,block.GRASS_TALL.id,34,block.FLOWER_YELLOW.id,
                    block.FLOWER_CYAN.id,block.MUSHROOM_BROWN.id,block.MUSHROOM_RED.id,block.TORCH.id,63,block.DOOR_WOOD.id,block.LADDER.id,
                    66,68,69,70,block.DOOR_IRON.id,72,75,76,77,block.SUGAR_CANE.id,93,94,96,104,105,106,108,111,
                    113,115,116,117,122,127,131,132,141,142,143,145,147,148,149,150,151,154,157,
                    167,block.SUNFLOWER.id,176,177,178,183,184,185,186,187,188,189,190,191,192,
                    193,194,195,196,197))

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

def importSchematic(mc,path,x0,y0,z0,centerX=False,centerY=False,centerZ=False,clear=False,movePlayer=True):
    mc.postToChat("Reading "+path);
    schematic = nbt.NBTFile(path, "rb")
    sizeX = schematic["Width"].value
    sizeY = schematic["Height"].value
    sizeZ = schematic["Length"].value

    def offset(x,y,z):
        return x + (y*sizeZ + z)*sizeX

    px,pz = x0,z0

    if centerX:
        x0 -= sizeX // 2
    if centerY:
        y0 -= sizeY // 2
    if centerZ:
        z0 -= sizeZ // 2

    corner1 = (x0,y0,z0)
    corner2 = (x0+sizeX-1,y0+sizeY-1,z0+sizeZ-1)

    if clear:
        mc.setBlocks(corner1,corner2,block.AIR)

    blocks = schematic["Blocks"].value
    data = schematic["Data"].value
    tileEntities = schematic["TileEntities"]
    tileEntityDict = {}
    if not isPE:
        for e in tileEntities:
            origCoords = e['x'].value,e['y'].value,e['z'].value
            e['x'].value += x0
            e['y'].value += y0
            e['z'].value += z0
            tileEntityDict[origCoords] = nbtToJson(e)
    check1 = lambda b : b != block.CARPET.id and b not in NEED_SUPPORT
    check2 = lambda b : b in NEED_SUPPORT
    check3 = lambda b : b == block.CARPET.id
    mc.postToChat("Rendering");
    for check in (check1,check2,check3):
        for y in range(sizeY):
            if check == check1 and movePlayer:
                mc.player.setTilePos(px,y0+y,pz)
            for x in range(sizeX):
                for z in range(sizeZ):
                    i = offset(x,y,z)
                    b = blocks[i]
                    if b == block.AIR.id:
                        continue
                    d = data[i]
                    if not check(b):
                        if check == check1:
                            b = block.AIR.id
                            d = 0
                        else:
                            continue
                    if b==33 and (d&7)==7:
                        d = (d&8)
                    if (x,y,z) in tileEntityDict:
#                        if b==33: \print x0+x,y0+y,z0+z,x,y,z,b,d,e
                        mc.setBlockWithNBT(x0+x,y0+y,z0+z,b,d,tileEntityDict[(x,y,z)])
                    else:
#                        if b==33: print x0+x,y0+y,z0+z,x,y,z,b,d
                        mc.setBlock(x0+x,y0+y,z0+z,b,d)

    print("done")
    # TODO: entities
    return corner1,corner2

if __name__=='__main__':
    if len(argv) >= 2:
        path = argv[1]
    else:
        if int(version[0]) < 3:
            from tkFileDialog import askopenfilename
            from Tkinter import Tk
        else:
            from tkinter.filedialog import askopenfilename
            from tkinter import Tk
        master = Tk()
        master.attributes("-topmost", True)
        path = askopenfilename(filetypes=['schematic {*.schematic}'],title="Open")
        master.destroy()
        if not path:
            exit()

    mc = Minecraft()
    pos = mc.player.getTilePos()
    (corner0,corner1)=importSchematic(mc,path,pos.x,pos.y,pos.z,centerX=True,centerZ=True)
    mc.postToChat("Done drawing, putting player on top")
    y = corner1[1]
    while y > -256 and mc.getBlock(pos.x,y-1,pos.z) == block.AIR.id:
        y -= 1
    mc.player.setTilePos(pos.x,y,pos.z)
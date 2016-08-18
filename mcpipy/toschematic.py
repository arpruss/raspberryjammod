from mine import *
from ast import literal_eval
import os
import sys
import re
import mcpi.nbt as nbt
from struct import pack
from vehicle import getLoadPath

def load(filename):
    with open(filename) as f:
        data = ''.join(f.readlines())
        result = re.search("=\\s*(.*)",data)
        if result is None:
            raise ValueError
        
        # Check to ensure only function called is Block() by getting literal_eval to
        # raise an exception when "Block" is removed and the result isn't a literal.
        # This SHOULD make the eval call safe, though USE AT YOUR OWN RISK. Ideally,
        # one would walk the ast parse tree and use a whitelist.
        literal_eval(result.group(1).replace("Block",""))

        return eval(result.group(1))

def toSchematic(vehicle):
    x0 = min(x for (x,y,z) in vehicle)
    y0 = min(y for (x,y,z) in vehicle)
    z0 = min(z for (x,y,z) in vehicle)
    x1 = max(x for (x,y,z) in vehicle)
    y1 = max(y for (x,y,z) in vehicle)
    z1 = max(z for (x,y,z) in vehicle)
    schematic = nbt.NBTFile()
    schematic.name = "Schematic"
    schematic.tags.append(nbt.TAG_Short(name="Width", value = x1-x0+1))
    schematic.tags.append(nbt.TAG_Short(name="Height", value = y1-y0+1))
    schematic.tags.append(nbt.TAG_Short(name="Length", value = z1-z0+1))
    schematic.tags.append(nbt.TAG_String(name="Materials", value="Alpha"))
    ids = b''
    metas = b''

    for y in range(y0,y1+1):
        for z in range(z0,z1+1):
            for x in range(x0,x1+1):
                try:
                    b = vehicle[(x,y,z)]
                except:
                    b = Block(0)
                ids += pack("B", b.id)
                metas += pack("B", b.data)

    blocks = nbt.TAG_Byte_Array(name="Blocks")
    blocks.value = ids
    schematic.tags.append(blocks)
    data = nbt.TAG_Byte_Array(name="Data")
    data.value = metas
    schematic.tags.append(data)
    schematic.tags.append(nbt.TAG_List(name="Entities", type=nbt.TAG_Compound))
    schematic.tags.append(nbt.TAG_List(name="TileEntities", type=nbt.TAG_Compound))

    return schematic

def vehicleToSchematic(vehiclePath, schematicPath):
    angle,highWater,vehicle = load(vehiclePath)
    nbt = toSchematic(vehicle)
    nbt.write_file(schematicPath)

if __name__ == '__main__':
    directory = os.path.join(os.path.dirname(sys.argv[0]),"vehicles")
    if len(sys.argv) >= 2:
        if sys.argv[1].endswith(".py"):
            name = directory + "/" + sys.argv[1]
        else:
            name = directory + "/" + sys.argv[1] + ".py"
    else:
        name = getLoadPath(directory, "py")

    out = name

    if out.endswith(".py"):
        out = name[:-2] + "schematic"
    else:
        out += ".schematic"

    vehicleToSchematic(name, out)

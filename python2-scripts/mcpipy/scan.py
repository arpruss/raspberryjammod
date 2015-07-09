import vehicle
import sys
from mc import *
import os

def save(vehicle,name):
    dir = os.path.join(os.path.dirname(sys.argv[0]),"vehicles")
    try:
        os.mkdir(dir)
    except:
        pass
    vehicle.save(os.path.join(dir,name+".py"))
    mc.postToChat('Saved as "'+name+'".')

mc = Minecraft()
basePos = mc.player.getTilePos()
rot = mc.player.getRotation()
vehicle = vehicle.Vehicle(mc)

if len(sys.argv) != 8:
    mc.postToChat("scan x1 y1 z1 x2 y2 z2 vehiclename")
    exit()
corner1 = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
corner2 = int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])

mc.postToChat("Scanning region")
dict = {}
for x in range(corner1[0],corner2[0]+1):
    for y in range(corner1[1],corner2[1]+1):
        for z in range(corner1[2],corner2[2]+1):
            block = vehicle.getBlockWithData(basePos.x+x,basePos.y+y,basePos.z+z)
            if block.id != AIR.id:
                dict[(x,y,z)] = block
mc.postToChat("Found "+str(len(dict))+" blocks")
vehicle.setVehicle(dict, rot)
save(vehicle,sys.argv[7])

from vehicle import Vehicle,getSavePath,getLoadPath
import sys
from mine import *
from time import sleep
import os

#
# Either:len
#   scan name x0 y0 z0 x1 y1 z1 : scan from (x0,y0,z0) relative to player to (x1,y1,z1) relative to player
#   scan name y0 : scan from y0 to sky in sword-right-click specified rectangle
#   scan name : scan from player feet to sky in sword-right-click specified rectangle
#   scan name r : restore scan
# Put a - for the name to be asked.
#

def getArea(basePos,depth):
    mc.postToChat("Sword-right-click other corner of rectangle")
    mc.events.clearAll()
    while True:
        hits = mc.events.pollBlockHits()
        if len(hits) > 0:
            c1 = (min(basePos.x,hits[0].pos.x),min(basePos.y-depth,hits[0].pos.y),min(basePos.z,hits[0].pos.z))
            c2 = (max(basePos.x,hits[0].pos.x),None,max(basePos.z,hits[0].pos.z))
            break
        sleep(0.25)
    maxY = c1[1]
    for x in range(c1[0],c2[0]+1):
        for z in range(c1[2],c2[2]+1):
            y = mc.getHeight(x,z)
            if y > maxY:
                maxY = y
    return (c1[0]-basePos.x,c1[1]-basePos.y,c1[2]-basePos.z),(c2[0]-basePos.x,maxY-basePos.y,c2[2]-basePos.z)


def save(vehicle,name):
    directory = os.path.join(os.path.dirname(sys.argv[0]),"vehicles")
    try:
        os.mkdir(directory)
    except:
        pass
    if name and name != '-':
        path = os.path.join(directory,name+".py")
    else:
        path = getSavePath('vehicles', 'py')
        if not path:
            mc.postToChat('Canceled')
            return
    vehicle.save(path)
    mc.postToChat('Saved in '+path)

def restore(vehicle,name,pos):
    directory = os.path.join(os.path.dirname(sys.argv[0]),"vehicles")
    if name and name != '-':
        path = os.path.join(directory,name+".py")
    else:
        path = getLoadPath('vehicles', 'py')
        if not path:
            mc.postToChat('Canceled')
            return
    vehicle.load(path)
    mc.postToChat('Loaded from '+path)
    minX = min(x for (x,y,z) in vehicle.baseVehicle)
    minY = min(y for (x,y,z) in vehicle.baseVehicle)
    minZ = min(z for (x,y,z) in vehicle.baseVehicle)
    maxX = max(x for (x,y,z) in vehicle.baseVehicle)
    maxY = max(y for (x,y,z) in vehicle.baseVehicle)
    maxZ = max(z for (x,y,z) in vehicle.baseVehicle)
    mc.postToChat('Erasing')
    mc.setBlocks(pos.x+minX,pos.y+minY,pos.z+minZ,pos.x+maxX,pos.y+maxY,pos.z+maxZ,block.AIR)
    mc.postToChat('Drawing')
    vehicle.draw(pos.x,pos.y,pos.z,vehicle.baseAngle)
    mc.postToChat('Done')

mc = Minecraft()
basePos = mc.player.getTilePos()
rot = mc.player.getRotation()
vehicle = Vehicle(mc)
#restore(vehicle, "cottage", basePos)
#exit()

if len(sys.argv) == 8:
    corner1 = int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
    corner2 = int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7])
elif len(sys.argv) == 2:
    corner1,corner2 = getArea(basePos,0)
elif len(sys.argv) == 3:
    if sys.argv[2].startswith('r'):
        restore(vehicle,sys.argv[1],basePos)
        exit()
    corner1,corner2 = getArea(basePos,int(sys.argv[2]))
else:
    mc.postToChat("scan vehiclename x1 y1 z1 x2 y2 z2")
    mc.postToChat("scan vehiclename depth [then right-click with sword on other corner]")
    mc.postToChat("scan vehiclename restore")
    mc.postToChat("scan vehiclename [then right-click with sword on other corner]")
    mc.postToChat("All coordinates are relative to player")
    exit()

mc.postToChat("Scanning region "+str(corner1)+"-"+str(corner2))
dict = {}
for x in range(corner1[0],corner2[0]+1):
    for y in range(corner1[1],corner2[1]+1):
        for z in range(corner1[2],corner2[2]+1):
            b = vehicle.getBlockWithData(basePos.x+x,basePos.y+y,basePos.z+z)
            if b.id != block.AIR.id:
                dict[(x,y,z)] = b
mc.postToChat("Scanned "+str(len(dict))+" blocks")
vehicle.setVehicle(dict, rot)
save(vehicle,sys.argv[1])

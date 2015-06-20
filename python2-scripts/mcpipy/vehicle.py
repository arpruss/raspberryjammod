#
# Code under the MIT license by Alexander Pruss
#

#
# Make a moving vehicle out of whatever the player is standing on, within a set distance
#

from mc import *
import time
import sys

try:
    MAX_DISTANCE_FROM_PLAYER = int(sys.argv[0])
except:
    MAX_DISTANCE_FROM_PLAYER = 25

# the following blocks do not count as part of the vehicle
SKIP = set((AIR.id,WATER_FLOWING.id,WATER_STATIONARY.id,GRASS.id,DIRT.id,LAVA_FLOWING.id,LAVA_STATIONARY.id))

def scan(dict,startPos,curPos=None):
    if curPos is not None:
        block = mc.getBlockWithData(curPos[0]+startPos[0],curPos[1]+startPos[1],curPos[2]+startPos[2])

        if block.id in SKIP:
            if block == WATER_STATIONARY and (highWater is None or highWater < curPos[1]+startPos[1]):
                highWater = curPos[1]+startPos[1]
            return
        else:
            dict[curPos] = block
    else:
        curPos = (0,0,0)

    for x in range(-1,2):
        for y in range(-1,2):
            for z in range(-1,2):
                pos = (x+curPos[0],y+curPos[1],z+curPos[2])
                if ( pos not in dict and abs(pos[0]) <= MAX_DISTANCE_FROM_PLAYER and
                     abs(pos[1]) <= MAX_DISTANCE_FROM_PLAYER and
                     abs(pos[2]) <= MAX_DISTANCE_FROM_PLAYER ):
                    scan(dict,startPos,pos)

def rotate(dict, amount):
    if amount == 0:
        return dict
    out = {}
    if amount == 1:
        for pos in dict:
            out[(-pos[2],pos[1],pos[0])] = dict[pos]
    elif amount == 2:
        for pos in dict:
            out[(-pos[1],pos[1],-pos[2])] = dict[pos]
    else:
        for pos in dict:
            out[(pos[2],pos[1],-pos[0])] = dict[pos]
    return out

def translate(base,x,y,z):
    out = {}
    for pos in base:
        out[(x+pos[0],y+pos[1],z+pos[2])] = base[pos]
    return out

mc = Minecraft()

vehiclePos = mc.player.getTilePos()
vehicleRotation = int(round(mc.player.getRotation() / 90.)) % 4

highWater = None
baseVehicle = {}
mc.postToChat("Scanning")
scan(baseVehicle,(vehiclePos.x,vehiclePos.y,vehiclePos.z))
mc.postToChat("Number of blocks: "+str(len(baseVehicle)))
if len(baseVehicle) == 0:
    mc.postToChat("Make a vehicle and then stand on it when starting this script.")
    exit()
else:
    mc.postToChat("Now walk around.")

oldVehicle = translate(baseVehicle,vehiclePos.x,vehiclePos.y,vehiclePos.z)
oldPos = vehiclePos
oldRotation = vehicleRotation

while True:
    vehiclePos = mc.player.getTilePos()
    vehicleRotation = int(round(mc.player.getRotation() / 90.)) % 4
    if vehicleRotation != oldRotation:
        baseVehicle = rotate(baseVehicle,(vehicleRotation-oldRotation)%4)
    if vehiclePos != oldPos or vehicleRotation != oldRotation:
        newVehicle = translate(baseVehicle,vehiclePos.x,vehiclePos.y,vehiclePos.z)
        todo = {}
        for pos in oldVehicle:
            if pos not in newVehicle:
                todo[pos] = WATER_FLOWING.id if pos[1] < highWater else AIR.id
        for pos in newVehicle:
            block = newVehicle[pos]
            if pos not in oldVehicle or oldVehicle[pos] != block:
                todo[pos] = block
        for pos in todo:
            mc.setBlock(pos,todo[pos])
        oldVehicle = newVehicle
        oldPos = vehiclePos
        oldRotation = vehicleRotation
    time.sleep(0.25)

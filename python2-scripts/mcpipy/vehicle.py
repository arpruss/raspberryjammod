#
# Code under the MIT license by Alexander Pruss
#

#
# Make a moving vehicle out of whatever the player is standing on, within a set distance
#
# Add a 'b' argument if you have and want an airtight bubble in the vehicle for going underwater
# Add an 'n' argument if you want (somewhat) non-destructive mode
#

from mc import *
import time
import sys

MAX_DISTANCE_FROM_PLAYER = 25

bubble = False
nondestructive = False

for opt in sys.argv[1:]:
    if opt[0] == 'b':
        bubble = True
    elif opt[0] == 'n':
        nondestructive = True

# the following blocks do not count as part of the vehicle
SKIP = set((AIR.id,WATER_FLOWING.id,WATER_STATIONARY.id,GRASS.id,DIRT.id,LAVA_FLOWING.id,LAVA_STATIONARY.id))

def scan(x0,y0,z0):
    global highWater

    positions = {}
    positions[(x0,y0,z0)] = mc.getBlockWithData(x0,y0,z0)

    foundAny = True

    while foundAny:
        foundAny = False
        for q in list(positions.keys()):
            for x in range(-1,2):
                for y in range(-1,2):
                    for z in range(-1,2):
                        pos = (x+q[0],y+q[1],z+q[2])
                        if pos not in positions:
                            if ( abs(pos[0]-x0) <= MAX_DISTANCE_FROM_PLAYER and
                                abs(pos[1]-y0) <= MAX_DISTANCE_FROM_PLAYER and
                                abs(pos[2]-z0) <= MAX_DISTANCE_FROM_PLAYER ):
                                block = mc.getBlockWithData(pos)
                                if block.id in SKIP:
                                    if (block.id == WATER_STATIONARY.id or block.id == WATER_FLOWING.id) and (highWater is None or highWater < pos[1]):
                                        highWater = pos[1]
                                else:
                                    positions[pos] = block
                                    foundAny = True

    if positions[(x0,y0,z0)].id in SKIP:
        del positions[(x0,y0,z0)]

    offsets = {}

    for pos in positions:
        offsets[(pos[0]-x0,pos[1]-y0,pos[2]-z0)] = positions[pos]

    return offsets

def getBubble(vehicle):
    positions = set()
    positions.add((0,0,0))

    tooBig = False
    foundAny = True
    while foundAny:
        foundAny = False
        for q in list(positions):
            for x,y,z in [(-1,0,0),(1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                pos = (x+q[0],y+q[1],z+q[2])
                if (abs(pos[0]) >= MAX_DISTANCE_FROM_PLAYER or 
                    abs(pos[1]) >= MAX_DISTANCE_FROM_PLAYER or
                    abs(pos[2]) >= MAX_DISTANCE_FROM_PLAYER):
                    mc.postToChat("Vehicle is not airtight!")
                    positions = set()
                    for x1 in range(-1,2):
                        for y1 in range(-1,2):
                            for z1 in range(-1,2):
                                if (x1,y1,z1) not in vehicle:
                                    positions.add((x1,y1,z1))
                    if (0,2,0) not in vehicle:
                        positions.add((0,2,0))
                    return positions
                if pos not in positions and pos not in vehicle:
                    positions.add(pos)
                    foundAny = True
    if (0,0,0) in vehicle:
        del positions[(0,0,0)]
    return positions

def rotate(dict, amount):
    if amount == 0:
        return dict
    out = {}
    if amount == 1:
        for pos in dict:
            out[(-pos[2],pos[1],pos[0])] = dict[pos]
    elif amount == 2:
        for pos in dict:
            out[(-pos[0],pos[1],-pos[2])] = dict[pos]
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
mc.postToChat("Scanning vehicle")
baseVehicle = scan(vehiclePos.x,vehiclePos.y,vehiclePos.z)
mc.postToChat("Number of blocks: "+str(len(baseVehicle)))
if bubble:
    mc.postToChat("Scanning for air bubble")
    for pos in getBubble(baseVehicle):
        baseVehicle[pos] = AIR

if len(baseVehicle) == 0 and not bubble:
    mc.postToChat("Make a vehicle and then stand on or in it when starting this script.")
    exit()
else:
    mc.postToChat("Now walk around.")

oldVehicle = translate(baseVehicle,vehiclePos.x,vehiclePos.y,vehiclePos.z)
oldPos = vehiclePos
oldRotation = vehicleRotation
saved = {}

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
                if nondestructive and pos in saved:
                    todo[pos] = saved[pos]
                    del saved[pos]
                else:
                    todo[pos] = WATER_FLOWING.id if highWater is not None and pos[1] <= highWater else AIR.id
        for pos in newVehicle:
            block = newVehicle[pos]
            if pos not in oldVehicle or oldVehicle[pos] != block:
                todo[pos] = block
                if nondestructive and pos not in oldVehicle:
                    saved[pos] = mc.getBlockWithData(pos)
        for pos in todo:
            mc.setBlock(pos,todo[pos])
        oldVehicle = newVehicle
        oldPos = vehiclePos
        oldRotation = vehicleRotation
    time.sleep(0.25)

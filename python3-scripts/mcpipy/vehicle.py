#
# Code under the MIT license by Alexander Pruss
#

"""
 Make a moving vehicle out of whatever blocks the player is standing near.

 Add a 'b' argument if you have and want an airtight bubble in the vehicle for going underwater
 Add an 'n' argument if you want (somewhat) non-destructive mode
 Add an 'q' argument if you don't want the vehicle to flash red as it is scanned

 The vehicle detection algorithm works as follows:
   first, search for nearest non-terrain block within distance SCAN_DISTANCE of the player
   second, get the largest connected set of non-terrain blocks, including diagonal connections, up to
     distance MAX_DISTANCE in each coordinate
   in bubble mode, add the largest set of air blocks, excluding diagonal connections, or a small bubble about the
     player if the the vehicle is not airtight
"""

from mcpi.minecraft import *
from mcpi.block import *
from math import *
import time
import sys

SCAN_DISTANCE = 5
MAX_DISTANCE = 30

bubble = False
nondestructive = False
flash = True

if len(sys.argv)>1:
    for x in ''.join(sys.argv[1:]):
        if x == 'b':
            bubble = True
        elif x == 'n':
            nondestructive = True
        elif x == 'q':
            flash = False

# the following blocks do not count as part of the vehicle
TERRAIN = set((AIR.id,WATER_FLOWING.id,WATER_STATIONARY.id,GRASS.id,DIRT.id,LAVA_FLOWING.id,
               LAVA_STATIONARY.id,GRASS.id,DOUBLE_TALLGRASS.id,GRASS_TALL.id,BEDROCK.id,GRAVEL.id))

NEED_SUPPORT = set((SAPLING.id,WATER_FLOWING.id,LAVA_FLOWING.id,GRASS_TALL.id,34,35,FLOWER_YELLOW.id,
                    FLOWER_CYAN.id,MUSHROOM_BROWN.id,MUSHROOM_RED.id,TORCH.id,63,DOOR_WOOD.id,LADDER.id,
                    66,68,69,70,DOOR_IRON.id,72,75,76,77,SUGAR_CANE.id,93,94,96,104,105,106,108,111,
                    113,115,116,117,122,127,131,132,141,142,143,145,147,148,149,150,151,154,157,
                    167,CARPET.id,SUNFLOWER.id,176,177,178,183,184,185,186,187,188,189,190,191,192,
                    193,194,195,196,197))

def keyFunction(dict,erase,pos):
    return (dict[pos].id in NEED_SUPPORT,pos not in erase or erase[pos].id not in NEED_SUPPORT,pos[1],pos[0],pos[2])

def box(x0,y0,z0,x1,y1,z1):
    for x in range(x0,x1+1):
        for y in range(y0,y1+1):
            for z in range(z0,z1+1):
                yield (x,y,z)

def getSeed(x0,y0,z0):
    scanned = set()
    for r in range(0,SCAN_DISTANCE+1):
        for x,y,z in box(-r,-r,-r,r,r,r):
            if x*x+y*y+z*z <= r*r and (x,y,z) not in scanned:
                blockId = mc.getBlock(x+x0,y+y0,z+z0)
                scanned.add((x,y,z))
                if blockId not in TERRAIN:
                    return (x0+x,y0+y,z0+z)
    return None

def safeSetBlockWithData(pos,block):
    """
    Draw block, making sure buttons are not depressed. This is to fix a glitch where launching 
    the vehicle script from a commandblock resulted in re-pressing of the button.
    """
    if block.id == WOOD_BUTTON.id or block.id == STONE_BUTTON.id:
        block = Block(block.id, block.data & ~0x08)
    setBlockWithData(pos,block)

def scan(x0,y0,z0):
    global highWater

    seed = getSeed(x0,y0,z0)
    if seed is None:
        return {}

    block = getBlockWithData(seed)
    positions = {seed:block}
    if flash and block.id not in NEED_SUPPORT:
        mc.setBlock(seed,GOLD_BLOCK)
    newlyAdded = set(positions.keys())

    while len(newlyAdded)>0:
        adding = set()
        mc.postToChat("Added "+str(len(newlyAdded))+" blocks")
        for q in newlyAdded:
            for x,y,z in box(-1,-1,-1,1,1,1):
                pos = (x+q[0],y+q[1],z+q[2])
                if pos not in positions:
                    if ( abs(pos[0]-x0) <= MAX_DISTANCE and
                        abs(pos[1]-y0) <= MAX_DISTANCE and
                        abs(pos[2]-z0) <= MAX_DISTANCE ):
                        block = getBlockWithData(pos)
                        if block.id in TERRAIN:
                            if (block.id == WATER_STATIONARY.id or block.id == WATER_FLOWING.id) and (highWater is None or highWater < pos[1]):
                                highWater = pos[1]
                        else:
                            positions[pos] = block
                            adding.add(pos)
                            if block.id not in NEED_SUPPORT:
                                mc.setBlock(pos,GOLD_BLOCK)
        newlyAdded = adding

    offsets = {}
    empty = {}
    for pos in sorted(positions, key=lambda x : keyFunction(positions,empty,x)):
        offsets[(pos[0]-x0,pos[1]-y0,pos[2]-z0)] = positions[pos]
        if flash:
            safeSetBlockWithData(pos,positions[pos])

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
                if (abs(pos[0]) >= MAX_DISTANCE or 
                    abs(pos[1]) >= MAX_DISTANCE or
                    abs(pos[2]) >= MAX_DISTANCE):
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

stairDirectionsClockwise = [2, 1, 3, 0]
stairToClockwise = [3, 1, 0, 2]
STAIRS = set((STAIRS_COBBLESTONE.id, STAIRS_WOOD.id, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180))

# TODO: rotate blocks other than stairs
def rotateBlock(block,amount):
    if block.id in STAIRS:
        meta = block.data
        return Block(block.id, (meta & ~0x03) | stairDirectionsClockwise[(stairToClockwise[meta & 0x03] + amount) % 4])
    elif block.id == STONE_BUTTON.id or block.id == WOOD_BUTTON.id:
        direction = block.data & 0x07
        if direction < 1 or direction > 4:
            return block
        direction = 1 + stairDirectionsClockwise[(stairToClockwise[direction-1] + amount) % 4]
        return Block(block.id, (block.data & ~0x07) | direction)
    else:
        return block


def rotate(dict, amount):
    if amount == 0:
        return dict
    out = {}
    if amount == 1:
        for pos in dict:
            out[(-pos[2],pos[1],pos[0])] = rotateBlock(dict[pos],amount)
    elif amount == 2:
        for pos in dict:
            out[(-pos[0],pos[1],-pos[2])] = rotateBlock(dict[pos],amount)
    else:
        for pos in dict:
            out[(pos[2],pos[1],-pos[0])] = rotateBlock(dict[pos],amount)
    return out

def translate(base,x,y,z):
    out = {}
    for pos in base:
        out[(x+pos[0],y+pos[1],z+pos[2])] = base[pos]
    return out

mc = Minecraft()

if hasattr(Minecraft, 'getBlockWithNBT'):
    getBlockWithData = mc.getBlockWithNBT
    setBlockWithData = mc.setBlockWithNBT
else:
    getBlockWithData = mc.getBlockWithData
    setBlockWithData = mc.setBlock

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
        erase = {}
        for pos in oldVehicle:
            if pos not in newVehicle:
                if nondestructive and pos in saved:
                    todo[pos] = saved[pos]
                    del saved[pos]
                else:
                    todo[pos] = WATER_STATIONARY if highWater is not None and pos[1] <= highWater else AIR
            else:
                erase[pos] = newVehicle[pos]
        for pos in newVehicle:
            block = newVehicle[pos]
            if pos not in oldVehicle or oldVehicle[pos] != block:
                todo[pos] = block
                if pos not in oldVehicle and nondestructive:
                    curBlock = getBlockWithData(pos)
                    if curBlock == block:
                        del todo[pos]
                    saved[pos] = curBlock
                    erase[pos] = curBlock

#        mc.setting("pause_drawing",1)
        for pos in sorted(todo, key=lambda x : keyFunction(todo,erase,x)):
            safeSetBlockWithData(pos,todo[pos])
#        mc.setting("pause_drawing",0)
        oldVehicle = newVehicle
        oldPos = vehiclePos
        oldRotation = vehicleRotation
    time.sleep(0.25)

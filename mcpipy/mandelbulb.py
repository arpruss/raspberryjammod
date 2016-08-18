#
# Code by Alexander Pruss and under the MIT license
#
#
# mandelbulb.py [size [power [half]]]
#
# Options for half: south, north, east, west, up, down

from mine import *
import mcpi.settings as settings
import cmath
import time
import sys
from random import uniform

# setting this to 0 makes for more isolated blocks because the connecting filigree was
# missed; increasing slows down rendering
AVOID_ISOLATES = 12 if not settings.isPE else 0

ESCAPE = 250
if len(sys.argv) < 2:
    size = 100
else:
    size = int(sys.argv[1])

if len(sys.argv) < 3:
    power = 8
else:
    power = int(sys.argv[2])

if power == 8:
    fractalSize = 2.16
else:
    fractalSize = 4.

if len(sys.argv) < 4:
    half = None
else:
    half = sys.argv[3].lower()[0]

palette = list(reversed([block.WOOL_WHITE,block.HARDENED_CLAY_STAINED_WHITE,block.WOOL_PINK,block.WOOL_LIGHT_GRAY,block.WOOL_LIGHT_BLUE,block.WOOL_MAGENTA,block.WOOL_PURPLE,block.HARDENED_CLAY_STAINED_LIGHT_BLUE,block.HARDENED_CLAY_STAINED_LIGHT_GRAY,block.HARDENED_CLAY_STAINED_MAGENTA,block.HARDENED_CLAY_STAINED_PINK,block.HARDENED_CLAY_STAINED_RED,block.WOOL_RED,block.REDSTONE_BLOCK,block.HARDENED_CLAY_STAINED_ORANGE,block.WOOL_ORANGE,block.HARDENED_CLAY_STAINED_YELLOW,block.WOOL_YELLOW,block.WOOL_LIME,block.HARDENED_CLAY_STAINED_LIME,block.HARDENED_CLAY_STAINED_PURPLE,block.HARDENED_CLAY_STAINED_CYAN,block.WOOL_CYAN,block.WOOL_BLUE,block.HARDENED_CLAY_STAINED_BLUE,block.WOOL_GRAY,block.HARDENED_CLAY_STAINED_GREEN,block.WOOL_GREEN,block.HARDENED_CLAY_STAINED_BROWN,block.WOOL_BROWN,block.HARDENED_CLAY_STAINED_GRAY,block.WOOL_BLACK]));

def positions(pos,scale):
    yield pos
    for i in range(AVOID_ISOLATES):
        yield (uniform(pos[0]-0.5*scale,pos[0]+0.5*scale),
               uniform(pos[1]-0.5*scale,pos[1]+0.5*scale),
               uniform(pos[2]-0.5*scale,pos[2]+0.5*scale))

def calculate0(pos):
    x,z,y = pos[0],pos[1],pos[2]
    cx,cy,cz = x,y,z

    i = 0
    try:
        wentOut = 0
        while i<ESCAPE:
            r = sqrt(x*x+y*y+z*z)
            if r > 2:
               return -1
            if r > wentOut:
               wentOut = r
            theta = acos(z/r)
            phi = atan2(y,x)
            zr = r**power
            theta *= power
            phi *= power

            x = cx+zr*sin(theta)*cos(phi)
            y = cy+zr*sin(phi)*sin(theta)
            z = cz+zr*cos(theta)

            i = i + 1
        return wentOut
    except:
        return 0

def calculate(pos0,scale):
    for pos in positions(pos0,scale):
        r = calculate0(pos)
        if r >= 0:
            return r
    return r

#
# we could of course just do for x in range(0,size): for y in range(0,size): yield(x,y)
# but it will make users happier if we start at the player
#


def pollZoom():
    global lastHitEvent,lastHitPos
    events = mc.events.pollBlockHits()
    if len(events) == 0:
        return lastHitEvent != None
    lastHitEvent = events[-1]
    lastHitPos = mc.player.getPos()
    return True

def toBulb(centerMC,centerBulb,scale,x,y,z):
    return ((x - centerMC.x) * scale  + centerBulb[0],
                    (y - centerMC.y) * scale  + centerBulb[1],
                    (z - centerMC.z) * scale + centerBulb[2])

def draw():
    count = 0
    
    rangeX = range(cornerMC.x, cornerMC.x+size)
    rangeY = range(cornerMC.y, cornerMC.y+size)
    rangeZ = range(cornerMC.z, cornerMC.z+size)
    
    if not half is None:
        if half == 'w':
            rangeX = range(cornerMC.x, cornerMC.x+size/2)
        elif half == 'e':
            rangeX = range(cornerMC.x+size/2, cornerMC.x+size)
        elif half == 'n':
            rangeZ = range(cornerMC.z, cornerMC.z+size/2)
        elif half == 's':
            rangeZ = range(cornerMC.z+size/2, cornerMC.z+size)
        elif half == 'u':
            rangeY = range(cornerMC.y+size/2, cornerMC.y+size)
        elif half == 'd':
            rangeY = range(cornerMC.y, cornerMC.y+size/2)

    for mcX in rangeX:
        for mcY in rangeY:
            for mcZ in rangeZ:
                radius = calculate(toBulb(centerMC,centerBulb,scale,mcX,mcY,mcZ),scale)
                if radius < 0:
                    mc.setBlock(mcX,mcY,mcZ,block.AIR)
                else:
                    i = int(len(palette) / (fractalSize/2) * radius)
                    if i >= len(palette):
                        i = len(palette) - 1
                    mc.setBlock(mcX,mcY,mcZ,palette[i])
        if pollZoom():
            return
    mc.postToChat("Rendered")

if __name__=='__main__':
    mc = Minecraft()
    startPos = mc.player.getTilePos()
    cornerMC = startPos + Vec3(1,0,1)
    centerMC = cornerMC + Vec3(size/2,size/2,size/2)
    centerBulb = (0,0,0)
    initial = True
    scale    = fractalSize / size
    lastHitEvent = None

    while True:
        mc.player.setPos(startPos)
        mc.postToChat("Scale: "+str(fractalSize/size/scale))
        draw()
        if not initial:
            mc.player.setPos(centerMC)
        while not pollZoom():
            time.sleep(0.25)
        if ( lastHitEvent.pos.x < cornerMC.x or
             lastHitEvent.pos.x >= cornerMC.x + size or
             lastHitEvent.pos.y < cornerMC.y or
             lastHitEvent.pos.y >= cornerMC.y + size or
             lastHitEvent.pos.z < cornerMC.z or
             lastHitEvent.pos.z >= cornerMC.z + size ):
                mc.postToChat("resetting")
                centerBulb = (0,0,0)
                scale = fractalSize / size
                initial = True
        else:
                mc.postToChat("zooming")
                centerBulb = toBulb(centerMC,centerBulb,scale,lastHitPos.x,lastHitPos.y,lastHitPos.z)
                scale /= 8
                initial = False
        lastHitEvent = None

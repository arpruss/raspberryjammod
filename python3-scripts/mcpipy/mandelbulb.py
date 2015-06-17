#
# MIT-licensed code by Alexander Pruss
#
#
# mandelbulb.py [size [power [half]]]
#

from .mc import *
from . import mcpi.settings
import cmath
import time
import sys

ESCAPE = 250
if len(sys.argv) < 2:
    size = 100
else:
    size = int(sys.argv[1])

if len(sys.argv) < 3:
    power = 8
else:
    power = int(sys.argv[2])

if power != 8:
    fractalSize = 4.
else:
    fractalSize = 2.16

if len(sys.argv) < 4:
    half = False
else:
    half = sys.argv[3].lower()[0] == 'h'

palette = list(reversed([WOOL_WHITE,HARDENED_CLAY_STAINED_WHITE,WOOL_PINK,WOOL_LIGHT_GRAY,WOOL_LIGHT_BLUE,WOOL_MAGENTA,WOOL_PURPLE,HARDENED_CLAY_STAINED_LIGHT_BLUE,HARDENED_CLAY_STAINED_LIGHT_GRAY,HARDENED_CLAY_STAINED_MAGENTA,HARDENED_CLAY_STAINED_PINK,HARDENED_CLAY_STAINED_RED,WOOL_RED,REDSTONE_BLOCK,HARDENED_CLAY_STAINED_ORANGE,WOOL_ORANGE,HARDENED_CLAY_STAINED_YELLOW,WOOL_YELLOW,WOOL_LIME,HARDENED_CLAY_STAINED_LIME,HARDENED_CLAY_STAINED_PURPLE,HARDENED_CLAY_STAINED_CYAN,WOOL_CYAN,WOOL_BLUE,HARDENED_CLAY_STAINED_BLUE,WOOL_GRAY,HARDENED_CLAY_STAINED_GREEN,WOOL_GREEN,HARDENED_CLAY_STAINED_BROWN,WOOL_BROWN,HARDENED_CLAY_STAINED_GRAY,WOOL_BLACK]));

def calculate(pos):
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
    for mcX in range(cornerMC.x, cornerMC.x+size):
        for mcY in range(cornerMC.y, cornerMC.y+size):
            for mcZ in range(cornerMC.z, cornerMC.z+size/2 if half else cornerMC.z+size):
                radius = calculate(toBulb(centerMC,centerBulb,scale,mcX,mcY,mcZ))
                if radius < 0:
                    mc.setBlock(mcX,mcY,mcZ,AIR)
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

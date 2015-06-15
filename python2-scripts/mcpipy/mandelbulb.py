#
# MIT-licensed code by Alexander Pruss
#

from mc import *
import mcpi.settings
import cmath
import time
import sys

ESCAPE = 30
if len(sys.argv) < 2:
    SIZE = 100
else:
    SIZE = int(sys.argv[1])

block = REDSTONE_ORE

def escapes(x,y,z):
    i = 0
    cx = x
    cy = y
    cz = z
    try:
        while i<ESCAPE:
        # http://iquilezles.org/www/articles/mandelbulb/mandelbulb.htm
            """
            x2 = x*x
            x4 = x2*x2
            y2 = y*y
            y4 = y2*y2
            z2 = z*z
            z4 = z2*z2

            k3 = x2 + z2
            if k3+y2 > 1000: # 1.2:
                return True
            k2 = 1./sqrt(k3*k3*k3*k3*k3*k3*k3)
            k1 = x4 + y4 + z4 - 6*y2*z2 - 6*x2*y2 + 2*z2*x2
            k4 = x2 - y2 + z2
            x = cx+64*x*y*z*(x2-z2)*k4*(x4-6*x2*z2+z4)*k1*k2
            y = cy-16*y2*k3*k4*k4+k1*k1
            z = cz-8*y*k4*(x4*x4 - 28*x4*x2*z2 + 70*x4*z4 - 28*x2*z2*z4 + z4*z4)*k1*k2
            """
            r = sqrt(x*x+y*y+z*z)
            if r > 31:
               return True
            theta = acos(z/r)
            phi = atan2(y,x)
            zr = r**8
            theta *= 8
            phi *= 8

            x = cx+zr*sin(theta)*cos(phi)
            y = cy+zr*sin(phi)*sin(theta)
            z = cz+zr*cos(theta)

            i = i + 1
        return False
    except:
        return False

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

def toBulb(x,y,z):
    return ((x - centerMC.x) * scale  + centerBulb[0],
                    (y - centerMC.y) * scale  + centerBulb[1],
                    (z - centerMC.z) * scale + centerBulb[2])

def draw():
    count = 0
    for mcX in range(cornerMC.x, cornerMC.x+SIZE):
        for mcY in range(cornerMC.y, cornerMC.y+SIZE):
            for mcZ in range(cornerMC.z, cornerMC.z+SIZE):
                x,y,z = toBulb(mcX,mcY,mcZ)
                mc.setBlock(mcX,mcY,mcZ,AIR if escapes(x,y,z) else block)
        if pollZoom():
            return

mc = Minecraft()
startPos = mc.player.getTilePos()
cornerMC = startPos + Vec3(1,0,1)
centerMC = cornerMC + Vec3(SIZE/2,SIZE/2,SIZE/2)
centerBulb = (0,0,0)
initial = True
scale    = 2.4 / SIZE
lastHitEvent = None

while True:
    mc.player.setPos(startPos)
    mc.postToChat("Scale: "+str(2.4/SIZE/scale))
    draw()
    mc.postToChat("Rendered")
    if not initial:
        mc.player.setPos(centerMC)
    while not pollZoom():
        time.sleep(0.25)
    if ( lastHitEvent.pos.x < cornerMC.x or
         lastHitEvent.pos.x >= cornerMC.x + SIZE or
         lastHitEvent.pos.y < cornerMC.y or
         lastHitEvent.pos.y >= cornerMC.y + SIZE or
         lastHitEvent.pos.z < cornerMC.z or
         lastHitEvent.pos.z >= cornerMC.z + SIZE ):
            mc.postToChat("resetting")
            centerBulb = (0,0,0)
            scale = 2.2 / SIZE
            initial = True
    else:
            mc.postToChat("zooming")
            centerBulb = toBulb(lastHitPos.x, lastHitPos.y, lastHitPos.z)
            scale /= 8
            initial = False
    lastHitEvent = None

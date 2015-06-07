#
# MIT-licensed code by Alexander Pruss
#

from mc import *
import mcpi.settings
import cmath
import time

ESCAPE = 256
SIZE = 768 if not mcpi.settings.isPE else 400
black = WOOL_BLACK
palette = [ WOOL_WHITE, WOOL_ORANGE, WOOL_MAGENTA, WOOL_LIGHT_BLUE,
            WOOL_YELLOW, WOOL_LIME, WOOL_PINK, WOOL_GRAY, WOOL_LIGHT_GRAY,
            WOOL_CYAN, WOOL_PURPLE, WOOL_BLUE, WOOL_BROWN, WOOL_GREEN,
            WOOL_RED, 152 ]

def escapeTime(c):
    i = 0
    z = c
    while abs(z) < 2 and i < ESCAPE:
        i = i + 1
        z = z * z + c
    return i

#
# we could of course just do for x in range(0,size): for y in range(0,size): yield(x,y)
# but it will make users happier if we start at the player
#

def loopGenerator(size, cenX, cenY):
    yield (cenX, cenY)
    for r in range(1,size):
        # right line segment
        if cenX+r < size:
            y = cenY - r
            if y < 0:
                y = 0
            while y < cenY + r and y < size:
                yield (cenX+r, y)
                y += 1
        # top line segment
        if cenY+r < size:
            x = cenX + r
            if x >= size:
                x = size - 1
            while cenX - r < x and 0 <= x:
                yield (x, cenY+r)
                x -= 1
        # left line segment
        if 0 <= cenX-r:
            y = cenY + r
            if y >= size:
                y = size - 1
            while cenY - r < y and 0 <= y:
                yield (cenX-r, y)
                y -= 1
        # bottom line segment
        if 0 <= cenY-r:
            x = cenX - r
            if x < 0:
                x = 0
            while x < cenX + r and x < size:
                yield(x, cenY - r)
                x += 1
                
def pollZoom():
    global lastHitEvent
    events = mc.events.pollBlockHits()
    if len(events) == 0:
        return lastHitEvent != None
    lastHitEvent = events[-1]
    return True

def toComplex(x,y):
    return  complex((x - posMC.x) * scale  + posCx.real,
                    (y - posMC.z) * scale  + posCx.imag)

def draw():
    count = 0
    for (x,y) in loopGenerator(SIZE, posMC.x-centerMC.x+SIZE/2, posMC.z-centerMC.z+SIZE/2):
        mcX = x + centerMC.x - SIZE/2
        mcY = y + centerMC.z - SIZE/2
        c = toComplex(mcX, mcY)
        
        esc = escapeTime(c)
        mc.setBlock(mcX, centerMC.y, mcY,
                    palette[esc % len(palette)] if esc < ESCAPE else black)
        if count >= 1000:
            if pollZoom():
                break
            else:
                count = 0
        else:
            count += 1

mc = Minecraft()
centerMC = mc.player.getPos()
centerMC.ifloor()
posMC    = centerMC
posCx    = complex(0,0)
scale    = 4. / SIZE
lastHitEvent = None

while True:
    draw()
    while not pollZoom():
        time.sleep(0.25)
    if ( lastHitEvent.pos.y != centerMC.y or lastHitEvent.pos.x < centerMC.x - size / 2 or
         lastHitEvent.pos.x >= centerMC.x + size / 2 or
         lastHitEvent.pos.z < centerMC.z - size / 2 or
         lastHitEvent.pos.z >= centerMC.z + size / 2 ):
            scale /= 2
            posMC = centerMC
            posCx = complex(0,0)
            mc.postToChat("Recentering at origin")
    else:
            posCx = toComplex(lastHitEvent.pos.x,lastHitEvent.pos.z)
            mc.postToChat("Recentering at "+posCx)
            scale *= 2
            posMC = lastHitEvent.pos

mc.postToChat("Done")

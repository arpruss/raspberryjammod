#
# MIT-licensed code by Alexander Pruss
#

from mc import *
import settings
import cmath

ESCAPE = 256
SIZE = 768 if not isPE else 400
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

def draw(centerMC, posMC, posCx, size, scale):
    for x in range(size):
        for y in range(size):
            mcX = x + centerMC.x - size/2
            mcY = y + centerMC.z - size/2
            c = complex((mcX - posMC.x) * scale  + posCx.real,
                        (mcY - posMC.z) * scale  + posCx.imag)
            esc = escapeTime(c)
            mc.setBlock(mcX, centerMC.y, mcY,
                        palette[esc % len(palette)] if esc < ESCAPE else black)

mc = Minecraft()
centerMC = mc.player.getPos()
centerMC.ifloor()
print centerMC
posMC    = centerMC
posCx    = complex(0,0)
scale    = 4. / SIZE
draw(centerMC, posMC, posCx, SIZE, scale)

#for x in range(SIZE):
#    for y in range(SIZE):
#        value = complex(4. * x / SIZE - 2, 4. * y / SIZE - 2)
#        esc = escapeTime(value)
#        mc.setBlock(pos.x + x - SIZE/2, pos.y, pos.z + y - SIZE/2,
#                    palette[esc % len(palette)] if esc < ESCAPE else black)

mc.postToChat("Done")

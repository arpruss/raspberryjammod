#
# Code under the MIT license by Alexander Pruss
#
# mengersponge [levels [options]]
#   levels is a level count, up to 5
#   options is a string of characters containing possibly the options 's' for 'slice' (cut off a diagonal slice) and 'c' for 'color'
#
from mc import *
import mcpi.settings as settings
import sys

RAINBOW = (STAINED_GLASS_RED,STAINED_GLASS_ORANGE,STAINED_GLASS_YELLOW,STAINED_GLASS_GREEN,STAINED_GLASS_BLUE,STAINED_GLASS_PURPLE)

def deleteCubes(x0,y0,z0,length,colorIndex=None):
    nextColorIndex = colorIndex + 1 if colorIndex is not None else None
    length /= 3
    if length < 1:
        return
    for x in range(3):
        for y in range(3):
            for z in range(3):
                posX = x0+x*length
                posY = y0+y*length
                posZ = z0+z*length
                if (x == 1 and y == 1) or (x == 1 and z == 1) or (y == 1 and z == 1):
                    if colorIndex is not None:
                        mc.setBlocks(posX,posY,posZ,
                                     posX+length-1,posY+length-1,posZ+length-1,RAINBOW[colorIndex])
                    else:
                        mc.setBlocks(posX,posY,posZ,
                                 posX+length-1,posY+length-1,posZ+length-1,AIR)
                else:
                    deleteCubes(posX,posY,posZ,length,nextColorIndex)

def slice(x0,y0,z0,length):
    for x in range(0,length):
        for y in range(0,length):
            for z in range(0,length):
                if x+y+z >= 1.5*length:
                    mc.setBlock(x0+x,y0+y,z0+z,AIR)

mc = Minecraft()
playerPos = mc.player.getPos()
if settings.isPE:
    length = 3*3*3
else:
    length = 3*3*3*3
if len(sys.argv) > 1:
    length = 3**int(sys.argv[1])
colorIndex = None
if len(sys.argv) > 2:
    colorIndex = 0 if 'c' in sys.argv[2] else None
mc.setBlocks(playerPos.x,playerPos.y,playerPos.z,
             playerPos.x+length-1,playerPos.y+length-1,playerPos.z+length-1,WOOL_PURPLE)
deleteCubes(playerPos.x,playerPos.y,playerPos.z,length,colorIndex=colorIndex)
if len(sys.argv)>2 and 's' in sys.argv[2]:
    mc.postToChat("Slicing")
    slice(playerPos.x,playerPos.y,playerPos.z,length)

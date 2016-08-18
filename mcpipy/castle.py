#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
import random
import sys

def getHeightBelow(x,y,z):
    if isPE:
        return min(mc.getHeight(x,z),y)
    else:
        y0 = y - 255
        while y > y0:
           if mc.getBlock(x,y,z) != block.AIR.id:
               return y
           y -= 1
        return min(mc.getHeight(x,z),y)

def rectangularPrism(x1,y1,z1, x2,y2,z2, distribution):
    x1 = int(round(x1))
    y1 = int(round(y1))
    z1 = int(round(z1))
    x2 = int(round(x2))
    y2 = int(round(y2))
    z2 = int(round(z2))
    for x in range(min(x1,x2),max(x1,x2)+1):
        for y in range(min(y1,y2),max(y1,y2)+1):
            for z in range(min(z1,z2),max(z1,z2)+1):
                if isinstance(distribution, Block):
                    mc.setBlock(x,y,z,distribution)
                else:
                    r = random.random()
                    for p,b in distribution:
                        r -= p
                        if r<0:
                            mc.setBlock(x,y,z,b)
                            break

# Note: the first set of coordinates must be smaller than the second
def wall(x1,y1,z1, x2,y2,z2, baseHeight, altHeight, distribution):
    x = x1
    z = z1

    while True:
        if (x-x1+z-z1) % 2 == 0:
            height = altHeight
        else:
            height = baseHeight
        y0 = getHeightBelow(x,y1,z)
        rectangularPrism(x,y0,z,x,y1+height,z,distribution)
        if x >= x2 and z >= z2:
            return
        if x < x2:
            x = x + 1
        if z < z2:
            z = z + 1

# Note: the first set of coordinates must be smaller than the second
def moatSide(x1,y1,z1, x2,y2,z2, depth):
    x = x1
    z = z1

    while True:
        y0 = getHeightBelow(x,y1,z)
        mc.setBlocks(x,y0-depth+1,z,x,y0,z,block.WATER_STATIONARY)
        if x >= x2 and z >= z2:
            return
        if x < x2:
            x = x + 1
        if z < z2:
            z = z + 1

def crenellatedSquare(x1,y1,z1,width,height,altHeight,distribution):
    wall(x1, y1, z1, x1+width-1, y1, z1, height, altHeight,distribution)
    wall(x1, y1, z1, x1, y1, z1+width-1, height, altHeight,distribution)
    wall(x1+width-1, y1, z1, x1+width-1, y1, z1+width-1, height, altHeight,distribution)
    wall(x1, y1, z1+width-1, x1+width-1, y1, z1+width-1, height, altHeight,distribution)

def square(x,y,z,width,height,distribution):
    crenellatedSquare(x,y,z,width,height,height,distribution)

def moatSquare(x1,y1,z1,width,depth):
    moatSide(x1, y1, z1, x1+width-1, y1, z1, depth)
    moatSide(x1, y1, z1, x1, y1, z1+width-1, depth)
    moatSide(x1+width-1, y1, z1, x1+width-1, y1, z1+width-1, depth)
    moatSide(x1, y1, z1+width-1, x1+width-1, y1, z1+width-1, depth)

def crenellatedSquareWithInnerWall(x,y,z,width,baseHeight,altHeight,distribution):
    crenellatedSquare(x,y,z,width,baseHeight,altHeight,distribution)
    square(x+1,y,z+1,width-2,baseHeight-1,distribution)

def tower(x,y,z,width,baseHeight,altHeight,innerHeight,distribution):
    crenellatedSquareWithInnerWall(x,y,z,width,baseHeight,altHeight,distribution)
    rectangularPrism(x+2,y+innerHeight-1,z+2, x+width-3,y+innerHeight-1,z+width-3, distribution)

mc = Minecraft()
pos = mc.player.getTilePos()

distribution = ((.05,block.MOSS_STONE), (.1,Block(block.STONE_BRICK.id, 1)), 
                (.2,Block(block.STONE_BRICK.id, 2)),
                (.651,Block(block.STONE_BRICK.id, 0)))

wallSize = 51
groundY = 1+getHeightBelow(pos.x, pos.y, pos.z)

# outer walls
mc.postToChat("Outer walls")
crenellatedSquareWithInnerWall(pos.x,groundY,pos.z, wallSize, 9, 10, distribution)

# towers
mc.postToChat("Towers")
tower(pos.x-7,groundY,pos.z-7, 9, 12, 13, 11, distribution)
tower(pos.x+wallSize-2,groundY,pos.z+wallSize-2, 9, 12, 13, 11, distribution)
tower(pos.x-7,groundY,pos.z+wallSize-2, 9, 12, 13, 11, distribution)
tower(pos.x+wallSize-1,groundY,pos.z-7, 9, 12, 13, 11, distribution)

# keep
mc.postToChat("Keep")
keepStartX = pos.x+wallSize/4
keepStartZ = pos.z+wallSize/4
keepWidth = wallSize / 6 * 3
tower(keepStartX,groundY, keepStartZ,keepWidth, 16, 17, 15, distribution)

# moat
if len(sys.argv) <= 1 or sys.argv[1][0] != 'n':
    mc.postToChat("Moat")
    moatStartX = pos.x - 12
    moatStartZ = pos.z - 12
    moatInnerSize = wallSize+24
    
    for i in range(6):
        moatSquare(moatStartX-i,groundY-1,moatStartZ-i,moatInnerSize+2*i,2)

mc.postToChat("Castle done")

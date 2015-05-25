from mc import *

def deleteCubes(x0,y0,z0,length):
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
                    mc.setBlocks(posX,posY,posZ,
                                 posX+length-1,posY+length-1,posZ+length-1,AIR)
                else:
                    deleteCubes(posX,posY,posZ,length)

mc = Minecraft()
playerPos = mc.player.getPos()
length = 3*3*3*3
mc.setBlocks(playerPos.x,playerPos.y,playerPos.z,
             playerPos.x+length-1,playerPos.y+length-1,playerPos.z+length-1,WOOL_PURPLE)
deleteCubes(playerPos.x,playerPos.y,playerPos.z,length)


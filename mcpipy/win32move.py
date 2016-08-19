from mine import *
from time import sleep
from sys import argv
import input

mc = Minecraft()

player = True

if len(argv)>=2 and argv[1] != "me":
    playerPos = mc.player.getPos()
    playerYaw = mc.player.getRotation()
    entity = mc.spawnEntity(argv[1], playerPos.x - sin(radians(playerYaw)), playerPos.z, 
                playerPos.z + cos(radians(playerYaw)), "{NoAI:1}")
    player = False
else:        
    entity = mc.getPlayerId()

lastPlatform = None
lastPlatformBlock = None

UNSOLID = set([block.WATER_FLOWING.id,block.WATER_STATIONARY.id,block.AIR.id,block.LAVA_FLOWING.id,block.LAVA_STATIONARY.id])

while True:
    pos = mc.entity.getPos(entity)
    yaw = mc.entity.getRotation(entity)
    move = False
    if input.wasPressedSinceLast(input.NEXT):
        pos.y -= 1
        move = True
    if input.wasPressedSinceLast(input.PRIOR):
        pos.y += 1
        move = True
    if input.wasPressedSinceLast(input.LEFT):
        yaw -= 15
        mc.entity.setRotation(entity,yaw)
    if input.wasPressedSinceLast(input.RIGHT):
        yaw += 15
        mc.entity.setRotation(entity,yaw)
    if input.wasPressedSinceLast(input.UP):
        pos.x += .5 * -sin(radians(yaw))
        pos.z += .5 * cos(radians(yaw))
        move = True
    if input.wasPressedSinceLast(input.DOWN):
        pos.x -= .5 * -sin(radians(yaw))
        pos.z -= .5 * cos(radians(yaw))
        move = True
    if move:
        if player:
            under = (int(floor(pos.x)),int(floor(pos.y))-1,int(floor(pos.z)))
            b = mc.getBlock(under)
            if b in UNSOLID:
                drew = under
                mc.setBlock(drew,block.GLASS)
            else:
                drew = None
            mc.entity.setPos(entity,pos)
            if lastPlatform is not None and lastPlatform != under:
                mc.setBlock(lastPlatform,block.AIR)
                lastPlatform = None
            if drew:
                lastPlatform = drew
                lastPlatformBlock = b
        else:
            mc.entity.setPos(entity,pos)
    sleep(0.2)
    
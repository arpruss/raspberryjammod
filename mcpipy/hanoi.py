from mine import *
from time import sleep

def drawPillar(n,h1,h2):
    mc.setBlocks(pillarPos[n].x, pillarPos[n].y+h1, pillarPos[n].z,
        pillarPos[n].x, pillarPos[n].y+h2, pillarPos[n].z, block.STONE)

def drawRing(n, height, ring):
    size = ring
    mc.setBlocks(pillarPos[n].x-size, pillarPos[n].y+height, pillarPos[n].z-size,
        pillarPos[n].x+size, pillarPos[n].y+height, pillarPos[n].z+size, block.WOOL_RED)
    drawPillar(n, height, height)
    
def eraseRing(n, height, ring):
    size = ring
    mc.setBlocks(pillarPos[n].x-size, pillarPos[n].y+height, pillarPos[n].z-size,
        pillarPos[n].x+size, pillarPos[n].y+height, pillarPos[n].z+size, block.AIR)
    drawPillar(n, height, height)
    
def moveRing(source, dest):
    ring = pillars[source].pop()
    eraseRing(source, len(pillars[source]), ring)
    drawRing(dest, len(pillars[dest]), ring)
    pillars[dest].append(ring)
    sleep(delay)
    
def moveRings(source, dest, helper, count):
    if count == 1:
        moveRing(source, dest)
    else:
        moveRings(source, helper, dest, count-1)
        moveRing(source, dest)
        moveRings(helper, dest, source, count-1)        
        
mc = Minecraft()

playerPos = mc.player.getPos()

delay = 0.25

pillarPos = [Vec3(playerPos.x-20,playerPos.y,playerPos.z-10),
                Vec3(playerPos.x,playerPos.y,playerPos.z-10),
                Vec3(playerPos.x+20,playerPos.y,playerPos.z-10)]

pillars = [ [8,7,6,5,4,3,2,1], [], [] ]

for i in range(3):
    drawPillar(i,0,len(pillars[0])+1)

for i in range(len(pillars[0])):
    drawRing(0, i, pillars[0][i])

moveRings(0, 2, 1, len(pillars[0]))        

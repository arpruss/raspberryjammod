from .mc import *
import os
import time

RADIUS = 5
THICKNESS = 2

def setBlock(pos, block):
    if not pos in records or records[pos] != block:
        records[pos] = block
        mc.setBlock(pos, block)

def sphere(dictionary,x0,y0,z0,R,thickness,block):
    R2 = R*R
    r = R-thickness
    r2 = r*r
    for x in range(-R,R+1):
        for y in range(-R,R+1):
            for z in range(-R,R+1):
                dist2 = x*x+y*y+z*z
                if dist2 <= r2:
                    dictionary[(x0+x,y0+y,z0+z)] = AIR
                elif dist2 <= R2:
                    dictionary[(x0+x,y0+y,z0+z)] = block

def platform(dictionary,x0,y0,z0,block):
     dictionary[(x0,y0-1,z0)] = block

def draw(dictionary):
    for pos in dictionary:
        setBlock(pos,dictionary[pos])

def light(x,y,z):
    setBlock((x,y-1,z+1),Block(TORCH.id, 3))
    setBlock((x,y-1,z-1),Block(TORCH.id, 4))
    setBlock((x-1,y-1,z),Block(TORCH.id, 2))
    setBlock((x+1,y-1,z),Block(TORCH.id, 1))

def unlight(x,y,z):
    setBlock((x,y-1,z+1),AIR)
    setBlock((x,y-1,z-1),AIR)
    setBlock((x-1,y-1,z),AIR)
    setBlock((x+1,y-1,z),AIR)


mc = Minecraft()
records = {}

try:
    player = int( os.environ['MINECRAFT_PLAYER_ID'] )
except:
    player = mc.getPlayerId()

prev = None
current = {}
while True:
    pos = mc.entity.getTilePos(player)
    if prev is None or prev != pos:
        dictionary = {}

        if not prev is None:
            unlight(prev.x,prev.y,prev.z)
            sphere(dictionary, prev.x, prev.y, prev.z, RADIUS, THICKNESS, AIR)
            platform(dictionary, prev.x, prev.y, prev.z, AIR)

        # or 166 for barrier
        sphere(dictionary, pos.x, pos.y, pos.z, RADIUS, THICKNESS, GLASS)
        platform(dictionary, pos.x, pos.y, pos.z, 1)
        draw(dictionary)
        if len(records) > 100000:
            records = {}

        light(pos.x, pos.y, pos.z)

        prev = pos
    time.sleep(0.1)

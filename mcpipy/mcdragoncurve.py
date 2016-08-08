#
# Code by Alexander Pruss and under the MIT license
#

import mcpi.minecraft as minecraft
import mcpi.block as block
import lsystem

mc = minecraft.Minecraft()
playerPos = mc.player.getPos()

DIRECTIONS = ((1,0),(0,1),(-1,0),(0,-1))

pos = (int(playerPos.x),int(playerPos.y),int(playerPos.z))
direction = 0

def go():
    global pos
    dx = DIRECTIONS[direction][0]
    dz = DIRECTIONS[direction][1]
    # draw a wall
    mc.setBlocks(pos,pos[0]+dx*4,pos[1]+4,pos[2]+dz*4,block.BRICK_BLOCK)
    # draw a door in it
    mc.setBlocks(pos[0]+dx*2,pos[1],pos[2]+dz*2,pos[0]+dx*2,pos[1]+1,pos[2]+dz*2,block.AIR)
    pos = (pos[0]+dx*4, pos[1], pos[2]+dz*4)

def left():
    global direction
    direction -= 1
    if direction == -1:
        direction = 3

def right():
    global direction
    direction += 1
    if direction == 4:
        direction = 0

rules = {'X':'X+YF+', 'Y':'-FX-Y'}
dictionary = { '+': left,
               '-': right,
               'F': go }

lsystem.lsystem('FX', rules, dictionary, 14)

#go()

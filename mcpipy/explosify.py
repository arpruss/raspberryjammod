#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
import math
import sys

def replace(mcx,mcy,mcz,R,mcblock):
  for x in range(-R,R):
     for y in range(-R,R):
         for z in range(-R,R):
            if (x**2 + y**2 + z**2 <= R**2 and mc.getBlock(mcx+x,mcy+y,mcz+z) != block.AIR.id):
                mc.setBlock(mcx+x,mcy+y,mcz+z,mcblock)

mc = Minecraft()

playerPos = mc.player.getPos()
R = 20
b = block.TNT

if len(sys.argv) >= 2:
   R = int(sys.argv[1])
   if len(sys.argv) >= 3:
      b = Block.byName(sys.argv[2])

replace(playerPos.x, playerPos.y, playerPos.z, R, b)

mc.postToChat("Explosify done")

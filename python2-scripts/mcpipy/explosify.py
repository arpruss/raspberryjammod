#
# Code under the MIT license by Alexander Pruss
#

import mcpi.minecraft as minecraft
import mcpi.block as block
import math
import sys

def replace(mcx,mcy,mcz,R,mcblock,mcmeta):
  for x in range(-R,R):
     for y in range(-R,R):
         for z in range(-R,R):
            if (x**2 + y**2 + z**2 <= R**2 and mc.getBlock(mcx+x,mcy+y,mcz+z) != block.AIR.id):
                mc.setBlock(mcx+x,mcy+y,mcz+z,mcblock,mcmeta)

mc = minecraft.Minecraft()

playerPos = mc.player.getPos()
R = 20
b = block.TNT.id
m = 0

if len(sys.argv) >= 2:
   R = int(sys.argv[1])
   if len(sys.argv) >= 3:
      b = int(sys.argv[2])
      if len(sys.argv) >= 4:
          m  = int(sys.argv[3])

replace(playerPos.x, playerPos.y, playerPos.z, R, b, m)

mc.postToChat("Explosify done")

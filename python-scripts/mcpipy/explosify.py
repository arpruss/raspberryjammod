#
# Code under the MIT license by Alexander Pruss
#

from mc import *
import math
import sys
from ast import literal_eval

def parseBlock(s):
    try:
        return literal_eval(s)
    except:
        return globals()[s.upper()]

def replace(mcx,mcy,mcz,R,mcblock):
  for x in range(-R,R):
     for y in range(-R,R):
         for z in range(-R,R):
            if (x**2 + y**2 + z**2 <= R**2 and mc.getBlock(mcx+x,mcy+y,mcz+z) != AIR.id):
                mc.setBlock(mcx+x,mcy+y,mcz+z,mcblock)

mc = Minecraft()

playerPos = mc.player.getPos()
R = 20
b = TNT

if len(sys.argv) >= 2:
   R = int(sys.argv[1])
   if len(sys.argv) >= 3:
      b = parseBlock(sys.argv[2])

replace(playerPos.x, playerPos.y, playerPos.z, R, b)

mc.postToChat("Explosify done")

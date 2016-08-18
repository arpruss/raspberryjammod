#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
import time
import os

mc = Minecraft()

bridge = []

while True:
   pos = mc.player.getTilePos()
   pos.y = pos.y - 1
   belowBlock = mc.getBlock(pos)
   if belowBlock == block.AIR.id or belowBlock == block.WATER_FLOWING.id or belowBlock == block.WATER_STATIONARY.id:
     bridge.append(pos)
     mc.setBlock(pos, block.STAINED_GLASS_BLUE)
     if len(bridge) > 10:
         firstPos = bridge.pop(0)
         if not firstPos in bridge:
             mc.setBlock(firstPos, block.AIR)
   time.sleep(0.05)

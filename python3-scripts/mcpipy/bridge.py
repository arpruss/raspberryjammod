#
# Code under the MIT license by Alexander Pruss
#


from mc import *
import time
import os

mc = Minecraft()

try:
   playerId = int(os.environ['MINECRAFT_PLAYER_ID'])
   getTilePos = lambda: mc.entity.getTilePos(playerId)
except:
   getTilePos = mc.player.getTilePos

bridge = []

while True:
   pos = getTilePos()
   pos.y = pos.y - 1
   belowBlock = mc.getBlock(pos)
   if belowBlock == AIR.id or belowBlock == WATER_FLOWING.id or belowBlock == WATER_STATIONARY.id:
     bridge.append(pos)
     mc.setBlock(pos, STAINED_GLASS_BLUE)
     if len(bridge) > 10:
         firstPos = bridge.pop(0)
         if not firstPos in bridge:
             mc.setBlock(firstPos, AIR)
   time.sleep(0.05)

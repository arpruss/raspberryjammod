#
# MIT-licensed code by Alexander Pruss
#


from mc import *
import time

mc = Minecraft()

bridge = []

previousPos = None

while True:
   pos = mc.player.getTilePos()
   if previousPos is None or pos != previousPos:
       belowBlock = mc.getBlock(pos.x, pos.y - 1, pos.z)
       if belowBlock == AIR.id or belowBlock == WATER_FLOWING.id or belowBlock == WATER_STATIONARY.id:
           bridge.append(pos)
           mc.setBlock(pos.x, pos.y - 1, pos.z, STAINED_GLASS_BLUE)
           if len(bridge) > 10:
               firstPos = bridge.pop(0)
               if not firstPos in bridge:
                   mc.setBlock(firstPos.x, firstPos.y - 1, firstPos.z, AIR)
   previousPos = pos
   time.sleep(0.05)

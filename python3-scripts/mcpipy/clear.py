from mc import *


mc = Minecraft()
pos = mc.player.getTilePos()

mc.setBlocks(pos.x-100, pos.y, pos.z-100,
             pos.x+100, pos.y+100, pos.z+100,
             AIR)

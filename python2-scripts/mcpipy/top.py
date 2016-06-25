from mc import *

mc = Minecraft()

playerPos = mc.player.getTilePos()
mc.player.setPos(playerPos.x, mc.getHeight(playerPos.x, playerPos.z)+1, playerPos.z)

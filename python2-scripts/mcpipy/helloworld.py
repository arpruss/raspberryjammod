import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import sys
mc = minecraft.Minecraft()
mc.postToChat("Hello world!")
playerPos = mc.player.getPos()
mc.setBlock(playerPos.x,playerPos.y-1,playerPos.z,block.DIAMOND_ORE)

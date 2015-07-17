from . import mcpi.minecraft as minecraft
from . import mcpi.block as block
from . import server
import sys
mc = minecraft.Minecraft.create(server.address)
mc.postToChat("Hello world!")
playerPos = mc.player.getPos()
mc.setBlock(playerPos.x,playerPos.y-1,playerPos.z,block.DIAMOND_ORE)

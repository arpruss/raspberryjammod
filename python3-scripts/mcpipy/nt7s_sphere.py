#!/usr/bin/env python

# mcpipy.com retrieved from URL below, written by  Jason Milldrum, NT7S
# http://www.nt7s.com/blog/2013/02/exploring-minecraft-pi-edition/


from . import mcpi.minecraft as minecraft
from . import mcpi.block as block
from . import server


mc = minecraft.Minecraft.create(server.address)

radius = 8

mc.postToChat("Hello, here's your sphere")

playerPos = mc.player.getPos()

for x in range(radius*-1,radius):
	for y in range(radius*-1, radius):
		for z in range(radius*-1,radius):
			if x**2 + y**2 + z**2 < radius**2:
				mc.setBlock(playerPos.x + x, playerPos.y + y + radius, playerPos.z - z - 10, block.GLASS)
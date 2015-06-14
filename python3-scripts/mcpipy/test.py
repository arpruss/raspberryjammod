#!/usr/bin/env python

from . import mcpi.minecraft as minecraft
from . import mcpi.block as block
from . import server
import math

mc = minecraft.Minecraft.create(server.address)
mc.player.setPos(0,3,4)
print("hello")
mc.setBlock(0,0,0,3,0)
print(mc.getBlock(0,0,0))
pos = mc.player.getPos()
pos.x = pos.x - 10
print(mc.player.getPitch())
print(mc.player.getRotation())
print(mc.player.getDirection())

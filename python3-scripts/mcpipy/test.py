#!/usr/bin/env python

import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import math

mc = minecraft.Minecraft.create(server.address)
mc.setBlock(0,0,0,3,0)
print(mc.getBlock(0,0,0))

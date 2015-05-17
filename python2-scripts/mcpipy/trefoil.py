#!/usr/bin/env python

#
# (c) 2015 Alexander R. Pruss
#
# Available under MIT license
#

#
# Draw a trefoil
#

import mcpi.minecraft as minecraft
import mcpi.block as block
import server
from math import *

def draw_data(x0,y0,z0,data):
  for key in data:
     mc.setBlock(x0+key[0],y0+key[1],z0+key[2],data[key])

def ball(x0,y0,z0,r,block_type,data):
  for x in range(-r,r):
    for y in range(-r,r):
      for z in range(-r,r):
         if (x**2 + y**2 + z**2 <= r**2):
            data[x0+x,y0+y,z0+z] = block_type


knot = {}
scale = 12
t = 0
while t < 2*pi:
# trefoil from http://en.wikipedia.org/wiki/Trefoil_knot
  x = int( scale * (sin(t) + 2 * sin(2*t)) )
  y = int( scale * (cos(t) - 2 * cos(2*t)) )
  z = int( scale * -sin(3*t) )
  ball(x,y,z,5,block.GOLD_BLOCK,knot)
  t += 2*pi / 10000

mc = minecraft.Minecraft.create(server.address)
playerPos = mc.player.getPos()
draw_data(playerPos.x,playerPos.y + 3.5 * scale,playerPos.z,knot)

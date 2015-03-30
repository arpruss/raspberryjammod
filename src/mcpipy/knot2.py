#!/usr/bin/env python

#
# (c) 2015 Alexander R. Pruss
#
# Available under MIT license
#

#
# Draw a water-filled donut
#

import mcpi.minecraft as minecraft
import mcpi.block as block
import server
from math import *

def draw_data(x0,y0,z0,data):
  for key in data:
     mc.setBlock(x0+key[0],y0+key[1],z0+key[2],data[x,y,z])

def ball(x0,y0,z0,r,block,data):
  for x in range(-r,r):
    for y in range(-r,r):
      for z in range(-r,r):
         if (x**2 + y**2 + z**2 <= r**2):
            data[x0+x,y0+y,z0+z] = block


knot = {}
scale = 10
t = 0
while t < 2*pi:
# cinquefoil from http://www.maa.org/sites/default/files/images/upload_library/23/stemkoski/knots/page6.html
  x = int( scale * cos(2*t) * (3 + cos(5*t)) )
  y = int( scale * sin(2*t) * (3 + cos(5*t)) )
  z = int( scale * sin(5*t) )
  ball(x,y,z,4,block.GOLD_BLOCK,knot)
  t += 2*pi / 10000

mc = minecraft.Minecraft.create(server.address)
playerPos = mc.player.getPos()
draw_data(playerPos.x,playerPos.y + 5 * scale,playerPos.z,knot)

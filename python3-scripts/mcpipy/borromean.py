#!/usr/bin/env python

#
# (c) 2015 Alexander R. Pruss
#
# Available under MIT license
#

#
# Draw Borromean rings
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

mc = minecraft.Minecraft.create(server.address)
playerPos = mc.player.getPos()

scale = 30
r = sqrt(3)/3

# parametrization by I.J.McGee

knot = {}
t = 0
while t < 2*pi:
  x = int( scale * cos(t) )
  y = int( scale * ( sin(t) + r) )
  z = int( scale * - cos(3*t)/3 )
  ball(x,y,z,4,block.GOLD_BLOCK,knot)
  t += 2*pi / 10000
draw_data(playerPos.x,playerPos.y + 4+ (r/2+1) * scale,playerPos.z,knot)

knot = {}
t = 0
while t < 2*pi:
  x = int( scale * (cos(t) + 0.5) )
  y = int( scale * ( sin(t) - r/2) )
  z = int( scale * - cos(3*t)/3 )
  ball(x,y,z,4,block.LAPIS_LAZULI_BLOCK,knot)
  t += 2*pi / 10000
draw_data(playerPos.x,playerPos.y + 4+ (r/2+1) * scale,playerPos.z,knot)

knot = {}
t = 0
while t < 2*pi:
  x = int( scale * ( cos(t) - 0.5 ) )
  y = int( scale * ( sin(t) - r/2) )
  z = int( scale * - cos(3*t)/3 )
  ball(x,y,z,4,block.DIAMOND_BLOCK,knot)
  t += 2*pi / 10000
draw_data(playerPos.x,playerPos.y + 4 + (r/2+1) * scale,playerPos.z,knot)


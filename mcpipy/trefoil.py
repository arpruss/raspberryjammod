#!/usr/bin/env python

#
# Code by Alexander Pruss and under the MIT license
#

#
# Draw a trefoil
#

from mine import *

def ball(x0,y0,z0,r,block_type,done):
  for x in range(-r,r):
    for y in range(-r,r):
      for z in range(-r,r):
         if (x**2 + y**2 + z**2 <= r**2):
            if not (x0+x,y0+y,z0+z) in done:
                mc.setBlock(x0+x,y0+y,z0+z,block_type)
                done.add((x0+x,y0+y,z0+z))


mc = Minecraft()
playerPos = mc.player.getPos()

scale = 12
x0 = int(playerPos.x)
y0 = int(playerPos.y + 3.5 * scale)
z0 = int(playerPos.z)

done = set()
t = 0
while t < 2*pi:
# trefoil from http://en.wikipedia.org/wiki/Trefoil_knot
  x = x0+int( scale * (sin(t) + 2 * sin(2*t)) )
  y = y0+int( scale * (cos(t) - 2 * cos(2*t)) )
  z = z0+int( scale * -sin(3*t) )
  ball(x,y,z,5,block.GOLD_BLOCK,done)
  t += 2*pi / 10000

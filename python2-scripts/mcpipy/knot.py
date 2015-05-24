#!/usr/bin/env python

#
# (c) 2015 Alexander R. Pruss
#
# Available under MIT license
#

#
# Draw a knot
#

from mc import *

mc = Minecraft()
playerPos = mc.player.getPos()

scale = 10
t = 0
done = {}
while t < 2*pi:
# cinquefoil from http://www.maa.org/sites/default/files/images/upload_library/23/stemkoski/knots/page6.html
  x = playerPos.x+int( scale * cos(2*t) * (3 + cos(5*t)) )
  y = playerPos.y+5*scale+int( scale * sin(2*t) * (3 + cos(5*t)) )
  z = playerPos.z+int( scale * sin(5*t) )
  if (x,y,z) not in done:
      mc.setBlock(x,y,z,GOLD_BLOCK)
      done[x,y,z] = GOLD_BLOCK
  t += 2*pi / 10000

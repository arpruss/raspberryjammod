#
# Code by Alexander Pruss and under the MIT license
#

#
# Draw a knot
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
playerPos = mc.player.getTilePos()

scale = 10

done = set()
t = 0
while t < 2*pi:
# cinquefoil from http://www.maa.org/sites/default/files/images/upload_library/23/stemkoski/knots/page6.html
  x = playerPos.x+int( scale * cos(2*t) * (3 + cos(5*t)) )
  y = playerPos.y+int( scale * sin(2*t) * (3 + cos(5*t)) )
  z = playerPos.z+int( scale * sin(5*t) )
  ball(x,y,z,4,block.GLOWSTONE_BLOCK,done)
  t += 2*pi / 10000

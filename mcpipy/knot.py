#
# Code under the MIT license by Alexander Pruss
#

#
# Draw a knot
#

from mc import *

mc = Minecraft()
playerPos = mc.player.getPos()
scale = 10
x0 = int(playerPos.x)
y0 = int(playerPos.y+5*scale)
z0 = int(playerPos.z)
t = 0
done = set()
while t < 2*pi:
# cinquefoil from http://www.maa.org/sites/default/files/images/upload_library/23/stemkoski/knots/page6.html
  x = x0+int( scale * cos(2*t) * (3 + cos(5*t)) )
  y = y0+5*scale+int( scale * sin(2*t) * (3 + cos(5*t)) )
  z = z0+int( scale * sin(5*t) )
  if (x,y,z) not in done:
      mc.setBlock(x,y,z,GOLD_BLOCK)
      done.add((x,y,z))
  t += 2*pi / 10000

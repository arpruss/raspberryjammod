#
# Code by Alexander Pruss and under the MIT license
#

#
# Draw Borromean rings
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

scale = 30
r = sqrt(3)/3


x0 = int(playerPos.x)
y0 = int(playerPos.y + 4 + (r/2+1) * scale)
z0 = int(playerPos.z)


# parametrization by I.J.McGee
done = set()
t = 0
while t < 2*pi:
  x = x0+int( scale * cos(t) )
  y = y0+int( scale * ( sin(t) + r) )
  z = z0+int( scale * - cos(3*t)/3 )
  ball(x,y,z,4,block.GOLD_BLOCK,done)
  t += 2*pi / 10000

done = set()
t = 0
while t < 2*pi:
  x = x0+int( scale * (cos(t) + 0.5) )
  y = y0+int( scale * ( sin(t) - r/2) )
  z = z0+int( scale * - cos(3*t)/3 )
  ball(x,y,z,4,block.LAPIS_LAZULI_BLOCK,done)
  t += 2*pi / 10000

done = set()
t = 0
while t < 2*pi:
  x = x0+int( scale * ( cos(t) - 0.5 ) )
  y = y0+int( scale * ( sin(t) - r/2) )
  z = z0+int( scale * - cos(3*t)/3 )
  ball(x,y,z,4,block.DIAMOND_BLOCK,done)
  t += 2*pi / 10000

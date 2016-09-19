#
# Code by Alexander Pruss and under the MIT license
#

#
# Draw a knot
#
# python knot3.py variable1=value1 variable2=value2 ...
#
from mine import *
from sys import argv
import colors

def ball(x0,y0,z0,r,block_type,done):
  for x in range(-r,r):
    for y in range(-r,r):
      for z in range(-r,r):
         if (x**2 + y**2 + z**2 <= r**2):
            if not (x0+x,y0+y,z0+z) in done:
                mc.setBlock(x0+x,y0+y,z0+z,block_type)
                done.add((x0+x,y0+y,z0+z))

def ditheredBall(x0,y0,z0,r,rgb,done):
  for x in range(-r,r):
    for y in range(-r,r):
      for z in range(-r,r):
         if (x**2 + y**2 + z**2 <= r**2):
            if not (x0+x,y0+y,z0+z) in done:
                mc.setBlock(x0+x,y0+y,z0+z,colors.rgbToBlock(rgb, randomDither=30))
                done.add((x0+x,y0+y,z0+z))

mc = Minecraft()
playerPos = mc.player.getTilePos()

# see http://www.mi.sanu.ac.rs/vismath/taylor2009/index.html

p = 1
q = -2
h = 0.35
t = 3
m = 1
n = 1.5
scale = 15
width = 2

for i in range(1,len(argv)):
    variable,value = argv[i].split("=")
    if variable == "m":
        m = float(value)
    elif variable == "n":
        n = float(value)
    elif variable == "p":
        p = float(value)
    elif variable == "q":
        q = float(value)
    elif variable == "t":
        t = float(value)
    elif variable == "h":
        h = float(value)
    elif variable == "scale":
        scale = float(value)
    elif variable == "width":
        width = float(value)

yOffset = abs(m)+abs(n)+1

done = set()
th = 0

while th < 2*pi:
  x = m * cos(p * th) + n * cos(q * th)
  y = m * sin(p * th) + n * sin(q * th)
  z = h * sin(t * th)
  
  x = playerPos.x + int(scale * x)
  y = playerPos.y + int(scale * (yOffset+y)) 
  z = playerPos.z + int(scale * z)

  hue = 180 * th / pi + 180 if th < pi else 360+180 - 180 * th / pi 
  ditheredBall(x,y,z,width,colors.hsvToRGB(hue, 1, 1),done)

  th += 2*pi / 10000

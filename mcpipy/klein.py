#
# Code by Alexander Pruss and under the MIT license
#

from mine import *

def draw_surface(xf,yf,zf,a0,a1,asteps,b0,b1,bsteps,ox,oy,oz,scalex,scaley,scalez,mcblock,mcmeta):
  for i in range(asteps):
     a = (a0 * (asteps-1-i) + a1 * i) / asteps
     for j in range(bsteps):
        b = (b0 * (bsteps-1-j) + b1 * j) / bsteps
        x = xf(a,b)
        y = yf(a,b)
        z = zf(a,b)
        mc.setBlock(ox+x * scalex, oy+y * scaley, oz+z * scalez, mcblock, mcmeta)

mc = Minecraft()
playerPos = mc.player.getPos()

# formula from http://paulbourke.net/geometry/klein/

xformula = lambda a,b: (6 * cos(a) * (1 + sin(a)) + 4 * (1 - cos(a) / 2) * cos(a) * cos(b)) if (a <= pi) else (6 * cos(a) * (1 + sin(a)) + 4 * (1 - cos(a) / 2) * cos(b + pi))
yformula = lambda a,b: 16 * sin(a) + 4 * (1-cos(a)) * sin(a) * cos(b) if a <= pi else 16 * sin(a)
zformula = lambda a,b: 4 * (1- cos(a)/2) * sin(b)

scale = 3

b = block.STAINED_GLASS.id
m = 5

draw_surface(xformula,yformula,zformula,0,2*pi,150*scale,0,2*pi,150*scale,playerPos.x,playerPos.y+16*scale,playerPos.z,scale,scale,scale,b, m)
#mc.postToChat("Formula done")

#
# Code under the MIT license by Alexander Pruss
#

from mc import *
import sys

def draw_surface(xf,yf,zf,a0,a1,asteps,b0,b1,bsteps,ox,oy,oz,scalex,scaley,scalez,mcblock,mcmeta):
  cfx = compile(xf,'<string>','eval')
  cfy = compile(yf,'<string>','eval')
  cfz = compile(zf,'<string>','eval')

  for i in range(asteps):
     a = (a0 * (asteps-1-i) + a1 * i) / asteps
     for j in range(bsteps):
        b = (b0 * (bsteps-1-j) + b1 * j) / bsteps
        x = eval(cfx)
        y = eval(cfy)
        z = eval(cfz)
        mc.setBlock(ox+x * scalex, oy+y * scaley, oz+z * scalez, mcblock, mcmeta)

mc = Minecraft()
playerPos = mc.player.getPos()

# formula from http://paulbourke.net/geometry/klein/

xformula = '(6 * cos(a) * (1 + sin(a)) + 4 * (1 - cos(a) / 2) * cos(a) * cos(b)) if (a <= pi) else (6 * cos(a) * (1 + sin(a)) + 4 * (1 - cos(a) / 2) * cos(b + pi))'
yformula = '16 * sin(a) + 4 * (1-cos(a)) * sin(a) * cos(b) if a <= pi else 16 * sin(a)'
zformula = '4 * (1- cos(a)/2) * sin(b)'

scale = 3

b = STAINED_GLASS.id
m = 5

if (len(sys.argv)>1):
   b = int(sys.argv[1])
   if (len(sys.argv)>2):
      m = int(sys.argv[2])

draw_surface(xformula,yformula,zformula,0,2*pi,150*scale,0,2*pi,150*scale,playerPos.x,playerPos.y+16*scale,playerPos.z,scale,scale,scale,b, m)
#mc.postToChat("Formula done")

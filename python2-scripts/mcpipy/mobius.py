#
# Code under the MIT license by Alexander Pruss
#

from mc import *
import sys

def draw_surface(xf,yf,zf,a0,a1,asteps,b0,b1,bsteps,ox,oy,oz,scalex,scaley,scalez,mcblock,mcmeta):
  cfx = compile(xf,'<string>','eval')
  cfy = compile(yf,'<string>','eval')
  cfz = compile(zf,'<string>','eval')

  for i in xrange(asteps):
     a = (a0 * (asteps-1-i) + a1 * i) / asteps
     for j in xrange(bsteps):
        b = (b0 * (bsteps-1-j) + b1 * j) / bsteps
        x = eval(cfx)
        y = eval(cfy)
        z = eval(cfz)
#        print a,b,ox+x * scalex, oy+y * scaley, oz+z * scalez
        mc.setBlock(ox+x * scalex, oy+y * scaley, oz+z * scalez, mcblock, mcmeta)

mc = Minecraft()
playerPos = mc.player.getPos()

xformula = '(3 + a * cos(b/2)) * cos(b)'
yformula = 'a * sin(b/2)'
zformula = '(3 + a * cos(b/2)) * sin(b)'

scale = 15

b = STONE
m = 0

if (len(sys.argv)>1):
   b = int(sys.argv[1])
   if (len(sys.argv)>2):
      m = int(sys.argv[2])

draw_surface(xformula,yformula,zformula,-1.,1.,10*scale,0,2*pi,30*scale,playerPos.x,playerPos.y+scale,playerPos.z,scale,scale,scale,b, m)
mc.postToChat("Formula done")

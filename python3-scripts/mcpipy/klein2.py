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
     u = (a0 * (asteps-1-i) + a1 * i) / asteps
     for j in range(bsteps):
        v = (b0 * (bsteps-1-j) + b1 * j) / bsteps
        x = eval(cfx)
        y = eval(cfy)
        z = eval(cfz)
        mc.setBlock(ox+x * scalex, oy+y * scaley, oz+z * scalez, mcblock, mcmeta)

mc = Minecraft()
playerPos = mc.player.getPos()

scale = 3

b = STAINED_GLASS.id
m = 5

arg = 1

if (len(sys.argv)>arg):
   b = int(sys.argv[arg])
   arg += 1
   if (len(sys.argv)>arg):
      m = int(sys.argv[arg])
      arg += 1

# http://www.gnuplotting.org/klein-bottle/

xformula = '(2.5-1.5*cos(v))*cos(u)'
zformula = '(2.5-1.5*cos(v))*sin(u)'
yformula = '-2.5*sin(v)'

draw_surface(xformula,yformula,zformula,0,2*pi,50*scale,0,pi,50*scale,playerPos.x,playerPos.y+2.5*scale,playerPos.z,scale,scale,scale,b, m)
mc.postToChat("Part 1 done")

if (len(sys.argv)>arg):
   b = int(sys.argv[arg])
   arg += 1
   if (len(sys.argv)>arg):
      m = int(sys.argv[arg])
      arg += 1

xformula = '(2.5-1.5*cos(v))*cos(u)'
zformula = '(2.5-1.5*cos(v))*sin(u)'
yformula = '3*v - 3*pi'

draw_surface(xformula,yformula,zformula,0,2*pi,50*scale,pi,2*pi,50*scale,playerPos.x,playerPos.y+2.5*scale,playerPos.z,scale,scale,scale,b,m)
mc.postToChat("Part 2 done")

if (len(sys.argv)>arg):
   b = int(sys.argv[arg])
   arg += 1
   if (len(sys.argv)>arg):
      m = int(sys.argv[arg])
      arg += 1

xformula = '-2+2*cos(v)-cos(u)'
zformula = 'sin(u)'
yformula = '(2+cos(u))*sin(v)+3*pi'

draw_surface(xformula,yformula,zformula,0,2*pi,50*scale,2*pi,3*pi,50*scale,playerPos.x,playerPos.y+2.5*scale,playerPos.z,scale,scale,scale,b,m)
mc.postToChat("Part 3 done")

if (len(sys.argv)>arg):
   b = int(sys.argv[arg])
   arg += 1
   if (len(sys.argv)>arg):
      m = int(sys.argv[arg])
      arg += 1

xformula = '-2+2*cos(v)-cos(u)'
zformula = 'sin(u)'
yformula = '-3*v+12*pi'

draw_surface(xformula,yformula,zformula,0,2*pi,50*scale,3*pi,4*pi,50*scale,playerPos.x,playerPos.y+2.5*scale,playerPos.z,scale,scale,scale,b,m)

mc.postToChat("Formula done")

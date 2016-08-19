#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
import drawing
from sys import argv
import mcpi.settings as settings

RAINBOW = (block.WOOL_RED,block.WOOL_PINK,block.WOOL_ORANGE,
            block.WOOL_YELLOW,block.WOOL_GREEN,block.WOOL_BLUE,
            block.WOOL_LIGHT_BLUE,block.WOOL_PURPLE)

TAN30 = sqrt(3.)/3
SQRT32 = sqrt(3./2)

def distance(a,b):
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def tetrahedronBottom(height, apex):
    side = SQRT32*height
    return ( (apex[0]-0.5*TAN30*side,apex[1]-height,apex[2]-0.5*side),
       (apex[0]-0.5*TAN30*side,apex[1]-height,apex[2]+0.5*side),
       (apex[0]+TAN30*side,apex[1]-height,apex[2]) )

def drawTetrahedron(height, apex, block):
    bottom = tetrahedronBottom(height, apex)
    for i in range(int(round(height))+1):
        triangle = []
        for point in bottom:
            a = float(i)/height
            triangle.append(((1-a)*apex[0]+a*point[0],apex[1]-i,(1-a)*apex[2]+a*point[2]))
        d.face(triangle,block)
    return triangle

def average(a,b):
    return tuple(0.5*(a[i]+b[i]) for i in range(len(a)))

def transform(tet):
    level, height, apex = tet[0],tet[1],tet[2]
    bottom = tetrahedronBottom(height,apex)
    yield (level,height/2.,apex)
    for p in bottom:
        yield (level+1,height/2.,average(apex,p))

def sierpinski(height, x,y,z, level):
    tetrahedra = [(0,height,(x,y,z))]
    for i in range(level):
        out = []
        for tet in tetrahedra:
            out += transform(tet)
        tetrahedra = out
    return tetrahedra

mc = Minecraft()
d = drawing.Drawing(mc)
pos = mc.player.getPos()
height = 240 if not settings.isPE else 128
levels = 7
mc.player.setPos(tetrahedronBottom(height,(pos.x,pos.y+height,pos.z))[0])
tetrahedra = sierpinski(height,pos.x,pos.y+height,pos.z,levels)
mc.postToChat("Drawing")
if len(argv) >= 2:
    specifiedBlock = Block.byName(argv[1])
    b = lambda level : specifiedBlock
else:
    b = lambda level : RAINBOW[level % len(RAINBOW)]
for tet in tetrahedra:
    drawTetrahedron(tet[1],tet[2],b(tet[0]))

#
# Code by Alexander Pruss and under the MIT license
#

import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.entity import *
from math import *
from numbers import Number,Integral

class V3(tuple):
    def __new__(cls,*args):
        if len(args) == 1:
           return tuple.__new__(cls,tuple(*args))
        else:
           return tuple.__new__(cls,args)

    def dot(self,other):
        return self[0]*other[0]+self[1]*other[1]+self[2]*other[2]

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def __add__(self,other):
        other = tuple(other)
        return V3(self[0]+other[0],self[1]+other[1],self[2]+other[2])

    def __radd__(self,other):
        other = tuple(other)
        return V3(self[0]+other[0],self[1]+other[1],self[2]+other[2])

    def __sub__(self,other):
        other = tuple(other)
        return V3(self[0]-other[0],self[1]-other[1],self[2]-other[2])

    def __rsub__(self,other):
        other = tuple(other)
        return V3(other[0]-self[0],other[1]-self[1],other[2]-self[2])

    def __neg__(self):
        return V3(-self[0],-self[1],-self[2])

    def __pos__(self):
        return self

    def len2(self):
        return self[0]*self[0]+self[1]*self[1]+self[2]*self[2]

    def __abs__(self):
        return sqrt(self.len2())

    def __div__(self,other):
        if isinstance(other,Number):
            y = float(other)
            return V3(self[0]/y,self[1]/y,self[2]/y)
        else:
            return NotImplemented

    def __mul__(self,other):
        if isinstance(other,Number):
            return V3(self[0]*other,self[1]*other,self[2]*other)
        else:
            other = tuple(other)
            # cross product
            return V3(self[1]*other[2]-self[2]*other[1],self[2]*other[0]-self[0]*other[2],self[0]*other[1]-self[1]*other[0])

    def __rmul__(self,other):
        return self.__mul__(other)

    def __repr__(self):
        return "V3"+repr(tuple(self))

    def ifloor(self):
        return V3(int(floor(self[0])),int(floor(self[1])),int(floor(self[2])))

    def iceil(self):
        return V3(int(ceil(self[0])),int(ceil(self[1])),int(ceil(self[2])))

TO_RADIANS = pi / 180.
TO_DEGREES = 180. / pi
ICOS = [1,0,-1,0]
ISIN = [0,1,0,-1]

def makeMatrix(compass,vertical,roll):
    m0 = matrixMultiply(yawMatrix(compass), pitchMatrix(vertical))
    return matrixMultiply(m0, rollMatrix(roll))

def applyMatrix(m,v):
    if m is None:
       return v
    else:
       return V3(m[i][0]*v[0]+m[i][1]*v[1]+m[i][2]*v[2] for i in range(3))

def matrixDistanceSquared(m1,m2):
    d2 = 0.
    for i in range(3):
        for j in range(3):
            d2 += (m1[i][j]-m2[i][j])**2
    return d2

def iatan2(y,x):
    """One coordinate must be zero"""
    if x == 0:
        return 90 if y > 0 else -90
    else:
        return 0 if x > 0 else 180

def icos(angleDegrees):
    """Calculate a cosine of an angle that must be a multiple of 90 degrees"""
    return ICOS[(angleDegrees % 360) // 90]

def isin(angleDegrees):
    """Calculate a sine of an angle that must be a multiple of 90 degrees"""
    return ISIN[(angleDegrees % 360) // 90]

def matrixMultiply(a,b):
    c = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        for j in range(3):
            c[i][j] = a[i][0]*b[0][j] + a[i][1]*b[1][j] + a[i][2]*b[2][j]
    return c

def yawMatrix(angleDegrees):
    if isinstance(angleDegrees, Integral) and angleDegrees % 90 == 0:
        return [[icos(angleDegrees), 0, -isin(angleDegrees)],
                [0,          1, 0],
                [isin(angleDegrees), 0, icos(angleDegrees)]]
    else:
        theta = angleDegrees * TO_RADIANS
        return [[cos(theta), 0., -sin(theta)],
                [0.,         1., 0.],
                [sin(theta), 0., cos(theta)]]

def rollMatrix(angleDegrees):
    if isinstance(angleDegrees, Integral) and angleDegrees % 90 == 0:
        return [[icos(angleDegrees), -isin(angleDegrees), 0],
                [isin(angleDegrees), icos(angleDegrees),0],
                [0,          0,          1]]
    else:
        theta = angleDegrees * TO_RADIANS
        return [[cos(theta), -sin(theta), 0.],
                [sin(theta), cos(theta),0.],
                [0.,          0.,          1.]]

def pitchMatrix(angleDegrees):
    if isinstance(angleDegrees, Integral) and angleDegrees % 90 == 0:
        return [[1,          0,          0],
                [0, icos(angleDegrees),isin(angleDegrees)],
                [0, -isin(angleDegrees),icos(angleDegrees)]]
    else:
        theta = angleDegrees * TO_RADIANS
        return [[1.,          0.,          0.],
                [0., cos(theta),sin(theta)],
                [0., -sin(theta),cos(theta)]]

def get2DTriangle(a,b,c):
    """get the points of the 2D triangle"""
    minX = {}
    maxX = {}

    for line in (traverse2D(a,b), traverse2D(b,c), traverse2D(a,c)):
        for p in line:
            minX0 = minX.get(p[1])
            if minX0 == None:
                minX[p[1]] = p[0]
                maxX[p[1]] = p[0]
                yield(p)
            elif p[0] < minX0:
                for x in range(p[0],minX0):
                    yield(x,p[1])
                minX[p[1]] = p[0]
            else:
                maxX0 = maxX[p[1]]
                if maxX0 < p[0]:
                    for x in range(maxX0,p[0]):
                        yield(x,p[1])
                    maxX[p[1]] = p[0]

def getFace(vertices):
    if len(vertices) < 1:
        raise StopIteration
    if len(vertices) <= 2:
        for p in traverse(V3(vertices[0]), V3(vertices[1])):
            yield p
    v0 = V3(vertices[0])
    for i in range(2,len(vertices)):
        for p in traverse(V3(vertices[i-1]), V3(vertices[i])):
            for q in traverse(p, v0):
                yield q

def getTriangle(p1, p2, p3):
    """
    Note that this will return many duplicate poitns
    """
    p1,p2,p3 = V3(p1),V3(p2),V3(p3)

    for u in traverse(p2,p3):
        for w in traverse(p1,u):
             yield w

def frac(x):
    return x - floor(x)

def traverse2D(a,b):
    """
    equation of line: a + t(b-a), t from 0 to 1
    Based on Amantides and Woo's ray traversal algorithm with some help from
    http://stackoverflow.com/questions/12367071/how-do-i-initialize-the-t-variables-in-a-fast-voxel-traversal-algorithm-for-ray
    """

    inf = float("inf")

    if b[0] == a[0]:
        if b[1] == a[1]:
            yield (int(floor(a[0])),int(floor(a[1])))
            return
        tMaxX = inf
        tDeltaX = 0
    else:
        tDeltaX = 1./abs(b[0]-a[0])
        tMaxX = tDeltaX * (1. - frac(a[0]))

    if b[1] == a[1]:
        tMaxY = inf
        tDeltaY = 0
    else:
        tDeltaY = 1./abs(b[1]-a[1])
        tMaxY = tDeltaY * (1. - frac(a[1]))

    endX = int(floor(b[0]))
    endY = int(floor(b[1]))
    x = int(floor(a[0]))
    y = int(floor(a[1]))
    if x <= endX:
        stepX = 1
    else:
        stepX = -1
    if y <= endY:
        stepY = 1
    else:
        stepY = -1

    yield (x,y)
    if x == endX:
        if y == endY:
            return
        tMaxX = inf
    if y == endY:
        tMaxY = inf

    while True:
        if tMaxX < tMaxY:
            x += stepX
            yield (x,y)
            if x == endX:
                tMaxX = inf
            else:
                tMaxX += tDeltaX
        else:
            y += stepY
            yield (x,y)
            if y == endY:
                tMaxY = inf
            else:
                tMaxY += tDeltaY

        if tMaxX == inf and tMaxY == inf:
            return

def traverse(a,b):
    """
    equation of line: a + t(b-a), t from 0 to 1
    Based on Amantides and Woo's ray traversal algorithm with some help from
    http://stackoverflow.com/questions/12367071/how-do-i-initialize-the-t-variables-in-a-fast-voxel-traversal-algorithm-for-ray
    """

    inf = float("inf")

    if b.x == a.x:
        if b.y == a.y and b.z == a.z:
            yield a.ifloor()
            return
        tMaxX = inf
        tDeltaX = 0
    else:
        tDeltaX = 1./abs(b.x-a.x)
        tMaxX = tDeltaX * (1. - frac(a.x))

    if b.y == a.y:
        tMaxY = inf
        tDeltaY = 0
    else:
        tDeltaY = 1./abs(b.y-a.y)
        tMaxY = tDeltaY * (1. - frac(a.y))

    if b.z == a.z:
        tMaxZ = inf
        tDeltaZ = 0
    else:
        tDeltaZ = 1./abs(b.z-a.z)
        tMaxZ = tDeltaZ * (1. - frac(a.z))

    end = b.ifloor()
    x = int(floor(a.x))
    y = int(floor(a.y))
    z = int(floor(a.z))
    if x <= end.x:
        stepX = 1
    else:
        stepX = -1
    if y <= end.y:
        stepY = 1
    else:
        stepY = -1
    if z <= end.z:
        stepZ = 1
    else:
        stepZ = -1

    yield V3(x,y,z)

    if x == end.x:
        if y == end.y and z == end.z:
            return
        tMaxX = inf
    if y == end.y:
        tMaxY = inf
    if z == end.z:
        tMaxZ = inf

    while True:
        if tMaxX < tMaxY:
            if tMaxX < tMaxZ:
                x += stepX
                yield V3(x,y,z)
                if x == end.x:
                    tMaxX = inf
                else:
                    tMaxX += tDeltaX
            else:
                z += stepZ
                yield V3(x,y,z)
                if z == end.z:
                    tMaxZ = inf
                else:
                    tMaxZ += tDeltaZ
        else:
            if tMaxY < tMaxZ:
                y += stepY
                yield V3(x,y,z)
                if y == end.y:
                    tMaxY = inf
                else:
                    tMaxY += tDeltaY
            else:
                z += stepZ
                yield V3(x,y,z)
                if z == end.z:
                    tMaxZ = inf
                else:
                    tMaxZ += tDeltaZ

        if tMaxX == inf and tMaxY == inf and tMaxZ == inf:
            return

# Brasenham's algorithm
def getLine(x1, y1, z1, x2, y2, z2):
    line = []
    x1 = int(floor(x1))
    y1 = int(floor(y1))
    z1 = int(floor(z1))
    x2 = int(floor(x2))
    y2 = int(floor(y2))
    z2 = int(floor(z2))
    point = [x1,y1,z1]
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    x_inc = -1 if dx < 0 else 1
    l = abs(dx)
    y_inc = -1 if dy < 0 else 1
    m = abs(dy)
    z_inc = -1 if dz < 0 else 1
    n = abs(dz)
    dx2 = l << 1
    dy2 = m << 1
    dz2 = n << 1

    if l >= m and l >= n:
        err_1 = dy2 - l
        err_2 = dz2 - l
        for i in range(0,l-1):
            line.append(V3(point[0],point[1],point[2]))
            if err_1 > 0:
                point[1] += y_inc
                err_1 -= dx2
            if err_2 > 0:
                point[2] += z_inc
                err_2 -= dx2
            err_1 += dy2
            err_2 += dz2
            point[0] += x_inc
    elif m >= l and m >= n:
        err_1 = dx2 - m;
        err_2 = dz2 - m;
        for i in range(0,m-1):
            line.append(V3(point[0],point[1],point[2]))
            if err_1 > 0:
                point[0] += x_inc
                err_1 -= dy2
            if err_2 > 0:
                point[2] += z_inc
                err_2 -= dy2
            err_1 += dx2
            err_2 += dz2
            point[1] += y_inc
    else:
        err_1 = dy2 - n;
        err_2 = dx2 - n;
        for i in range(0, n-1):
            line.append(V3(point[0],point[1],point[2]))
            if err_1 > 0:
                point[1] += y_inc
                err_1 -= dz2
            if err_2 > 0:
                point[0] += x_inc
                err_2 -= dz2
            err_1 += dy2
            err_2 += dx2
            point[2] += z_inc
    line.append(V3(point[0],point[1],point[2]))
    if point[0] != x2 or point[1] != y2 or point[2] != z2:
        line.append(V3(x2,y2,z2))
    return line


class Drawing:
    TO_RADIANS = pi / 180.
    TO_DEGREES = 180. / pi

    def __init__(self,mc=None):
        if mc is not None:
             self.mc = mc
        else:
             self.mc = minecraft.Minecraft()
        self.width = 1
        self.nib = [(0,0,0)]

    def penwidth(self,w):
        self.width = int(w)
        if self.width == 0:
            self.nib = []
        elif self.width == 1:
            self.nib = [(0,0,0)]
        elif self.width == 2:
            self.nib = []
            for x in range(-1,1):
                for y in range(0,2):
                    for z in range(-1,1):
                        self.nib.append((x,y,z))
        else:
            self.nib = []
            r2 = self.width * self.width / 4.
            for x in range(-self.width//2 - 1,self.width//2 + 1):
                for y in range(-self.width//2 - 1, self.width//2 + 1):
                    for z in range(-self.width//2 -1, self.width//2 + 1):
                        if x*x + y*y + z*z <= r2:
                            self.nib.append((x,y,z))

    def point(self, x, y, z, block):
        for p in self.nib:
            self.mc.setBlock(x+p[0],y+p[1],z+p[2],block)

    def face(self, vertices, block):
        self.drawPoints(getFace(vertices), block)

    def line(self, x1,y1,z1, x2,y2,z2, block):
        self.drawPoints(getLine(x1,y1,z1, x2,y2,z2), block)

    def drawPoints(self, points, block):
        if self.width == 1:
            done = set()
            for p in points:
                if p not in done:
                    self.mc.setBlock(p, block)
                    done.add(p)
        else:
            done = set()
            for p in points:
                for point in self.nib:
                    x0 = p[0]+point[0]
                    y0 = p[1]+point[1]
                    z0 = p[2]+point[2]
                    if (x0,y0,z0) not in done:
                        self.mc.setBlock(x0,y0,z0,block)
                        done.add((x0,y0,z0))

if __name__ == "__main__":
    d = Drawing()
    pos = d.mc.player.getPos()
    d.face([(pos.x,pos.y,pos.z),(pos.x+20,pos.y+20,pos.z),(pos.x+20,pos.y+20,pos.z+20),
         (pos.x,pos.y,pos.z+20)], block.GLASS)
    n = 20
    for t in range(0,n):
        (x1,z1) = (100*cos(t*2*pi/n),80*sin(t*2*pi/n))
        for p in traverse(V3(pos.x,pos.y-1,pos.z),V3(pos.x+x1,pos.y-1,pos.z+z1)):
            d.mc.setBlock(p,block.OBSIDIAN)
    n = 40
    vertices = []
    for t in range(0,n):
        (x1,z1) = (100*cos(t*2*pi/n),80*sin(t*2*pi/n))
        vertices.append((pos.x+x1,pos.y,pos.z+z1))
    d.face(vertices, block.STAINED_GLASS_BLUE)
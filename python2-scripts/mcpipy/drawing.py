#
# Code under the MIT license by Alexander Pruss
#

import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.block import *
from mcpi.entity import *
from math import *
from numbers import Number
from operator import itemgetter

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

def get2DTriangle(*v):
    """get the points of the 2D triangle with vertices a,b,c"""
    """Coordinates assumed to be integral"""
    points = []
    # sort by y coordinate
    A,B,C = tuple(sorted(v, key=itemgetter(1)))
    # Use algorithm from http://www-users.mat.uni.torun.pl/~wrona/3d_tutor/tri_fillers.html
    dx1 = (B[0]-A[0])/float(B[1]-A[1]) if B[1]>A[1] else 0
    dx2 = (C[0]-A[0])/float(C[1]-A[1]) if C[1]>A[1] else 0
    dx3 = (C[0]-B[0])/float(C[1]-B[1]) if C[1]>B[1] else 0

    Sx=A[0]
    Ex=A[0]
    Sy=A[1]
    Ey=A[1]
    
    def horiz(sx,ex,y):
        a = int(floor(sx))
        b = int(floor(ex))
        for x in range(min(a,b),max(a,b)+1):
            points.append((x,y))

    if dx1 > dx2:
        while Sy <= B[1]:
            horiz(Sx,Ex,Sy)
            Sy += 1
            Ey += 1
            Sx += dx2
            Ex += dx1
        Ex=B[0]
        Ey=B[1]
        while Sy <= C[1]:
            horiz(Sx,Ex,Sy)
            Sy += 1
            Ey += 1
            Sx += dx2
            Ex += dx3
    else:
        while Sy < B[1]:
             horiz(Sx,Ex,Sy)
             Sy += 1
             Sx += dx1
             Ex += dx2
        Sx=B[0]
        Sy=B[1]
        while Sy <= C[1]:
             horiz(Sx,Ex,Sy)
             Sy += 1
             Ey += 1
             Sx += dx3
             Ex += dx2

    return points

def getTriangle(p1, p2, p3):
    v = (V3(p1),V3(p2),V3(p3))
    a = v[1]-v[0]
    b = v[2]-v[0]
    normal = a*b
    if normal.len2() < 0.000001:
       lMax = a.len2()
       sideMax = 0
       l2 = b.len2()
       if lMax < l2:
          lMax = l2
          sideMax = 1
       l3 = (v[2]-v[0]).len2()
       if lMax < l3:
          lMax = l3
          sideMax = 2
       if sideMax == 0:
          return getLine(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2])
       elif sideMax == 1:
          return getLine(p2[0],p2[1],p2[2],p3[0],p3[1],p3[2])
       else:
          return getLine(p1[0],p1[1],p1[2],p3[0],p3[1],p3[2])
    nMax = abs(normal[0])
    iMax = 0
    l = abs(normal[1])
    if l > nMax:
       iMax = 1
       nMax = l
    l = abs(normal[2])
    if l > nMax:
       iMax = 2
       #nMax = l

    def project(u):
       return (floor(u[0]) if iMax > 0 else floor(u[1]),
                  floor(u[1]) if iMax > 1 else floor(u[2]))

    flat = get2DTriangle((0,0),project(a),project(b))

    # the plane of the 3D triangle translated by -v[0] is defined by
    # { u : u.normal = 0 }

    if iMax == 0:
       unproject = lambda u : v[0]+( -(normal[1]*u[0]+normal[2]*u[1])/normal[0], u[0], u[1])
    elif iMax == 1:
       unproject = lambda u : v[0]+( u[0], -(normal[0]*u[0]+normal[2]*u[1])/normal[1], u[1])
    else:
       unproject = lambda u : v[0]+( u[0], u[1], -(normal[0]*u[0]-normal[1]*u[1])/normal[2])

    return [unproject(u).ifloor() for u in flat]

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
            line.append((point[0],point[1],point[2]))
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
            line.append((point[0],point[1],point[2]))
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
            line.append((point[0],point[1],point[2]))
            if err_1 > 0:
                point[1] += y_inc
                err_1 -= dz2
            if err_2 > 0:
                point[0] += x_inc
                err_2 -= dz2
            err_1 += dy2
            err_2 += dx2
            point[2] += z_inc
    line.append((point[0],point[1],point[2]))
    if point[0] != x2 or point[1] != y2 or point[2] != z2:
        line.append((x2,y2,z2))
    return line


class Drawing:
    TO_RADIANS = pi / 180.
    TO_DEGREES = 180. / pi

    def __init__(self,mc=None):
        if mc:
             self.mc = mc
        else:
             self.mc = minecraft.Minecraft()
        self.width = 1
        self.nib = [(0,0,0)]
        self.fan = None

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

    def face(self, points, block):
        if len(points) == 0:
            return

        self.fan = points[0]
        self.done = {}
        prev = points[len(points)-1]

        for p in points:
            self.line(prev[0], prev[1], prev[2], p[0], p[1], p[2], block)
            prev = p

        self.fan = False

    def line(self, x1,y1,z1, x2,y2,z2, block):
        def drawPoint(p):
            if self.width == 1 and not self.fan:
                self.mc.setBlock(p[0],p[1],p[2],block)
            else:
                for point in self.nib:
                    x0 = p[0]+point[0]
                    y0 = p[1]+point[1]
                    z0 = p[2]+point[2]
                    if not (x0,y0,z0) in self.done:
                        self.mc.setBlock(x0,y0,z0,block)
                        self.done[x0,y0,z0] = True

        # dictinary to avoid duplicate drawing
        if not self.fan:
            self.done = {}

        if self.fan:
            for a in getTriangle(self.fan, (x1,y1,z1), (x2,y2,z2)):
                drawPoint(a)
        else:
            for a in line:
                drawPoint(a)


if __name__ == "__main__":
    d = Drawing()
    pos = d.mc.player.getPos()
    d.face([(pos.x,pos.y,pos.z),(pos.x+10,pos.y+10,pos.z),(pos.x+10,pos.y+10,pos.z+10),
         (pos.x,pos.y,pos.z+10)], GLASS)

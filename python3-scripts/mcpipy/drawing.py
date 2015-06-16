#
# MIT-licensed code by Alexander Pruss
#

import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.block import *
from mcpi.entity import *
import time
from math import *

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

        line = Drawing.getLine(x1,y1,z1, x2,y2,z2)

        if self.fan:
            def fan(base,line):
                for a in line:
                    fillLine = Drawing.getLine(a[0],a[1],a[2],
                                              base[0],base[1],base[2])
                    for b in fillLine:
                        drawPoint(b)

            # draw the main fan
            fan(self.fan,line)
            # now fill in some possible gaps
            # This is faster than it seems due to the self.done dictionary
            fan((x1,y1,z1),Drawing.getLine(self.fan[0],self.fan[1],self.fan[2],
                                          x2,y2,z2))
            fan((x2,y2,z2),Drawing.getLine(self.fan[0],self.fan[1],self.fan[2],
                                          x1,y1,z1))
        else:
            for a in line:
                drawPoint(a)

    @staticmethod
    def getLine(x1, y1, z1, x2, y2, z2):
        line = []
        x1 = int(x1)
        y1 = int(y1)
        z1 = int(z1)
        x2 = int(x2)
        y2 = int(y2)
        z2 = int(z2)
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
        return line


if __name__ == "__main__":
    d = Drawing()
    pos = d.mc.player.getPos()    
    d.face([(pos.x,pos.y,pos.z),(pos.x+10,pos.y+10,pos.z),(pos.x+10,pos.y+10,pos.z+10),(pos.x,pos.y,pos.z+10)], GLASS)

import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.block import *
from mcpi.entity import *
import copy
import time
from math import *
import server

class Turtle:
    TO_RADIANS = pi / 180.
    TO_DEGREES = 180. / pi
    QUICK_SAVE = ( 'block', 'width', 'pen', 'matrix', 'nib', 'fan' )

    def __init__(self,mc=None):
        if mc:
             self.mc = mc
        else:
             self.mc = minecraft.Minecraft.create(server.address)
        self.block = BEDROCK
        self.width = 1
        self.pen = True
        self.directionIn()
        self.positionIn()
        self.delayTime = 0.05
        self.nib = [(0,0,0)]
        self.turtleType = PLAYER
        self.playerId = self.mc.getPlayerId()
        self.turtleId = self.playerId
        self.fan = None
        self.stack = []

    def save(self):
        dict = {}
        for attribute in Turtle.QUICK_SAVE:
            dict[attribute] = copy.deepcopy(getattr(self, attribute))
        dict['position'] = (self.position.x, self.position.y, self.position.z)
        return dict

    def restore(self, dict):
        for attribute in Turtle.QUICK_SAVE:
            setattr(self, attribute, dict[attribute])
        p = dict['position']
        self.position = minecraft.Vec3(p[0], p[1], p[2])
        self.positionOut()
        self.directionOut()

    def push(self):
        """Save current drawing state to stack"""
        self.stack.append(self.save())

    def pop(self):
        """Restore current drawing state from stack"""
        self.restore(self.stack.pop())

    def turtle(self,turtleType):
        """Set turtle type. Use PLAYER for moving the player as the turtle and None for none"""
        if self.turtleType == turtleType:
            return
        if self.turtleType and self.turtleType != PLAYER:
            self.mc.removeEntity(self.turtleId)
        self.turtleType = turtleType
        if turtleType == PLAYER:
            self.turtleId = self.playerId
        elif turtleType:
            self.turtleId = self.mc.spawnEntity(turtleType,
                                                self.position.x,self.position.y,self.position.z,
                                                "{NoAI:1}")
        self.positionOut()
        self.directionOut()

    def follow(self): # deprecated
        self.turtle(PLAYER)
        
    def nofollow(self): # deprecated
        if self.turtleType == PLAYER:
            self.turtle(None)

    def penwidth(self,w):
        """Set pen stroke width (width:int)"""
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
        
    def goto(self,x,y,z):
        """Teleport turtle to location (x:int, y:int, z:int)"""
        self.position.x = x
        self.position.y = y
        self.position.z = z
        self.positionOut()
        self.delay()

    def verticalangle(self,angle):
        """Vertical angle of turtle (angle:float): 0=horizontal, 90=directly up, -90=directly down"""
        angles = self.getMinecraftAngles();
        self.matrix = Turtle.matrixMultiply(Turtle.yawMatrix(angles[0]), Turtle.pitchMatrix(angle))
        self.directionOut()

    def angle(self,angle):
        """Compass angle of turtle (angle:float): 0=south, 90=west, 180=north, 270=west"""
        angles = self.getMinecraftAngles()
        self.matrix = Turtle.matrixMultiply(Turtle.yawMatrix(angle), Turtle.pitchMatrix(angles[1]))
        self.directionOut()
        
    def penup(self):
        """Move without drawing"""
        self.pen = False

    def pendown(self):
        """Move with drawing"""
        self.pen = True

    def penblock(self, block):
        """Set material of pen block"""
        self.block = block

    def positionIn(self):
        self.position = self.mc.player.getPos()

    def positionOut(self):
        if self.turtleType:
            self.mc.entity.setPos(self.turtleId,self.position)

    def delay(self):
        if self.delayTime > 0:
            time.sleep(self.delayTime)

    def directionIn(self):
        rotation = self.mc.player.getRotation()
        pitch = 0 #self.mc.player.getPitch()
        self.matrix = Turtle.matrixMultiply(Turtle.yawMatrix(rotation), Turtle.pitchMatrix(-pitch))

    @staticmethod
    def matrixMultiply(a,b):
        c = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(3):
            for j in range(3):
                c[i][j] = a[i][0]*b[0][j] + a[i][1]*b[1][j] + a[i][2]*b[2][j]
        return c

    @staticmethod
    def yawMatrix(angleDegrees):
        theta = angleDegrees * Turtle.TO_RADIANS
        return [[cos(theta), 0, -sin(theta)],
                [0,          1, 0],
                [sin(theta), 0, cos(theta)]]

    @staticmethod
    def rollMatrix(angleDegrees):
        theta = angleDegrees * Turtle.TO_RADIANS
        return [[cos(theta), -sin(theta), 0.],
                [sin(theta), cos(theta),0.],
                [0.,          0.,          1.]]

    @staticmethod
    def pitchMatrix(angleDegrees):
        theta = angleDegrees * Turtle.TO_RADIANS
        return [[1,          0,          0],
                [0, cos(theta),sin(theta)],
                [0, -sin(theta),cos(theta)]]

    def yaw(self,angleDegrees):
        self.matrix = Turtle.matrixMultiply(self.matrix, Turtle.yawMatrix(angleDegrees))
        self.directionOut()
        self.delay()

    def roll(self,angleDegrees):
        self.matrix = Turtle.matrixMultiply(self.matrix, Turtle.rollMatrix(angleDegrees))
        self.directionOut()
        self.delay()

    def pitch(self,angleDegrees):
        self.matrix = Turtle.matrixMultiply(self.matrix, Turtle.pitchMatrix(angleDegrees))
        self.directionOut()
        self.delay()

    def getHeading(self):
        return [self.matrix[0][2],self.matrix[1][2],self.matrix[2][2]]

    def getMinecraftAngles(self):
        heading = self.getHeading()
        xz = sqrt(heading[0]*heading[0] + heading[2]*heading[2])
        if xz >= 1e-9:
            rotation = atan2(-heading[0], heading[2]) * Turtle.TO_DEGREES
        else:
            rotation = 0
        pitch = atan2(-heading[1], xz) * Turtle.TO_DEGREES
        return [rotation,pitch]

    def directionOut(self):
        if self.turtleType:
            heading = self.getHeading()
            xz = sqrt(heading[0]*heading[0] + heading[2]*heading[2])
            pitch = atan2(-heading[1], xz) * Turtle.TO_DEGREES
            self.mc.entity.setPitch(self.turtleId,pitch)
            if xz >= 1e-9:
                rotation = atan2(-heading[0], heading[2]) * Turtle.TO_DEGREES
                self.mc.entity.setRotation(self.turtleId,rotation)

    def pendelay(self, t):
        """Set pen delay in seconds (t: float)"""
        self.delayTime = t

    def left(self, angle):
        """Turn counterclockwise relative to compass heading"""
        self.right(-angle)

    def right(self, angle):
        """Turn clockwise relative to compass heading"""
        self.matrix = Turtle.matrixMultiply(Turtle.yawMatrix(angle), self.matrix)
        self.directionOut()
        self.delay()

    def up(self, angle):
        """Turn upwards (increase pitch)"""
        self.pitch(angle)

    def down(self, angle):
        """Turn downwards (decrease pitch)"""
        self.up(-angle)

    def go(self, distance):
        """Advance turtle, drawing as needed (distance: float)"""
#        pitch = self.pitch * pi/180.
#        rot = self.rotation * pi/180.
        # at pitch=0: rot=0 -> [0,0,1], rot=90 -> [-1,0,0]
#        dx = cos(-pitch) * sin(-rot)
#        dy = sin(-pitch)
#        dz = cos(-pitch) * cos(-rot)
        [dx,dy,dz] = self.getHeading()
        newX = self.position.x + dx * distance
        newY = self.position.y + dy * distance
        newZ = self.position.z + dz * distance
        self.drawLine(self.position.x, self.position.y, self.position.z,
                        newX, newY, newZ)
        self.position.x = newX
        self.position.y = newY
        self.position.z = newZ
        self.positionOut()
        self.delay()

    def back(self, distance):
        """Move turtle backwards, drawing as needed (distance: float), and keeping heading unchanged"""
#        pitch = self.pitch * pi/180.
#        rot = self.rotation * pi/180.
#        dx = - cos(-pitch) * sin(-rot)
#        dy = - sin(-pitch)
#        dz = - cos(-pitch) * cos(-rot)
        [dx,dy,dz] = self.getHeading()
        newX = self.position.x - dx * distance
        newY = self.position.y - dy * distance
        newZ = self.position.z - dz * distance
        self.drawLine(self.position.x, self.position.y, self.position.z,
                        newX, newY, newZ)
        self.position.x = newX
        self.position.y = newY
        self.position.z = newZ
        self.positionOut()
        self.delay()

    def startface(self):
        """Start drawing a convex polygon"""
        self.fan = (self.position.x,self.position.y,self.position.z)

    def endface(self):
        """Finish polygon"""
        self.fan = None

    def drawLine(self, x1,y1,z1, x2,y2,z2):
        def drawPoint(p, fast=False):
            if self.pen:
                if self.width == 1 and not self.fan:
                    self.mc.setBlock(p[0],p[1],p[2],self.block)
                else:
                    for point in self.nib:
                        x0 = p[0]+point[0]
                        y0 = p[1]+point[1]
                        z0 = p[2]+point[2]
                        if not (x0,y0,z0) in done:
                            self.mc.setBlock(x0,y0,z0,self.block)
                            done[x0,y0,z0] = True

            if not fast and self.delayTime > 0:
                self.position.x = p[0]
                self.position.y = p[1]
                self.position.z = p[2]
                self.positionOut()
                self.delay()

        if not self.pen and self.delayTime == 0:
            return

        # dictinary to avoid duplicate drawing
        done = {}
        line = Turtle.getLine(x1,y1,z1, x2,y2,z2)

        if self.pen and self.fan:
            if self.delayTime > 0:
                for a in line:
                    drawPoint(a)

            def fan(base,line):
                for a in line:
                    fillLine = Turtle.getLine(a[0],a[1],a[2],
                                              base[0],base[1],base[2])
                    for b in fillLine:
                        drawPoint(b, True)

            # draw the main fan
            fan(self.fan,line)
            # now fill in some possible gaps
            # This is faster than it seems due to the done dictionary
            fan((x1,y1,z1),Turtle.getLine(self.fan[0],self.fan[1],self.fan[2],
                                          x2,y2,z2))
            fan((x2,y2,z2),Turtle.getLine(self.fan[0],self.fan[1],self.fan[2],
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
    t = Turtle()
    for i in range(7):
        t.back(80)
        t.right(180-180./7)
    t.turtle(None)

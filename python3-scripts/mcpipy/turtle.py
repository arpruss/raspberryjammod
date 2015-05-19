import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.block import *
from mcpi.entity import *
import time
from math import *
import server

class Turtle:
    TO_RADIANS = pi / 180.
    TO_DEGREES = 180. / pi

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
        self.nib = []
        self.turtleType = PLAYER
        self.playerId = self.mc.getPlayerId()
        self.turtleId = self.playerId

    def turtle(self,turtleType):
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
        self.nib = []
        self.width = int(w)
        if self.width >= 0 and self.width <= 2:
            return
        r2 = self.width * self.width / 4.
        for x in range(-self.width//2 - 1,self.width//2 + 1):
            for y in range(-self.width//2 - 1, self.width//2 + 1):
                for z in range(-self.width//2 -1, self.width//2 + 1):
                    if x*x + y*y + z*z <= r2:
                        self.nib.append(minecraft.Vec3(x,y,z))
        
    def goto(self,x,y,z):
        self.position.x = x
        self.position.y = y
        self.position.z = z
        self.positionOut()
        self.delay()

    def verticalangle(self,angle):
        angles = self.getMinecraftAngles();
        self.matrix = Turtle.matrixMultiply(Turtle.yawMatrix(angles[0]), Turtle.pitchMatrix(angle))
        self.directionOut()

    def angle(self,angle):
        angles = self.getMinecraftAngles()
        self.matrix = Turtle.matrixMultiply(Turtle.yawMatrix(angle), Turtle.pitchMatrix(angles[1]))
        self.directionOut()
        
    def penup(self):
        self.pen = False

    def pendown(self):
        self.pen = True

    def penblock(self, block):
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
            if xz >= 1e-9:
                rotation = atan2(-heading[0], heading[2]) * Turtle.TO_DEGREES
                self.mc.entity.setRotation(self.turtleId,rotation)
            pitch = atan2(-heading[1], xz) * Turtle.TO_DEGREES
            self.mc.entity.setPitch(self.turtleId,pitch)

    def pendelay(self, t):
        self.delayTime = t

    def left(self, angle):
        self.right(-angle)

    def right(self, angle):
        self.matrix = Turtle.matrixMultiply(Turtle.yawMatrix(angle), self.matrix)
        self.directionOut()
        self.delay()

    def up(self, angle):
        self.pitch(angle)

    def down(self, angle):
        self.up(-angle)

    def go(self, distance):
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

    def drawPoint(self, x, y, z):
        if self.pen and self.width > 0:
            if self.width == 1:
                self.mc.setBlock(x,y,z,self.block)
            elif self.width == 2:
                self.mc.setBlocks(x-1,y,z-1,x,y+1,z,self.block)
            else:
                for point in self.nib:
                    self.mc.setBlock(x+point.x,y+point.y,z+point.z,self.block)
        if self.delayTime > 0:
            self.position.x = x
            self.position.y = y
            self.position.z = z
            self.positionOut()
            self.delay()

    def drawLine(self, x1, y1, z1, x2, y2, z2):
        if not self.pen and self.delayTime == 0:
            return
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
                self.drawPoint(point[0], point[1], point[2])
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
                self.drawPoint(point[0], point[1], point[2])
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
                self.drawPoint(point[0], point[1], point[2])
                if err_1 > 0:
                    point[1] += y_inc
                    err_1 -= dz2
                if err_2 > 0:
                    point[0] += x_inc
                    err_2 -= dz2
                err_1 += dy2
                err_2 += dx2
                point[2] += z_inc
        self.drawPoint(point[0], point[1], point[2])
    

if __name__ == "__main__":
    t = Turtle()
    t.pendelay(0.05)
    t.penblock(GOLD_BLOCK)
    t.turtle(HORSE)
    for i in range(7):
        t.go(60)
        t.up(180-180/7)
    t.turtle(None)

#
# Code by Alexander Pruss and under the MIT license
#

import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.entity import *
import numbers
import copy
import time
from drawing import *
from operator import itemgetter
from math import *
import numbers

Block = block.Block

class Turtle:
    QUICK_SAVE = ( 'block', 'width', 'pen', 'matrix', 'nib', 'fan' )

    def __init__(self,mc=None):
        if mc:
             self.mc = mc
        else:
             self.mc = minecraft.Minecraft()
        self.block = block.GOLD_BLOCK
        self.width = 1
        self.pen = True
        self.directionIn()
        self.positionIn()
        self.delayTime = 0.05
        self.nib = [(0,0,0)]
        self.turtleType = PLAYER
        self.turtleId = None
        self.fan = None
        self.stack = []
        self.setEntityCommands()

    def setEntityCommands(self):
        if self.turtleId == None:
            self.setPos = self.mc.player.setPos
            self.setPitch = self.mc.player.setPitch
            self.setRotation = self.mc.player.setRotation
        else:
            self.setPos = lambda *pos: self.mc.entity.setPos(self.turtleId,*pos)
            self.setPitch = lambda angle: self.mc.entity.setPitch(self.turtleId,angle)
            self.setRotation = lambda angle: self.mc.entity.setRotation(self.turtleId,angle)

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
            self.turtleId = None
        elif turtleType:
            self.turtleId = self.mc.spawnEntity(turtleType,
                                                self.position.x,self.position.y,self.position.z,
                                                "{NoAI:1}")
        self.setEntityCommands()
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

    def rollangle(self,angle):
        """Set roll angle of turtle (angle:float/int) in degrees: 0=up vector points up"""
        angles = self.getMinecraftAngles()
        m0 = matrixMultiply(yawMatrix(angles[0]), pitchMatrix(angles[1]))
        self.matrix = matrixMultiply(m0, rollMatrix(angle))

    def angles(self,compass=0,vertical=0,roll=0):
        """Set roll angle of turtle (compass, vertical, roll) in degrees"""
        self.matrix = makeMatrix(compass,vertical,roll)

    def verticalangle(self,angle):
        """Vertical angle of turtle (angle:float/int) in degrees: 0=horizontal, 90=directly up, -90=directly down"""
        angles = self.getMinecraftAngles();
        self.matrix = matrixMultiply(yawMatrix(angles[0]), pitchMatrix(angle))
        self.directionOut()

    def angle(self,angle):
        """Compass angle of turtle (angle:float/int) in degrees: 0=south, 90=west, 180=north, 270=west"""
        angles = self.getMinecraftAngles()
        self.matrix = matrixMultiply(yawMatrix(angle), pitchMatrix(angles[1]))
        self.directionOut()

    def penup(self):
        """Move without drawing"""
        self.pen = False

    def pendown(self):
        """Move with drawing"""
        self.pen = True

    def penblock(self, b):
        """Set material of pen block"""
        self.block = b

    def positionIn(self):
        pos = self.mc.player.getPos()
        self.position = minecraft.Vec3(int(round(pos.x)),int(round(pos.y)),int(round(pos.z)))

    def positionOut(self):
        if self.turtleType:
            self.setPos(self.position)

    def delay(self):
        if self.delayTime > 0:
            time.sleep(self.delayTime)

    def directionIn(self):
        rotation = self.mc.player.getRotation()
        pitch = 0 #self.mc.player.getPitch()
        self.matrix = matrixMultiply(yawMatrix(rotation), pitchMatrix(-pitch))

    def yaw(self,angleDegrees):
        self.matrix = matrixMultiply(self.matrix, yawMatrix(angleDegrees))
        self.directionOut()
        self.delay()

    def roll(self,angleDegrees):
        self.matrix = matrixMultiply(self.matrix, rollMatrix(angleDegrees))
        self.directionOut()
        self.delay()

    def pitch(self,angleDegrees):
        self.matrix = matrixMultiply(self.matrix, pitchMatrix(angleDegrees))
        self.directionOut()
        self.delay()

    def getHeading(self):
        return [self.matrix[0][2],self.matrix[1][2],self.matrix[2][2]]

    def getMinecraftAngles(self):
        heading = self.getHeading()

        if isinstance(heading[0], numbers.Integral) and isinstance(heading[1], numbers.Integral) and isinstance(heading[2], numbers.Integral):
            # the only way all coordinates of the heading can be integers is if we are
            # grid aligned

            # no need for square roots; could also use absolute value
            xz = abs(heading[0]) + abs(heading[2])
            if xz != 0:
                rotation = iatan2(-heading[0], heading[2])
            else:
                rotation = 0
            pitch = iatan2(-heading[1], xz)
        else:        
            xz = sqrt(heading[0]*heading[0] + heading[2]*heading[2])
            if xz >= 1e-9:
                rotation = atan2(-heading[0], heading[2]) * TO_DEGREES
            else:
                rotation = 0.
            pitch = atan2(-heading[1], xz) * TO_DEGREES
        return [rotation,pitch]

    def directionOut(self):
        if self.turtleType:
            heading = self.getHeading()
            xz = sqrt(heading[0]*heading[0] + heading[2]*heading[2])
            pitch = atan2(-heading[1], xz) * TO_DEGREES
            self.setPitch(pitch)
            if xz >= 1e-9:
                rotation = atan2(-heading[0], heading[2]) * TO_DEGREES
                self.setRotation(rotation)

    def pendelay(self, t):
        """Set pen delay in seconds (t: float)"""
        self.delayTime = t

    def left(self, angle):
        """Turn counterclockwise relative to compass heading"""
        self.right(-angle)

    def right(self, angle):
        """Turn clockwise relative to compass heading"""
        self.matrix = matrixMultiply(yawMatrix(angle), self.matrix)
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

    def gridalign(self):
        """Align positions to grid"""
        self.position.x = int(round(self.position.x))
        self.position.y = int(round(self.position.y))
        self.position.z = int(round(self.position.z))

        if self.fan:
            self.fan = (int(round(self.fan[0])),int(round(self.fan[1])),int(round(self.fan[2])))

        bestDist = 2*9
        bestMatrix = makeMatrix(0,0,0)

        for compass in [0, 90, 180, 270]:
            for pitch in [0, 90, 180, 270]:
                for roll in [0, 90, 180, 270]:
                    m = makeMatrix(compass,pitch,roll)
                    dist = matrixDistanceSquared(self.matrix, m)
                    if dist < bestDist:
                        bestMatrix = m
                        bestDist = dist

        self.matrix = bestMatrix
        self.positionOut()
        self.directionOut()

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
                        if (x0,y0,z0) not in done:
                            self.mc.setBlock(x0,y0,z0,self.block)
                            done.add((x0,y0,z0))

            if not fast and self.delayTime > 0:
                self.position.x = p[0]
                self.position.y = p[1]
                self.position.z = p[2]
                self.positionOut()
                self.delay()

        if not self.pen and self.delayTime == 0:
            return

        # dictinary to avoid duplicate drawing
        done = set()

        if self.pen and self.fan:
            if self.delayTime > 0:
                for a in getLine(x1,y1,z1, x2,y2,z2):
                    drawPoint(a)

            triangle = getTriangle(self.fan, (x1,y1,z1), (x2,y2,z2))
            for a in triangle:
                drawPoint(a, True)
        else:
            for a in getLine(x1,y1,z1, x2,y2,z2):
                drawPoint(a)


if __name__ == "__main__":
    t = Turtle()
    for i in range(7):
        t.back(80)
        t.right(180-180./7)
    t.turtle(None)

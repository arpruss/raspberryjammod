#Minecraft Graphics Turtle
#Martin O'Hanlon
#www.stuffaboutcode.com

import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import math

#MinecraftDrawing class.  Useful functions for drawing objects.
class MinecraftDrawing:
    def __init__(self, mc):
        self.mc = mc

    # draw point
    def drawPoint3d(self, x, y, z, blockType, blockData=0):
        self.mc.setBlock(x,y,z,blockType,blockData)
        #print "x = " + str(x) + ", y = " + str(y) + ", z = " + str(z)

    # draws a face, when passed a collection of vertices which make up a polyhedron
    def drawFace(self, vertices, filled, blockType, blockData=0):
        # get the edges of the face
        edgesVertices = []
        # persist first vertex
        firstVertex = vertices[0]
        # get last vertex
        lastVertex = vertices[0]
        # loop through vertices and get edges
        for vertex in vertices[1:]:
            # got 2 vertices, get the points for the edge
            edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z)
            # persist the last vertex found    
            lastVertex = vertex
        # get edge between the last and first vertices
        edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, firstVertex.x, firstVertex.y, firstVertex.z)

        if (filled):
            #draw solid face
            # sort edges vertices
            def keyX( point ): return point.x
            def keyY( point ): return point.y
            def keyZ( point ): return point.z
            edgesVertices.sort( key=keyZ )
            edgesVertices.sort( key=keyY )
            edgesVertices.sort( key=keyX )

            #draw lines between the points on the edges
            # this algorithm isnt very efficient, but it does always fill the gap
            lastVertex = edgesVertices[0]
            for vertex in edgesVertices[1:]:
                # got 2 vertices, draw lines between them
                self.drawLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z, blockType, blockData)
                #print "x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z) + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z)
                # persist the last vertex found
                lastVertex = vertex

        else:
            #draw wireframe
            self.drawVertices(edgesVertices, blockType, blockData)
        
    # draw's all the points in a collection of vertices with a block
    def drawVertices(self, vertices, blockType, blockData=0):
        for vertex in vertices:
            self.drawPoint3d(vertex.x, vertex.y, vertex.z, blockType, blockData)

    # draw line
    def drawLine(self, x1, y1, z1, x2, y2, z2, blockType, blockData=0):
        self.drawVertices(self.getLine(x1, y1, z1, x2, y2, z2), blockType, blockData)

    # draw sphere
    def drawSphere(self, x1, y1, z1, radius, blockType, blockData=0):
        # create sphere
        for x in range(radius*-1,radius):
            for y in range(radius*-1, radius):
                for z in range(radius*-1,radius):
                    if x**2 + y**2 + z**2 < radius**2:
                        self.drawPoint3d(x1 + x, y1 + y, z1 + z, blockType, blockData)

    # draw a verticle circle
    def drawCircle(self, x0, y0, z, radius, blockType, blockData=0):
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        self.drawPoint3d(x0, y0 + radius, z, blockType, blockData)
        self.drawPoint3d(x0, y0 - radius, z, blockType, blockData)
        self.drawPoint3d(x0 + radius, y0, z, blockType, blockData)
        self.drawPoint3d(x0 - radius, y0, z, blockType, blockData)
     
        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x   
            self.drawPoint3d(x0 + x, y0 + y, z, blockType, blockData)
            self.drawPoint3d(x0 - x, y0 + y, z, blockType, blockData)
            self.drawPoint3d(x0 + x, y0 - y, z, blockType, blockData)
            self.drawPoint3d(x0 - x, y0 - y, z, blockType, blockData)
            self.drawPoint3d(x0 + y, y0 + x, z, blockType, blockData)
            self.drawPoint3d(x0 - y, y0 + x, z, blockType, blockData)
            self.drawPoint3d(x0 + y, y0 - x, z, blockType, blockData)
            self.drawPoint3d(x0 - y, y0 - x, z, blockType, blockData)

    # draw a horizontal circle
    def drawHorizontalCircle(self, x0, y, z0, radius, blockType, blockData=0):
        f = 1 - radius
        ddf_x = 1
        ddf_z = -2 * radius
        x = 0
        z = radius
        self.drawPoint3d(x0, y, z0 + radius, blockType, blockData)
        self.drawPoint3d(x0, y, z0 - radius, blockType, blockData)
        self.drawPoint3d(x0 + radius, y, z0, blockType, blockData)
        self.drawPoint3d(x0 - radius, y, z0, blockType, blockData)
     
        while x < z:
            if f >= 0:
                z -= 1
                ddf_z += 2
                f += ddf_z
            x += 1
            ddf_x += 2
            f += ddf_x   
            self.drawPoint3d(x0 + x, y, z0 + z, blockType, blockData)
            self.drawPoint3d(x0 - x, y, z0 + z, blockType, blockData)
            self.drawPoint3d(x0 + x, y, z0 - z, blockType, blockData)
            self.drawPoint3d(x0 - x, y, z0 - z, blockType, blockData)
            self.drawPoint3d(x0 + z, y, z0 + x, blockType, blockData)
            self.drawPoint3d(x0 - z, y, z0 + x, blockType, blockData)
            self.drawPoint3d(x0 + z, y, z0 - x, blockType, blockData)
            self.drawPoint3d(x0 - z, y, z0 - x, blockType, blockData)
    
    # returns points on a line
    # 3d implementation of bresenham line algorithm
    def getLine(self, x1, y1, z1, x2, y2, z2):

        # return maximum of 2 values
        def MAX(a,b):
            if a > b: return a
            else: return b

        # return step
        def ZSGN(a):
            if a < 0: return -1
            elif a > 0: return 1
            elif a == 0: return 0

        # list for vertices
        vertices = []

        # if the 2 points are the same, return single vertice
        if (x1 == x2 and y1 == y2 and z1 == z2):
            vertices.append(minecraft.Vec3(x1, y1, z1))
                            
        # else get all points in edge
        else:
        
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            ax = abs(dx) << 1
            ay = abs(dy) << 1
            az = abs(dz) << 1

            sx = ZSGN(dx)
            sy = ZSGN(dy)
            sz = ZSGN(dz)

            x = x1
            y = y1
            z = z1

            # x dominant
            if (ax >= MAX(ay, az)):
                yd = ay - (ax >> 1)
                zd = az - (ax >> 1)
                loop = True
                while(loop):
                    vertices.append(minecraft.Vec3(x, y, z))
                    if (x == x2):
                        loop = False
                    if (yd >= 0):
                        y += sy
                        yd -= ax
                    if (zd >= 0):
                        z += sz
                        zd -= ax
                    x += sx
                    yd += ay
                    zd += az
            # y dominant
            elif (ay >= MAX(ax, az)):
                xd = ax - (ay >> 1)
                zd = az - (ay >> 1)
                loop = True
                while(loop):
                    vertices.append(minecraft.Vec3(x, y, z))
                    if (y == y2):
                        loop=False
                    if (xd >= 0):
                        x += sx
                        xd -= ay
                    if (zd >= 0):
                        z += sz
                        zd -= ay
                    y += sy
                    xd += ax
                    zd += az
            # z dominant
            elif(az >= MAX(ax, ay)):
                xd = ax - (az >> 1)
                yd = ay - (az >> 1)
                loop = True
                while(loop):
                    vertices.append(minecraft.Vec3(x, y, z))
                    if (z == z2):
                        loop=False
                    if (xd >= 0):
                        x += sx
                        xd -= az
                    if (yd >= 0):
                        y += sy
                        yd -= az
                    z += sz
                    xd += ax
                    yd += ay
                    
        return vertices

class MinecraftTurtle:

    SPEEDTIMES = {0:0, 10:0.1, 9:0.2, 8:0.3, 7:0.4, 6:0.5, 5:0.6, 4:0.7, 3:0.8, 2:0.9, 1:1}
    
    def __init__(self, mc, position = minecraft.Vec3(0,0,0)):
        #set defaults
        self.mc = mc
        #start position
        self.startposition = position
        #set turtle position
        self.position = position
        #set turtle angles
        self.heading = 0
        self.verticalheading = 0
        #set pen down
        self._pendown = True
        #set pen block to black wool
        self._penblock = block.Block(block.WOOL.id, 15)
        #flying to true
        self.flying = True
        #set speed
        self.turtlespeed = 6
        #create turtle
        self.showturtle = True
        # create drawing object
        self.mcDrawing = MinecraftDrawing(self.mc)
        # set turtle block
        self.turtleblock = block.Block(block.DIAMOND_BLOCK.id)
        # draw turtle
        self._drawTurtle(int(self.position.x), int(self.position.y), int(self.position.y))
        
    def forward(self, distance):
        #get end of line
        #x,y,z = self._findTargetBlock(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading, distance)
        x,y,z = self._findPointOnSphere(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading, distance)
        #move turtle forward
        self._moveTurtle(x,y,z)

    def backward(self, distance):
        #move turtle backward
        #get end of line
        #x,y,z = self._findTargetBlock(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading - 180, distance)
        x,y,z = self._findPointOnSphere(self.position.x, self.position.y, self.position.z, self.heading, self.verticalheading - 180, distance)
        #move turtle forward
        self._moveTurtle(x,y,z)

    def _moveTurtle(self,x,y,z):
        #get blocks between current position and next
        targetX, targetY, targetZ = int(x), int(y), int(z)
        #if walking, set target Y to be height of world
        if self.flying == False: targetY = self.mc.getHeight(targetX, targetZ)
        currentX, currentY, currentZ = int(self.position.x), int(self.position.y), int(self.position.z)

        #clear the turtle
        if self.showturtle: self._clearTurtle(currentX, currentY, currentZ)
        
        #if speed is 0 and flying, just draw the line, else animate it
        if self.turtlespeed == 0 and self.flying:
            #draw the line
            if self._pendown: self.mcDrawing.drawLine(currentX, currentY - 1, currentZ, targetX, targetY - 1, targetZ, self._penblock.id, self._penblock.data)
        else:
            blocksBetween = self.mcDrawing.getLine(currentX, currentY, currentZ, targetX, targetY, targetZ)
            for blockBetween in blocksBetween:
                #print blockBetween
                #if walking update the y, to be the height of the world
                if self.flying == False: blockBetween.y = self.mc.getHeight(blockBetween.x, blockBetween.z)
                #draw the turtle
                if self.showturtle: self._drawTurtle(blockBetween.x, blockBetween.y, blockBetween.z)
                #draw the pen
                if self._pendown: self.mcDrawing.drawPoint3d(blockBetween.x, blockBetween.y - 1, blockBetween.z, self._penblock.id, self._penblock.data)
                #wait
                time.sleep(self.SPEEDTIMES[self.turtlespeed])
                #clear the turtle
                if self.showturtle: self._clearTurtle(blockBetween.x, blockBetween.y, blockBetween.z)
  
        #update turtle's position to be the target
        self.position.x, self.position.y, self.position.z = x,y,z
        #draw turtle
        if self.showturtle: self._drawTurtle(targetX, targetY, targetZ)
            
    def right(self, angle):
        #rotate turtle angle to the right
        self.heading = self.heading + angle
        if self.heading > 360:
            self.heading = self.heading - 360

    def left(self, angle):
        #rotate turtle angle to the left
        self.heading = self.heading - angle
        if self.heading < 0:
            self.heading = self.heading + 360

    def up(self, angle):
        #rotate turtle angle up
        self.verticalheading = self.verticalheading + angle
        if self.verticalheading > 360:
            self.verticalheading = self.verticalheading - 360
        #turn flying on
        if self.flying == False: self.flying = True

    def down(self, angle):
        #rotate turtle angle down
        self.verticalheading = self.verticalheading - angle
        if self.verticalheading < 0:
            self.verticalheading = self.verticalheading + 360
        #turn flying on
        if self.flying == False: self.flying = True

    def setx(self, x):
        self.setposition(x, self.position.y, self.position.z)

    def sety(self, y):
        self.setposition(self.position.x, y, self.position.z)

    def setz(self, z):
        self.setposition(self.position.x, self.position.y, z)

    def setposition(self, x, y, z):
        #clear the turtle
        if self.showturtle: self._clearTurtle(self.position.x, self.position.y, self.position.z)
        #update the position
        self.position.x = x
        self.position.y = y
        self.position.z = z
        #draw the turtle
        if self.showturtle: self._drawTurtle(self.position.x, self.position.y, self.position.z)

    def setheading(self, angle):
        self.heading = angle

    def setverticalheading(self, angle):
        self.verticalheading = angle
        #turn flying on
        if self.flying == False: self.flying = True

    def home(self):
        self.position.x = startposition.x
        self.position.y = startposition.y
        self.position.z = startposition.z

    def pendown(self):
        self._pendown = True

    def penup(self):
        self._pendown = False

    def isdown(self):
        return self.pendown

    def fly(self):
        self.flying = True

    def walk(self):
        self.flying = False
        self.verticalheading = 0

    def penblock(self, blockId, blockData = 0):
        self._penblock = block.Block(blockId, blockData)

    def speed(self, turtlespeed):
        self.turtlespeed = turtlespeed

    def _drawTurtle(self,x,y,z):
        #draw turtle
        self.mcDrawing.drawPoint3d(x, y, z, self.turtleblock.id, self.turtleblock.data)
        lastDrawnTurtle = minecraft.Vec3(x,y,z)

    def _clearTurtle(self,x,y,z):
        #clear turtle
        self.mcDrawing.drawPoint3d(x, y, z, block.AIR.id)

    def _findTargetBlock(self, turtleX, turtleY, turtleZ, heading, verticalheading, distance):
        x,y,z = self._findPointOnSphere(turtleX, turtleY, turtleZ, heading, verticalheading, distance)
        x = int(round(x,0))
        y = int(round(y,0))
        z = int(round(z,0))
        return x,y,z
    
    def _findPointOnSphere(self, cx, cy, cz, horizontalAngle, verticalAngle, radius):
        x = cx + (radius * (math.cos(math.radians(verticalAngle)) * math.cos(math.radians(horizontalAngle))))
        y = cy + (radius * (math.sin(math.radians(verticalAngle))))
        z = cz + (radius * (math.cos(math.radians(verticalAngle)) * math.sin(math.radians(horizontalAngle))))
        return x, y, z

    def _roundXYZ(x,y,z):
        return int(round(x,0)), int(round(y,0)), int(round(z,0))

    def _roundVec3(position):
        return minecraft.vec3(int(position.x), int(position.y), int(position.z))

if __name__ == "__main__":
    #connect to minecraft
    mc = minecraft.Minecraft.create()
    pos = mc.player.getTilePos()
    print pos
    #create minecraft turtle
    steve = MinecraftTurtle(mc,pos)
    
    #tests
    # draw a pentagon at different speeds
    steve.forward(5)
    steve.right(72)
    steve.speed(8)
    steve.forward(5)
    steve.right(72)
    steve.speed(10)
    steve.forward(5)
    steve.right(72)
    steve.speed(0)
    steve.forward(5)
    steve.right(72)
    steve.forward(5)

    # change pen
    steve.penblock(block.WOOL.id, 0)

    #backward
    steve.speed(6)
    steve.backward(10)

    # change pen
    steve.penblock(block.WOOL.id, 1)

    # pen up/down
    steve.penup()
    steve.forward(20)
    steve.pendown()

    # change pen
    steve.penblock(block.WOOL.id, 2)

    #up, down, left
    steve.up(30)
    steve.forward(5)
    steve.right(72)
    steve.forward(5)
    steve.down(30)
    steve.left(72)
    steve.forward(5)

    # change pen
    steve.penblock(block.WOOL.id, 3)

    # walking
    steve.walk()
    steve.forward(10)
    

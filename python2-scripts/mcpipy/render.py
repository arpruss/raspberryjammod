#www.stuffaboutcode.com
#Raspberry Pi, Minecraft - Create 3D Model from Obj file
# Version 2 - draws complete faces rather than wireframes and uses materials
"""
Copyright (c) Martin O'Hanlon and Alexander Pruss

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#import the minecraft.py module from the minecraft directory
import sys
import mcpi.minecraft as minecraft
#import minecraft block module
import mcpi.block as block
#import time, so delays can be used
import time
#import datetime, to get the time!
import datetime
from drawing import getFace, V3

import math
import re

def safeEval(x):
    if '__' in x:
        raise ValueError("Unsafe evaluation string")
    return eval(x)

def parseBlock(data):
    b = Block(0,0)
    tokens = re.split("[\\s,]+", data)
    haveBlock = False
    start = safeEval(tokens[0])
    if isinstance(start,Block):
        b = start
    else:
        b.id = int(start)
    if len(tokens)>1:
        b.data = int(safeEval(tokens[1]))
    return (b.id,b.data)

class ObjDescriptor(object):
    def __init__(self,dataFile):
         self.swapYZ = False
         self.size = 50
         self.default = (BEDROCK.id, 0)
         self.materials = {}
         with open(dataFile) as f:
             materialMode = False
             for line in f:
                 found = re.match('([^\\s]+) (.*)$', line.strip())
                 if found:
                     token = found.group(1).lower()
                     if materialMode:
                         self.materials[found.group(1)] = parseBlock(found.group(2))
                     elif token == "file":
                         if found.group(2).startswith('"') or found.group(2).startswith("'"):
                             self.objName = safeEval(found.group(2))
                         else:
                             self.objName = found.group(2)
                     elif token == "swapyz":
                         self.swapYZ = bool(safeEval(found.group(2).capitalize()))
                     elif token == "size":
                         self.size = safeEval(found.group(2))
                     elif token == "default":
                         self.default = parseBlock(found.group(2))
                 elif line.strip().lower() == "materials":
                     materialMode = True

# class to create 3d filled polygons
class MinecraftDrawing:
    def __init__(self, mc):
        self.mc = mc
        self.data = {}

    # draws a face, when passed a collection of vertices which make up a polygon
    def drawFace(self, drawDict, vertices, block):
        self.drawVertices(drawDict, getFace(vertices), block)

    # draws all the points in a collection of vertices with a block
    def drawVertices(self, drawDict, vertices, block):
        for vertex in vertices:
            if not vertex in drawDict or block != drawDict[vertex]:
                self.mc.setBlock(vertex, block)
                drawDict[vertex] = block

def load_obj(filename, swapyz, defaultBlock, materials) :
    V = [] #vertex
    T = [] #texcoords
    N = [] #normals
    F = [] #face indexies
    MF = [] #materials to faces

    if swapyz:
        fix = lambda list : V3(list[0], list[2], list[1])
    else:
        fix = lambda list : V3(list)

    currentMaterial = defaultBlock

    fh = open(filename)
    for line in fh :
        if line[0] == '#' : continue
        line = re.split('\s+', line.strip())
        if line[0] == 'v' :
            V.append(V3(fix([float(x) for x in line[1:]])))
        elif line[0] == 'vt' : #tex-coord
            T.append(fix(line[1:]))
        elif line[0] == 'vn' : #normal vector
            N.append(fix(line[1:]))
        elif line[0] == 'f' : #face
            face = line[1:]
            for i in range(0, len(face)) :
                face[i] = face[i].split('/')
                # OBJ indexies are 1 based not 0 based hence the -1
                # convert indexies to integer
                for j in range(0, len(face[i])) :
                    if face[i][j] != "":
                        face[i][j] = int(face[i][j]) - 1
            #append the material currently in use to the face
            F.append(face)
            MF.append(currentMaterial)

        elif line[0] == 'usemtl': # material
            usemtl = line[1]
            if (usemtl in materials.keys()):
                currentMaterial = materials[usemtl]
            else:
                currentMaterial = defaultBlock
                print "Warning: Couldn't find '" + str(usemtl) + "' in materials using default"

    return V, T, N, F, MF

# main program
if __name__ == "__main__":

    print datetime.datetime.now()

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()

    #Create minecraft drawing class
    mcDrawing = MinecraftDrawing(mc)

    player = mc.player.getPos()

    WOOL_WHITE = (block.WOOL.id, 0)
    WOOL_ORANGE = (block.WOOL.id, 1)
    WOOL_MAGENTA = (block.WOOL.id, 2)
    WOOL_LIGHT_BLUE = (block.WOOL.id, 3)
    WOOL_YELLOW = (block.WOOL.id, 4)
    WOOL_LIME = (block.WOOL.id, 5)
    WOOL_PINK = (block.WOOL.id, 6)
    WOOL_GRAY = (block.WOOL.id, 7)
    WOOL_LIGHT_GRAY = (block.WOOL.id, 8)
    WOOL_CYAN = (block.WOOL.id, 9)
    WOOL_PURPLE = (block.WOOL.id, 10)
    WOOL_BLUE = (block.WOOL.id, 11)
    WOOL_BROWN = (block.WOOL.id, 12)
    WOOL_GREEN = (block.WOOL.id, 13)
    WOOL_RED = (block.WOOL.id, 14)
    WOOL_BLACK = (block.WOOL.id, 15)

    objects = {
        'ds9': ('model/ds9.obj', False, 200, (block.STONE.id, None),
                { "Yellow_self_illum": (block.GLOWSTONE_BLOCK.id, None),
                      "Lamps": (block.GLOWSTONE_BLOCK.id, None),
                      "Windows": (block.GLASS.id, None),
                      "Phaser": (124,0),
                      "Antenna": (173,0)
                    }),
        '1701d': ('model/1701d.obj', False, 200, (block.QUARTZ_BLOCK.id, None),
                { "Yellow_self_illum": (block.GLOWSTONE_BLOCK.id, None),
                      "Lamps": (block.SEA_LANTERN.id, None),
                      "Windows": (block.GLASS.id, None),
                      "Phaser": (block.REDSTONE_BLOCK.id,0),
                      "Antenna": (173,0)
                    }),
        'shuttle': ('model/shuttle.obj', True, 100, (block.WOOL.id, 0),
                    { "glass": (block.GLASS.id, None),
                     "bone": (block.WOOL.id, 0),
                     "fldkdkgrey": (block.WOOL.id, 7),
                     "redbrick": (block.WOOL.id, 14),
                     "black": (block.WOOL.id, 15),
                     "brass": (block.WOOL.id, 1),
                     "dkdkgrey": (block.WOOL.id, 7)
                        }),
        'skyscraper': ('model/skyscraper.obj', False, 100, (block.IRON_BLOCK.id, None), {}),
        'head': ('model/head.obj', False, 50, (block.GOLD_BLOCK.id, None), {}),
        'cessna': ('model/cessna.obj', False, 100, (block.IRON_BLOCK.id, None),
               {
                  "yellow": WOOL_YELLOW,
                  "red": WOOL_RED,
                  "white": WOOL_WHITE,
                  "black": WOOL_BLACK,
                  "glass": (block.GLASS.id, None),
                  "dkgrey": WOOL_GRAY,
               }),
        'ny': ('model/NY_LIL.obj', False, 200, (block.IRON_BLOCK.id, None),
               {
                   "Default_Material": (block.WOOL.id, 0),
                   "Color_A01": (block.WOOL.id, 14),
                   "0131_Silver": (block.IRON_BLOCK.id, None),
                   "0075_ForestGreen": (block.WOOL.id, 13),
                   "0137_Black": (block.WOOL.id, 15),
                   "Black": (block.WOOL.id, 15),
                   "Medium_Brown": (block.WOOL.id, 12),
                   "0056_Yellow": (block.WOOL.id, 4),
                   "0020_Red": (block.WOOL.id, 14),
                   "0102_RoyalBlue": (block.WOOL.id, 11),
                   "Color_E01": (block.WOOL.id, 4),
                   "Color_E02": (block.WOOL.id, 4),
                   "Color_B01": (block.WOOL.id, 1),
                   "Charcoal": (block.WOOL.id, 7),
                   "Material2": (block.WOOL.id, 0),
                   "Beige2": (block.SANDSTONE.id, None),
                   "DarkGoldenrod": (block.GOLD_BLOCK.id, None),
                   "Beige1": (block.SANDSTONE.id, None),
                   "jean_blue": (block.WOOL.id, 3),
                   "Gold1": (block.GOLD_BLOCK.id, None),
                   "WhiteSmoke": (block.WOOL.id, 8),
                   "0118_Thistle": (block.WOOL.id, 6),
                   "Color_D23": (block.WOOL.id, 7),
                   "Color_B23": (block.WOOL.id, 12),
                   "Color_009": (block.WOOL.id, 15),
                   "Color_D01": (block.WOOL.id, 1),
                   "Color_A06": (block.WOOL.id, 14),
                   "Color_D03": (block.WOOL.id, 4),
                   "0063_GreenYellow": (block.WOOL.id, 5)
                   }),
        'nottingham': ('model/City_Ground-Notts.obj', False, 200, (block.DIRT.id, None),
               {
                    "Default_Material": (block.STONE.id, None),
                    "Black": (block.WOOL.id, 15),
                   "Asphalt_Old": (block.WOOL.id, 7),
                   "GhostWhite": (block.WOOL.id, 0),
                   "Brick_Flemish_Bond": (block.BRICK_BLOCK.id, None),
                   "Concrete_Brushed": (block.STONE.id, None),
                   "Metal_Brushed": (block.IRON_BLOCK.id, None),
                   "Roofing_Metal_Standing_Seam_Blue": (block.WOOL.id, 8),
                   "White": (block.WOOL.id, 0),
                   "Metal_Brushed1": [(block.IRON_BLOCK.id, None),None],
                   "Rouge3141": (block.WOOL.id, 14),
                   "roof": (block.WOOL.id, 8),
                   "Metal_Aluminum_Anodized": (block.IRON_BLOCK.id, None),
                   "Translucent_Glass_Safety": (block.GLASS.id, None),
                   "Translucent_Glass_Safety1": (block.GLASS.id, None),
                   "Safety_Glass2": (block.GLASS.id, None),
                   "Red": (block.WOOL.id, 14),
                   "goal_net1": (block.WOOL.id, 0),
                   "Black": (block.WOOL.id, 15)}),
        'pi': ( 'model/RaspberryPi.obj', False, 150, (block.DIRT.id, None),
               {
                   "Default_Material": (block.WOOL.id, 0),
                   "Material1": (block.WOOL.id, 5),
                   "Goldenrod": (block.WOOL.id, 1),
                   "0136_Charcoal": (block.WOOL.id, 7),
                   "Gray61": (block.WOOL.id, 7),
                   "Charcoal": (block.WOOL.id, 7),
                   "Color_002": (block.WOOL.id, 8),
                   "Color_008": (block.WOOL.id, 4),
                   "Plastic_Green": (block.WOOL.id, 5),
                   "MB_Pastic_White": (block.WOOL.id, 0),
                   "IO_Shiny": (block.IRON_BLOCK.id, None),
                   "Material4": (block.GRASS.id, None),
                   "Gainsboro3": (block.WOOL.id, 5),
                   "CorrogateShiny1": (block.IRON_BLOCK.id, None),
                   "Gold": (block.GOLD_BLOCK.id, None),
                   "0129_WhiteSmoke": (block.WOOL.id, 0),
                   "Color_005": (block.WOOL.id, 0),
                   "USB_IO": (block.WOOL.id, 11),
                   "_Metal": (block.IRON_BLOCK.id, None),
                   "0132_LightGray": (block.WOOL.id, 8)})
                   }

    if sys.argv[0] in objects:
        object = objects[sys.argv]
    else:
        object = objects['pi']

    objectname = sys.argv[1] if len(sys.argv) >= 2 else 'pi'

    if not objectname in objects:
        print "Object not found"
        exit(3)

    filename,swapyz,size,defaultblock,materialdict = objects[objectname]
    if len(sys.argv) >= 3:
        size = float(sys.argv[2])
    vertices,textures,normals,faces,materials = load_obj(filename, swapyz, defaultblock, materialdict)

    min = [None, None, None]
    max = [None, None, None]

    for vertex in vertices:
        for i in range(3):
            if min[i] == None or vertex[i] < min[i]:
                min[i] = vertex[i]
            if max[i] == None or vertex[i] > max[i]:
                max[i] = vertex[i]

    maxsize = 0

    center = [(max[i] + min[i])/2 for i in range(3)]
    for i in range(3):
        if max[i]-min[i] > maxsize:
            maxsize = max[i]-min[i]

    scale = size / maxsize

    print "obj file loaded"

    translate = (player.x-scale*center[0], player.y-scale*min[1], player.z-scale*center[2])

    #Post a message to the minecraft chat window
    mc.postToChat("Hi, Minecraft 3d model maker, www.stuffaboutcode.com")

    # clear a suitably large area
    mc.setBlocks(int(translate[0]+scale*min[0]),
                 int(translate[1]+scale*min[1]),
                 int(translate[2]+scale*min[2]),
                 int(math.ceil(translate[0]+scale*max[0])),
                 int(math.ceil(translate[1]+scale*max[1])),
                 int(math.ceil(translate[2]+scale*max[2])),
                 block.AIR)

    scaledVertices = []
    for vertex in vertices:
        scaledVertices.append(vertex * scale + translate)

    faceCount = 0
    # loop through faces

    drawRecord = {}

    print len(faces),"faces"

    for face in faces:
        if faceCount % 10000 == 0:
             print faceCount

        faceVertices = [scaledVertices[vertex[0]] for vertex in face]

        # draw the face
        mcDrawing.drawFace(drawRecord, faceVertices, materials[faceCount])
        faceCount += 1

    mc.postToChat("Model complete, www.stuffaboutcode.com")

    print datetime.datetime.now()

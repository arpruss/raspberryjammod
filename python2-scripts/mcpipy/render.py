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
from mcpi.block import *
#import time, so delays can be used
import time
#import datetime, to get the time!
import datetime
from drawing import *

import math
import os
import re

def safeEval(p):
    if '__' in p:
        raise ValueError("Insecure entry")
    return eval(p)

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

class Mesh(object):
    def __init__(self,mc,infile):
         self.mc = mc
         self.swapYZ = False
         self.size = 100
         self.default = (BEDROCK.id, 0)
         self.materialBlockDict = {}
         self.baseVertices = []
         self.vertices = []
         self.textures = []
         self.normals = []
         self.faces = []
         self.materials = []
         self.materialNames = []
         self.corner1 = None
         self.corner2 = None

         base,ext = os.path.splitext(infile)
         if ext == '.obj':
             self.objName = infile
             self.dataFile = base + ".txt"
         with open(infile) as f:
             self.dataFile = infile
             self.objName = base + ".obj"
             dirname = os.path.dirname(infile)
             materialMode = False
             for line in f:
                 line = line.strip()
                 if line[0] == '#':
                     continue
                 found = re.match('([^\\s]+) (.*)$', line)
                 if found:
                     token = found.group(1).lower()
                     if materialMode:
                         self.materialBlockDict[found.group(1)] = parseBlock(found.group(2))
                     elif token == "file":
                         if found.group(2).startswith('"') or found.group(2).startswith("'"):
                             self.objName = dirname + "/" + safeEval(found.group(2))
                         else:
                             self.objName = dirname + "/" + found.group(2)
                     elif token == "swapyz":
                         self.swapYZ = bool(safeEval(found.group(2).capitalize()))
                     elif token == "size":
                         self.size = safeEval(found.group(2))
                     elif token == "default":
                         self.default = parseBlock(found.group(2))
                 elif line.strip().lower() == "materials":
                     materialMode = True

    def read(self):
        if self.swapYZ:
            fix = lambda list : V3(list[0], list[2], list[1])
        else:
            fix = lambda list : V3(list)

        warned = set()
        currentMaterialIndex = 0
        self.materialBlocks = [ self.default ]
        self.materialIndexDict = { "(unspecified)": 0 }

        with open(self.objName) as fh:
            for line in fh :
                line = line.strip()
                if len(line) == 0 or line[0] == '#' : continue
                line = re.split('\s+', line)
                if line[0] == 'v' :
                    self.baseVertices.append(V3(fix([float(x) for x in line[1:]])))
                #elif line[0] == 'vt' : #tex-coord
                #    self.textures.append(fix(line[1:]))
                #elif line[0] == 'vn' : #normal vector
                #    self.normals.append(fix(line[1:]))
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
                    self.faces.append(face)
                    self.materials.append(currentMaterialIndex)
                elif line[0] == 'usemtl': # material
                    name = line[1]
                    try:
                        currentMaterialIndex = self.materialIndexDict[name]
                    except KeyError:
                        currentMaterialIndex = len(self.materialBlocks)
                        self.materialIndexDict[name] = currentMaterialIndex
                        self.materialBlocks.append(self.materialBlockDict.get(name, self.default))
                        if name not in self.materialBlockDict and name not in warned:
                            self.mc.postToChat("Material "+name+" not defined")
                            warned.add(name)

    def scale(self, bottomCenter, matrix=None):
        minimum = [None, None, None]
        maximum = [None, None, None]

        self.vertices = []

        for v in self.baseVertices:
            if matrix is not None:
                vertex = applyMatrix(matrix,v)
            else:
                vertex = v
            self.vertices.append(v)
            for i in range(3):
                if minimum[i] == None or vertex[i] < minimum[i]:
                    minimum[i] = vertex[i]
                if maximum[i] == None or vertex[i] > maximum[i]:
                    maximum[i] = vertex[i]

        center = [(maximum[i] + minimum[i])/2 for i in range(3)]

        maxsize = max( ( maximum[i]-minimum[i] for i in range(3) ) )

        scale = self.size / maxsize
        translate = V3(bottomCenter.x-scale*center[0], bottomCenter.y-scale*minimum[1], bottomCenter.z-scale*center[2])

        for i in range(len(self.vertices)):
            self.vertices[i] = self.vertices[i] * scale + translate

        self.corner1 = (V3(minimum) * scale + translate).ifloor()
        self.corner2 = (V3(maximum) * scale + translate).iceil()

    def drawVertices(self, vertices, material):
        block = self.materialBlocks[material]
        for vertex in vertices:
            if material != self.drawRecord.get(vertex):
                self.mc.setBlock(vertex, block)
                self.drawRecord[vertex] = material

    def render(self):
        self.drawRecord = {}

        for faceCount,face in enumerate(self.faces):
            if faceCount % 4000 == 0:
                self.mc.postToChat("{0:.1f}%".format(100. * faceCount / len(self.faces)))

            faceVertices = [self.vertices[vertex[0]] for vertex in face]
            self.drawVertices(getFace(faceVertices), self.materials[faceCount])

def go(filename):
    mc = minecraft.Minecraft()

    mc.postToChat("Preparing")
    mesh = Mesh(mc, filename)
    mc.postToChat("Reading")
    mesh.read()
    mc.postToChat("Scaling")
    mesh.scale(mc.player.getPos())
    mc.postToChat("Clearing")
    mc.setBlocks(mesh.corner1,mesh.corner2,AIR)
    mc.postToChat("Rendering")
    mesh.render()
    mc.postToChat("Done!")

# main program
if __name__ == "__main__":
    go("models/" + sys.argv[1] + ".txt")

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

import sys
import urllib2
import mcpi.minecraft as minecraft
from copy import copy
from mcpi.block import *
import mcpi.settings as settings
#import time, so delays can be used
import time
#import datetime, to get the time!
import datetime
import gzip
from drawing import *

import math
import os
import re

def safeEval(p):
    if '__' in p:
        raise ValueError("Insecure entry")
    return eval(p)

def parseBlock(data,default):
    if '__' in data:
        raise ValueError("Insecure entry")
    b = Block(0,0)
    tokens = re.split("[\\s,]+", data)
    haveBlock = False
    start = eval(tokens[0])
    if isinstance(start,Block):
        b = copy(start)
    else:
        b.id = int(start)
    if len(tokens)>1:
        b.data = int(eval(tokens[1]))
    return Block(b.id,b.data)

class Mesh(object):
    UNSPECIFIED = None

    def __init__(self,mc,infile,rewrite=True):
         self.mc = mc
         self.rewrite = rewrite
         self.url = None
         self.urlgz = None
         self.swapYZ = False
         self.credits = None
         self.size = 100
         self.default = STONE
         self.materialBlockDict = {}
         self.materialOrderDict = {}
         self.baseVertices = []
         self.vertices = []
         self.textures = []
         self.normals = []
         self.faces = []
         self.materials = []
         self.materialNames = []
         self.haveMaterialArea = False
         self.corner1 = None
         self.corner2 = None
         self.endLineIndex = None

         base,ext = os.path.splitext(infile)
         if ext == '.obj':
             self.objName = infile
             self.controlFile = base + ".txt"
         else:
             self.objName = base + ".obj"
             self.controlFile = infile

         if os.path.isfile(self.controlFile):
             self.haveControlFile = True
             with open(self.controlFile) as f:
                 self.controlFileLines = f.readlines()
             self.objName = base + ".obj"
             dirname = os.path.dirname(self.controlFile)
             materialMode = False
             for i,line in enumerate(self.controlFileLines):
                 line = line.strip()
                 if len(line) == 0 or line[0] == '#':
                     continue
                 found = re.match('([^\\s]+) (.*)$', line)
                 if found:
                     token = found.group(1).lower()
                     if materialMode:
                         self.materialBlockDict[found.group(1)] = parseBlock(found.group(2),self.default)
                     elif token == "file":
                         if found.group(2).startswith('"') or found.group(2).startswith("'"):
                             self.objName = dirname + "/" + safeEval(found.group(2))
                         else:
                             self.objName = dirname + "/" + found.group(2)
                     elif token == "swapyz":
                         self.swapYZ = bool(safeEval(found.group(2).capitalize()))
                     elif token == "credits":
                         self.credits = found.group(2)
                     elif token == "url":
                         self.url = found.group(2)
                     elif token == "urlgz":
                         self.urlgz = found.group(2)
                     elif token == "size":
                         self.size = safeEval(found.group(2))
                     elif token == "default":
                         self.default = parseBlock(found.group(2),self.default)
                     elif token == "order":
                         args = re.split("[\\s,]+", found.group(2))
                         self.materialOrderDict[args[0]] = int(args[1])
                 elif line.strip().lower() == "materials":
                     materialMode = True
                     self.haveMaterialArea = True
                 elif line.strip().lower() == "end":
                     self.endLineIndex = i
                     break
             if self.endLineIndex is None:
                 self.endLineIndex = len(self.controlFileLines)
         elif rewrite:
             if not os.path.isfile(self.objName):
                 raise IOError("Cannot find mesh file")
             mc.postToChat("Creating a default control file")
             with open(self.controlFile,"w") as f:
                self.controlFileLines = []
                self.controlFileLines.append("file "+repr(self.objName)+"\n")
                self.controlFileLines.append("swapyz 0\n")
                self.controlFileLines.append("#credits [add?]\n")
                self.controlFileLines.append("#url [add?]\n")
                self.controlFileLines.append("#urlgz [add?]\n")
                self.controlFileLines.append("size "+str(self.size)+"\n")
                self.controlFileLines.append("default STONE\n")
                self.controlFileLines.append("#order material position\n")
                self.controlFileLines.append("materials\n")
                self.haveMaterialArea = True
                self.endLineIndex = len(self.controlFileLines)
                self.controlFileLines.append("end\n\n")
                self.controlFileLines.append("[Insert any detailed licensing information here]")
                for line in self.controlFileLines:
                    f.write(line)
         if settings.isPE:
             self.size /= 2

    def getFile(self, tryDownload=True):
        if os.path.isfile(self.objName):
            if self.objName.endswith(".gz"):
                return self.objName, gzip.open
            else:
                return self.objName, open
        if os.path.isfile(self.objName+".gz"):
            return self.objName+".gz", gzip.open
        if tryDownload and (self.url or self.urlgz):
            self.mc.postToChat("Downloading mesh")
            if self.urlgz:
                url = self.urlgz
                if not self.objName.endswith(".gz"):
                    outName = self.objName+".gz"
                else:
                    outName = self.objName
            else:
                url = self.url
                outName = self.objName
            content = urllib2.urlopen(url).read()
            with open(outName+".tempDownload","wb") as f:
                f.write(content)
            os.rename(outName+".tempDownload", outName)
            self.mc.postToChat("Downloaded")
            return self.getFile()
        else:
            raise IOError("File not found")

    def read(self, rewriteControlFile = None):
        if self.swapYZ:
            fix = lambda list : V3(list[0], list[2], list[1])
        else:
            fix = lambda list : V3(list)

        warned = set()
        currentMaterialIndex = 0
        self.materialBlocks = [ self.default ]
        self.materialOrders = [ 0 ]
        self.materialIndexDict = { Mesh.UNSPECIFIED: 0 }

        name,myopen = self.getFile()
        if self.credits:
            self.mc.postToChat("Credits: "+self.credits)
        with myopen(name) as fh:
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
                        # convert indexes to integer
                        for j in range(0, len(face[i])) :
                            if face[i][j] != "":
                                face[i][j] = int(face[i][j]) - 1
                    #prepend the material currently in use to the face
                    self.faces.append((currentMaterialIndex,face))
                elif line[0] == 'usemtl': # material
                    name = line[1]
                    try:
                        currentMaterialIndex = self.materialIndexDict[name]
                    except KeyError:
                        currentMaterialIndex = len(self.materialBlocks)
                        self.materialIndexDict[name] = currentMaterialIndex
                        self.materialOrders.append(self.materialOrderDict.get(name, 0))
                        self.materialBlocks.append(self.materialBlockDict.get(name, self.default))
                        if name not in self.materialBlockDict and name not in warned:
                            self.mc.postToChat("Material "+name+" not defined")
                            warned.add(name)

        if self.rewrite and warned and self.haveControlFile:
            try:
                self.mc.postToChat("Rewriting control file to include missing materials")
                with open(self.controlFile+".tempFile", "w") as f:
                    f.write(''.join(self.controlFileLines[:self.endLineIndex]))
                    if not self.haveMaterialArea:
                        f.write('\nmaterials\n')
                    for material in warned:
                        f.write(material+' default\n')
                    f.write(''.join(self.controlFileLines[self.endLineIndex:]))
                try:
                    os.unlink(self.controlFile+".bak")
                except:
                    pass
                try:
                    os.rename(self.controlFile, self.controlFile+".bak")
                except:
                    pass
                os.rename(self.controlFile+".tempFile", self.controlFile)
            except:
                self.mc.postToChat("Couldn't rewrite control file")
#        print 'self.materials',self.materials
#        print 'self.materialBlocks',self.materialBlocks
#        print 'self.materialIndexDict',self.materialIndexDict
#        print 'self.materialBlockDict',self.materialBlockDict
#        exit()

    def scale(self, bottomCenter, matrix=None):
        minimum = [None, None, None]
        maximum = [None, None, None]

        self.vertices = []

        for v in self.baseVertices:
            if matrix is not None:
                vertex = applyMatrix(matrix,v)
            else:
                vertex = v
            self.vertices.append(vertex)
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

        if len(self.materialOrderDict):
            faces = sorted(self.faces, key=lambda a : self.materialOrders[a[0]])
        else:
            faces = self.faces

        for faceCount,(material,face) in enumerate(faces):
            if faceCount % 4000 == 0:
                self.mc.postToChat("{0:.1f}%".format(100. * faceCount / len(self.faces)))

            faceVertices = [self.vertices[vertex[0]] for vertex in face]
            self.drawVertices(getFace(faceVertices), material)

def go(filename, args=[]):
    mc = minecraft.Minecraft()

    mc.postToChat("Preparing")
    mesh = Mesh(mc, filename)
    mc.postToChat("Reading")
    mesh.read()
    mc.postToChat("Scaling")

    opts = ""

    if args and re.match(args[0], "[a-zA-Z]"):
       opts = args.pop(0)

    if args:
       mesh.size = int(args.pop(0))

    matrix = None

    if args:
       yaw = float(args.pop(0))
       pitch = 0
       roll = 0
       if args:
          pitch = float(args.pop(0))
          if args:
             roll = float(args.pop(0))
       matrix = makeMatrix(yaw, pitch, roll)

    mesh.scale(mc.player.getPos(), matrix)
    mc.postToChat("Clearing")
    mc.setBlocks(mesh.corner1,mesh.corner2,AIR)
    mc.postToChat("Rendering")
    mesh.render()
    mc.postToChat("Done!")

# main program
if __name__ == "__main__":
    if len(sys.argv)<2:
        go("models/RaspberryPi.txt")
    else:
        go("models/" + sys.argv[1] + ".txt", sys.argv[2:])


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

from zipfile import ZipFile
import sys
import urllib2
import struct
from collections import OrderedDict
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

IDENTITY44 = ((1.,0.,0.,0.),(0.,1.,0.,0.),(0.,0.,1.,0.),(0.,0.,0.,1.))

def determinant44(m):
   inv00 = m[1][1] * m[2][2] * m[3][3] - m[1][1] * m[3][2] * m[2][3] - m[1][2] * m[2][1] * m[3][3] + m[1][2] * m[3][1] * m[2][3] + m[1][3] * m[2][1] * m[3][2] - m[1][3] * m[3][1] * m[2][2]
   inv01 = -m[0][1] * m[2][2] * m[3][3] + m[0][1] * m[3][2] * m[2][3] + m[0][2] * m[2][1] * m[3][3] - m[0][2] * m[3][1] * m[2][3] - m[0][3] * m[2][1] * m[3][2] + m[0][3] * m[3][1] * m[2][2]
   inv02 = m[0][1] * m[1][2] * m[3][3] - m[0][1] * m[3][2] * m[1][3] - m[0][2] * m[1][1] * m[3][3] + m[0][2] * m[3][1] * m[1][3] + m[0][3] * m[1][1] * m[3][2] - m[0][3] * m[3][1] * m[1][2]
   inv03 = -m[0][1] * m[1][2] * m[2][3] + m[0][1] * m[2][2] * m[1][3] + m[0][2] * m[1][1] * m[2][3] - m[0][2] * m[2][1] * m[1][3] - m[0][3] * m[1][1] * m[2][2] + m[0][3] * m[2][1] * m[1][2]
   return m[0][0] * inv00 + m[1][0] * inv01 + m[2][0] * inv02 + m[3][0] * inv03

def invertMatrix44(m):
   inv = [[0 for i in range(4)] for j in range(4)]

   inv[0][0] = m[1][1] * m[2][2] * m[3][3] - m[1][1] * m[3][2] * m[2][3] - m[1][2] * m[2][1] * m[3][3] + m[1][2] * m[3][1] * m[2][3] + m[1][3] * m[2][1] * m[3][2] - m[1][3] * m[3][1] * m[2][2]
   inv[0][1] = -m[0][1] * m[2][2] * m[3][3] + m[0][1] * m[3][2] * m[2][3] + m[0][2] * m[2][1] * m[3][3] - m[0][2] * m[3][1] * m[2][3] - m[0][3] * m[2][1] * m[3][2] + m[0][3] * m[3][1] * m[2][2]
   inv[0][2] = m[0][1] * m[1][2] * m[3][3] - m[0][1] * m[3][2] * m[1][3] - m[0][2] * m[1][1] * m[3][3] + m[0][2] * m[3][1] * m[1][3] + m[0][3] * m[1][1] * m[3][2] - m[0][3] * m[3][1] * m[1][2]
   inv[0][3] = -m[0][1] * m[1][2] * m[2][3] + m[0][1] * m[2][2] * m[1][3] + m[0][2] * m[1][1] * m[2][3] - m[0][2] * m[2][1] * m[1][3] - m[0][3] * m[1][1] * m[2][2] + m[0][3] * m[2][1] * m[1][2]

   inv[1][0] = -m[1][0] * m[2][2] * m[3][3] + m[1][0] * m[3][2] * m[2][3] + m[1][2] * m[2][0] * m[3][3] - m[1][2] * m[3][0] * m[2][3] - m[1][3] * m[2][0] * m[3][2] + m[1][3] * m[3][0] * m[2][2]
   inv[1][1] = m[0][0] * m[2][2] * m[3][3] - m[0][0] * m[3][2] * m[2][3] - m[0][2] * m[2][0] * m[3][3] + m[0][2] * m[3][0] * m[2][3] + m[0][3] * m[2][0] * m[3][2] - m[0][3] * m[3][0] * m[2][2]
   inv[1][2] = -m[0][0] * m[1][2] * m[3][3] + m[0][0] * m[3][2] * m[1][3] + m[0][2] * m[1][0] * m[3][3] - m[0][2] * m[3][0] * m[1][3] - m[0][3] * m[1][0] * m[3][2] + m[0][3] * m[3][0] * m[1][2]
   inv[1][3] = m[0][0] * m[1][2] * m[2][3] - m[0][0] * m[2][2] * m[1][3] - m[0][2] * m[1][0] * m[2][3] + m[0][2] * m[2][0] * m[1][3] + m[0][3] * m[1][0] * m[2][2] - m[0][3] * m[2][0] * m[1][2]

   inv[2][0] = m[1][0] * m[2][1] * m[3][3] - m[1][0] * m[3][1] * m[2][3] - m[1][1] * m[2][0] * m[3][3] + m[1][1] * m[3][0] * m[2][3] + m[1][3] * m[2][0] * m[3][1] - m[1][3] * m[3][0] * m[2][1]
   inv[2][1] = -m[0][0] * m[2][1] * m[3][3] + m[0][0] * m[3][1] * m[2][3] + m[0][1] * m[2][0] * m[3][3] - m[0][1] * m[3][0] * m[2][3] - m[0][3] * m[2][0] * m[3][1] + m[0][3] * m[3][0] * m[2][1]
   inv[2][2] = m[0][0] * m[1][1] * m[3][3] - m[0][0] * m[3][1] * m[1][3] - m[0][1] * m[1][0] * m[3][3] + m[0][1] * m[3][0] * m[1][3] + m[0][3] * m[1][0] * m[3][1] - m[0][3] * m[3][0] * m[1][1]
   inv[2][3] = -m[0][0] * m[1][1] * m[2][3] + m[0][0] * m[2][1] * m[1][3] + m[0][1] * m[1][0] * m[2][3] - m[0][1] * m[2][0] * m[1][3] - m[0][3] * m[1][0] * m[2][1] + m[0][3] * m[2][0] * m[1][1]

   inv[3][0] = -m[1][0] * m[2][1] * m[3][2] + m[1][0] * m[3][1] * m[2][2] + m[1][1] * m[2][0] * m[3][2] - m[1][1] * m[3][0] * m[2][2] - m[1][2] * m[2][0] * m[3][1] + m[1][2] * m[3][0] * m[2][1]
   inv[3][1] = m[0][0] * m[2][1] * m[3][2] - m[0][0] * m[3][1] * m[2][2] - m[0][1] * m[2][0] * m[3][2] + m[0][1] * m[3][0] * m[2][2] + m[0][2] * m[2][0] * m[3][1] - m[0][2] * m[3][0] * m[2][1]
   inv[3][2] = -m[0][0] * m[1][1] * m[3][2] + m[0][0] * m[3][1] * m[1][2] + m[0][1] * m[1][0] * m[3][2] - m[0][1] * m[3][0] * m[1][2] - m[0][2] * m[1][0] * m[3][1] + m[0][2] * m[3][0] * m[1][1]
   inv[3][3] = m[0][0] * m[1][1] * m[2][2] - m[0][0] * m[2][1] * m[1][2] - m[0][1] * m[1][0] * m[2][2] + m[0][1] * m[2][0] * m[1][2] + m[0][2] * m[1][0] * m[2][1] - m[0][2] * m[2][0] * m[1][1]

   invdet = 1. / (m[0][0] * inv[0][0] + m[1][0] * inv[0][1] + m[2][0] * inv[0][2] + m[3][0] * inv[0][3])
   for i in range(4):
       for j in range(4):
           inv[i][j] = invdet * inv[i][j]
   return inv

def mulMatrix44(a,b):
    return tuple(tuple(a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j] + a[i][3] * b[3][j] for j in xrange(4)) for i in xrange(4))

def applyMatrix44(a,v):
    if a is None:
        return v
    return V3(a[i][0] * v[0] + a[i][1] * v[1] + a[i][2] * v[2] + a[i][3] for i in range(3))

def translMatrix44(v):
    return tuple(tuple((IDENTITY44[i][j] if j < 3 or i == 3 else v[i]) for j in range(4)) for i in range(4))

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
    if len(tokens) > 1:
        b.data = int(eval(tokens[1]))
    return Block(b.id,b.data)

class MeshFile(object):
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.materialIndexDict = {None:0}
        self.materials = []
        self.objectData = {}
        self.objects = []

class MeshSTLBinary(MeshFile):
    def __init__(self, filename, myopen=open, swapYZ=False):
        super(MeshSTLBinary,self).__init__()

        with myopen(filename, "rb") as f:
             header = f.read(80)
             assert not header.startswith("solid")
             assert len(header) == 80
             
             vertexCount = 0
             
             numTriangles = struct.unpack("<I", f.read(4))[0]
             
             for i in range(numTriangles):
                assert len(f.read(12))==12 # skip normal
                for i in range(3):
                    v = struct.unpack("<3f", f.read(12))
                    if swapYZ:
                        v = (v[0],v[2],-v[1])
                    self.vertices.append(V3(v))
                self.faces.append((0,(vertexCount,vertexCount+1,vertexCount+2)))
                vertexCount += 3
                assert len(f.read(2))==2 # skip attributes

        assert self.vertices
        assert self.faces

class MeshPLY(MeshFile):
    """
    Currently doesn't support materials or binary data or any data. :-)
    """
    def __init__(self, filename, myopen=open, swapYZ=False):
        super(MeshPLY,self).__init__()

        with myopen(filename, "r") as f:
             assert f.readline().strip() == "ply"
             assert f.readline().strip().startswith("format ascii")
             elementCounts = []
             while True:
                 line = f.readline().strip()
                 if line == "end_header":
                     break
                 args = re.split("\\s+",line)
                 if len(args) >= 3 and args[0] == 'element':
                     elementCounts.append((args[1],int(args[2])))
             assert len(elementCounts) >= 2
             for element,count in elementCounts:
                 for i in range(count):
                     line = f.readline().strip()
                     if element == 'vertex':
                         args = re.split("\\s+",line)
                         if swapYZ:
                             v = V3(float(args[0]),float(args[2]),-float(args[1]))
                         else:
                             v = V3(float(args[0]),float(args[1]),float(args[2]))
                         self.vertices.append(v)
                     elif element == 'face':
                         args = re.split("\\s+",line)
                         count = int(args.pop(0))
                         v = tuple(int(args[j]) for j in range(count))
                         self.faces.append((0,v))

        assert self.vertices
        assert self.faces


class Mesh3DS(MeshFile):
    MAIN3DS = 0x4D4D
    EDIT3DS = 0x3D3D
    KEYF3DS = 0xB000
    KEYF_OBJDES = 0xB002
    KEYF_OBJHIERARCH = 0xB010
    KEYF_PIVOT = 0xB013
    EDIT_OBJECT = 0x4000
    OBJ_TRIMESH = 0x4100
    TRI_VERTEXL = 0x4110
    TRI_FACEL1 = 0x4120
    TRI_LOCAL = 0x4160
    TRI_MATERIAL = 0x4130

    def __init__(self, filename, myopen=open, swapYZ=False):
        super(Mesh3DS,self).__init__()

        self.swapYZ = swapYZ

        if int(sys.version[0]) >= 3:
            self.readAsciiz = self.readAsciiz_python3

        with myopen(filename, "rb") as self.file:
            id,lengthRemaining = self.readChunkHeader()
            lengthRemaining -= 6
            if id != Mesh3DS.MAIN3DS:
                raise IOError("Cannot find main chunk")
            while 0 < lengthRemaining:
                id,chunkLength = self.readChunkHeader()
                lengthRemaining -= 6
                if id == Mesh3DS.EDIT3DS:
                    self.handle_EDIT3DS(chunkLength - 6)
                    lengthRemaining -= chunkLength - 6
                elif id == Mesh3DS.KEYF3DS:
                    self.handle_KEYF3DS(chunkLength - 6)
                    lengthRemaining -= chunkLength - 6
                else:
                    self.skip(chunkLength - 6)
                    lengthRemaining -= chunkLength - 6

        self.processObjects()

        if not self.faces:
            raise IOError("No faces found")

    def processObjects(self):
        i = 0
        for (name,parent,pivot) in self.objects:
            try:
                (object_vertices,object_faces,object_material_data,object_matrix) = self.objectData[name]
            except KeyError:
                 continue

            if not object_vertices:
                 continue

            if determinant44(object_matrix) < 0:
                transform = mulMatrix44(object_matrix, mulMatrix44(((-1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)), invertMatrix44(object_matrix)))
            else:
                transform = None

            if pivot != V3(0,0,0):
               delta = applyMatrix(object_matrix, -pivot)
            else:
               delta = None

            firstObjectVertex = len(self.vertices)

            for v in object_vertices:
                if transform:
                    v = applyMatrix44(transform, v)

                if delta:
                    v = v + delta

                if self.swapYZ:
                    self.vertices.append(V3(v[0],v[2],-v[1]))
                else:
                    self.vertices.append(v1)

            for (faceIndex,face) in enumerate(object_faces):
                material = None
                for (name,faces) in object_material_data:
                    if faceIndex in faces:
                        material = name
                        break

                try:
                    materialIndex = self.materialIndexDict[material]
                except KeyError:
                    materialIndex = len(self.materials)
                    self.materials.append(material)
                    self.materialIndexDict[material] = materialIndex
                self.faces.append((materialIndex, tuple(v + firstObjectVertex for v in face)))

    def readChunkHeader(self):
        return struct.unpack("<HL", self.file.read(6))

    def skip(self,length):
        if length:
            self.file.seek(length,1)

    def readAsciiz(self,lengthRemaining):
        name = ""
        while lengthRemaining > 0:
            byte = self.file.read(1)
            lengthRemaining -= 1
            if ord(byte) == 0:
                return lengthRemaining, name
            name += byte
        raise IOError("Name overflowing chunk")

    def readAsciiz_python3(self,lengthRemaining):
        name = ""
        while lengthRemaining > 0:
            byte = self.file.read(1)
            lengthRemaining -= 1
            if ord(byte) == 0:
                return lengthRemaining, name
            name += byte.decode("cp1252")
        raise IOError("Name overflowing chunk")

    def handle_EDIT3DS(self,lengthRemaining):
        while lengthRemaining > 0:
            id,chunkLength = self.readChunkHeader()
            lengthRemaining -= 6
            if id == Mesh3DS.EDIT_OBJECT:
                self.handle_EDIT_OBJECT(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            else:
                self.skip(chunkLength - 6)
                lengthRemaining -= chunkLength - 6

    def handle_KEYF3DS(self,lengthRemaining):
        while lengthRemaining > 0:
            id,chunkLength = self.readChunkHeader()
            lengthRemaining -= 6
            if id == Mesh3DS.KEYF_OBJDES:
                self.handle_KEYF_OBJDES(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            else:
                self.skip(chunkLength - 6)
                lengthRemaining -= chunkLength - 6

    def handle_KEYF_OBJDES(self,lengthRemaining):
        self.object_name = None
        self.object_pivot = None
        self.object_parent = None
        while lengthRemaining > 0:
            id,chunkLength = self.readChunkHeader()
            lengthRemaining -= 6
            if id == Mesh3DS.KEYF_OBJHIERARCH:
                self.handle_KEYF_OBJHIERARCH(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            elif id == Mesh3DS.KEYF_PIVOT:
                self.handle_KEYF_PIVOT(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            else:
                self.skip(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
        self.objects.append((self.object_name,self.object_parent,self.object_pivot))


    def handle_KEYF_OBJHIERARCH(self,lengthRemaining):
        lengthRemaining, self.object_name = self.readAsciiz(lengthRemaining)
        self.skip(4)
        lengthRemaining -= 4
        self.object_parent = struct.unpack("<h", self.file.read(2))[0]
        lengthRemaining -= 2
        self.skip(lengthRemaining)

    def handle_KEYF_PIVOT(self,lengthRemaining):
        self.object_pivot = V3(struct.unpack("<fff", self.file.read(3 * 4)))
        lengthRemaining -= 3 * 4
        self.skip(lengthRemaining)

    def handle_EDIT_OBJECT(self,lengthRemaining):
        self.object_vertices = []
        self.object_faces = []
        self.object_material_data = []
        self.object_matrix = None

        lengthRemaining, self.object_name = self.readAsciiz(lengthRemaining)
        while lengthRemaining > 0:
            id,chunkLength = self.readChunkHeader()
            lengthRemaining -= 6
            if id == Mesh3DS.OBJ_TRIMESH:
                self.handle_OBJ_TRIMESH(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            else:
                self.skip(chunkLength - 6)
                lengthRemaining -= chunkLength - 6

    def handle_OBJ_TRIMESH(self,lengthRemaining):
        while lengthRemaining > 0:
            id,chunkLength = self.readChunkHeader()
            lengthRemaining -= 6
            if id == Mesh3DS.TRI_VERTEXL:
                self.handle_TRI_VERTEXL(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            elif id == Mesh3DS.TRI_FACEL1:
                self.handle_TRI_FACEL1(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            elif id == Mesh3DS.TRI_LOCAL:
                self.handle_TRI_LOCAL(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            else:
                self.skip(chunkLength - 6)
                lengthRemaining -= chunkLength - 6

        if self.object_matrix is None:
            self.object_matrix = IDENTITY44
        self.objectData[self.object_name] = (self.object_vertices,self.object_faces,self.object_material_data, self.object_matrix)


    def handle_TRI_VERTEXL(self,lengthRemaining):
        count = struct.unpack("<H", self.file.read(2))[0]
        lengthRemaining -= 2
        for i in xrange(count):
            self.object_vertices.append(V3(struct.unpack("<fff", self.file.read(3 * 4))))
            lengthRemaining -= 3 * 4
        self.skip(lengthRemaining)

    def handle_TRI_FACEL1(self,lengthRemaining):
        count = struct.unpack("<H", self.file.read(2))[0]
        lengthRemaining -= 2
        for i in xrange(count):
            self.object_faces.append(struct.unpack("<HHH", self.file.read(2 * 3)))
            lengthRemaining -= 2 * 3
            self.skip(2)
            lengthRemaining -= 2
        while lengthRemaining > 0:
            id,chunkLength = self.readChunkHeader()
            lengthRemaining -= 6
            if id == Mesh3DS.TRI_MATERIAL:
                self.handle_TRI_MATERIAL(chunkLength - 6)
                lengthRemaining -= chunkLength - 6
            else:
                self.skip(chunkLength - 6)
                lengthRemaining -= chunkLength - 6

    def handle_TRI_LOCAL(self,lengthRemaining):
        m = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
        for i in xrange(4):
            for j in xrange(3):
                m[j][i] = struct.unpack("<f", self.file.read(4))[0]
                lengthRemaining -= 4
        self.object_matrix = m
        self.skip(lengthRemaining)

    def handle_TRI_MATERIAL(self,lengthRemaining):
        lengthRemaining,name = self.readAsciiz(lengthRemaining)
        name = name.replace(' ', '_') # TODO: handle "A_B" and "A B" collision
        count = struct.unpack("<H", self.file.read(2))[0]
        lengthRemaining -= 2
        faces = set()
        for i in xrange(count):
            faces.add(struct.unpack("<H", self.file.read(2))[0])
            lengthRemaining -= 2
        self.object_material_data.append((name, faces))
        self.skip(lengthRemaining)

class Mesh(object):
    UNSPECIFIED = None
    SUPPORTED_ARCHIVES = set(['gz','zip'])

    def __init__(self,infile,minecraft=None,rewrite=True):
         if minecraft:
             self.setBlock = minecraft.setBlock
             self.message = minecraft.postToChat
         else:
             self.output = OrderedDict()
             def setBlock(v,b):
                 self.output[v] = b
             self.setBlock = setBlock
             def message(m):
                 print m
             self.message = message

         self.rewrite = rewrite
         self.url = None
         self.urlgz = None
         self.urlzip = None
         self.swapYZ = None
         self.credits = None
         self.size = 100
         self.preYaw = 0
         self.prePitch = 0
         self.preRoll = 0
         self.archive = None
         self.default = STONE
         self.materialBlockDict = {}
         self.materialOrderDict = {}
         self.baseVertices = []
         self.vertices = []
         #self.textures = []
         #self.normals = []
         self.faces = []
         self.materials = []
         self.materialNames = []
         self.haveMaterialArea = False
         self.corner1 = None
         self.corner2 = None
         self.endLineIndex = None
         self.specifiedMeshName = None

         base,ext = os.path.splitext(infile)
         if ext.lower() == '.obj' or ext.lower() == ".3ds" or ext.lower() == ".ply" or ext.lower() == ".stl":
             self.meshName = infile
             self.controlFile = base + ".txt"
         else:
             if os.path.isfile(base + ".3ds") or os.path.isfile(base + ".3ds.gz"):
                 self.meshName = base + ".3ds"
             elif os.path.isfile(base + ".ply") or os.path.isfile(base + ".ply.gz"):
                 self.meshName = base + ".ply"
             elif os.path.isfile(base + ".stl") or os.path.isfile(base + ".stl.gz"):
                 self.meshName = base + ".stl"
             else:
                 self.meshName = base + ".obj"

             if ext == '':
                 self.controlFile = base + ".txt"
             else:
                 self.controlFile = infile

         if os.path.isfile(self.controlFile):
             with open(self.controlFile) as f:
                 self.controlFileLines = f.readlines()
             dirname = os.path.dirname(self.controlFile)
             materialMode = False
             for i,line in enumerate(self.controlFileLines):
                 line = line.strip()
                 if len(line) == 0 or line[0] == '#':
                     continue
                 found = re.match('([^\\s]+) (.*)$', line)
                 if found:
                     def getString():
                         if found.group(2).startswith('"') or found.group(2).startswith("'") or found.group(2).startswith('u"') or found.group(2).startswith("u'"):
                             return safeEval(found.group(2))
                         else:
                             return found.group(2)
                     token = found.group(1).lower()
                     if materialMode:
                         self.materialBlockDict[found.group(1)] = parseBlock(found.group(2),self.default)
                     elif token == "file":
                         self.specifiedMeshName = getString()
                         self.meshName = dirname + "/" + self.specifiedMeshName
                     elif token == "archive":
                         self.archive = getString()
                         if self.archive.lower() not in Mesh.SUPPORTED_ARCHIVES:
                             self.archive = dirname + '/' + self.archive
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
                     elif token == "yaw":
                         self.preYaw = safeEval(found.group(2))
                     elif token == "pitch":
                         self.prePitch = safeEval(found.group(2))
                     elif token == "roll":
                         self.preRoll = safeEval(found.group(2))
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
             if self.archive in Mesh.SUPPORTED_ARCHIVES:
                 self.archive = self.meshName + "." + self.archive
             if self.swapYZ is None:
                 self.swapYZ = self.meshName.lower().endswith(".3ds") or self.meshName.lower().endswith(".stl") 
         elif rewrite:
             if not os.path.isfile(self.meshName):
                 raise IOError("Cannot find mesh file")
             if self.meshName.lower().endswith(".3ds") or self.meshName.lower().endswith(".stl"):
                 self.swapYZ = True
             self.message("Creating a default control file")
             with open(self.controlFile,"w") as f:
                self.controlFileLines = []
                self.controlFileLines.append("file " + repr(os.path.basename(self.meshName)) + "\n")
                if self.swapYZ:
                   self.controlFileLines.append("swapyz 1\n")
                else:
                   self.controlFileLines.append("swapyz 0\n")
                self.controlFileLines.append("#credits Mesh by ..., copyright (c) ...\n")
                self.controlFileLines.append("yaw 0\n")
                self.controlFileLines.append("pitch 0\n")
                self.controlFileLines.append("roll 0\n")
                self.controlFileLines.append("size " + str(self.size) + "\n")
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
        if self.archive and os.path.isfile(self.archive):
            if self.archive.lower().endswith(".gz"):
                return self.archive, gzip.open, None
            elif self.archive.lower().endswith(".zip"):
                z = ZipFile(self.archive)
                return self.specifiedMeshName, z.open, z.close
            else:
                raise IOError("Unsupported archive type")
        if os.path.isfile(self.meshName):
            return self.meshName, open, None
        if os.path.isfile(self.meshName + ".gz"):
            return self.meshName + ".gz", gzip.open, None
        if tryDownload and (self.url or self.urlgz):
            self.message("Downloading mesh")
            urlzip = False
            if self.urlgz:
                url = self.urlgz
                outName = self.meshName + ".gz"
            elif self.url:
                url = self.url
                if self.archive:
                    outName = self.archive
                else:
                    outName = self.meshName
            content = urllib2.urlopen(url).read()
            with open(outName + ".tempDownload","wb") as f:
                f.write(content)
            os.rename(outName + ".tempDownload", outName)
            self.message("Downloaded")
            return self.getFile()
        else:
            raise IOError("File not found")

    def read(self, rewriteControlFile=None):
        if self.swapYZ:
            fix = lambda list : V3(list[0], list[2], -list[1])
        else:
            fix = lambda list : V3(list)

        warned = set()
        currentMaterialIndex = 0
        if self.preYaw != 0 or self.prePitch != 0 or self.preRoll != 0:
            matrix = makeMatrix(self.preYaw, self.prePitch, self.preRoll)
        else:
            matrix = None

        name,myopen,closeArchive = self.getFile()
        if self.credits:
            self.message("Credits: " + self.credits)

        if name.endswith(".3ds") or name.endswith(".3ds.gz") or name.endswith(".ply") or name.endswith(".ply.gz") or name.endswith(".stl") or name.endswith(".stl.gz"):
            if name.endswith(".3ds") or name.endswith(".3ds.gz"):
                MeshFormat = Mesh3DS
            elif name.endswith(".ply") or name.endswith(".ply.gz"):
                MeshFormat = MeshPLY
            else:
                MeshFormat = MeshSTLBinary
            mesh = MeshFormat(name,myopen=myopen,swapYZ=self.swapYZ)
            self.baseVertices = mesh.vertices
            self.faces = mesh.faces
            self.materialBlocks = []
            self.materialOrders = []
            for name in mesh.materials:
                self.materialOrders.append(self.materialOrderDict.get(name, 0))
                self.materialBlocks.append(self.materialBlockDict.get(name, self.default))
                if name not in self.materialBlockDict and name not in warned:
                    self.message("Material " + name + " not defined")
                    warned.add(name)
            if len(self.materialBlocks) == 0:
                self.materialBlocks.append(self.default)
        else:
            self.materialBlocks = [self.default]
            self.materialOrders = [0]
            materialIndexDict = { Mesh.UNSPECIFIED: 0 }

            with myopen(name) as fh:
                for line in fh :
                    line = line.strip()
                    if len(line) == 0 or line[0] == '#' : continue
                    line = re.split('\s+', line)
                    if line[0] == 'v' :
                        self.baseVertices.append(applyMatrix(matrix,V3(fix([float(x) for x in line[1:]]))))
                    #elif line[0] == 'vt' : #tex-coord
                    #    self.textures.append(fix(line[1:]))
                    #elif line[0] == 'vn' : #normal vector
                    #    self.normals.append(fix(line[1:]))
                    elif line[0] == 'f' : #face
                        face = line[1:]
                        for i in xrange(0, len(face)) :
                            # OBJ indexies are 1 based not 0 based hence the -1
                            # convert indexes to integer
                            face[i] = int(face[i].split('/')[0]) - 1
                            # skip texture and normal
    #                        for j in xrange(0, len(face[i])) :
    #                            if face[i][j] != "":
    #                                face[i][j] = int(face[i][j]) - 1
                        #prepend the material currently in use to the face
                        self.faces.append((currentMaterialIndex,face))
                    elif line[0] == 'usemtl': # material
                        name = line[1]
                        try:
                            currentMaterialIndex = materialIndexDict[name]
                        except KeyError:
                            currentMaterialIndex = len(self.materialBlocks)
                            materialIndexDict[name] = currentMaterialIndex
                            self.materialOrders.append(self.materialOrderDict.get(name, 0))
                            self.materialBlocks.append(self.materialBlockDict.get(name, self.default))
                            if name not in self.materialBlockDict and name not in warned:
                                self.message("Material " + name + " not defined")
                                warned.add(name)

        if closeArchive:
            closeArchive()

        if self.rewrite and warned:
            try:
                self.message("Rewriting control file to include missing materials")
                with open(self.controlFile + ".tempFile", "w") as f:
                    f.write(''.join(self.controlFileLines[:self.endLineIndex]))
                    if not self.haveMaterialArea:
                        f.write('\nmaterials\n')
                    for material in warned:
                        f.write(material + ' default\n')
                    f.write(''.join(self.controlFileLines[self.endLineIndex:]))
                try:
                    os.unlink(self.controlFile + ".bak")
                except:
                    pass
                try:
                    os.rename(self.controlFile, self.controlFile + ".bak")
                except:
                    pass
                os.rename(self.controlFile + ".tempFile", self.controlFile)
            except:
                self.message("Couldn't rewrite control file")

    def scale(self, bottomCenter, matrix=None):
        bottomCenter = V3(bottomCenter)
        
        minimum = [None, None, None]
        maximum = [None, None, None]

        self.vertices = []

        for v in self.baseVertices:
            vertex = applyMatrix(matrix,v)
            self.vertices.append(vertex)
            for i in range(3):
                if minimum[i] == None or vertex[i] < minimum[i]:
                    minimum[i] = vertex[i]
                if maximum[i] == None or vertex[i] > maximum[i]:
                    maximum[i] = vertex[i]

        center = [(maximum[i] + minimum[i]) / 2 for i in range(3)]

        maxsize = max(( maximum[i] - minimum[i] for i in range(3) ))

        scale = self.size / maxsize
        translate = V3(bottomCenter.x - scale * center[0], bottomCenter.y - scale * minimum[1], bottomCenter.z - scale * center[2])

        for i in range(len(self.vertices)):
            self.vertices[i] = self.vertices[i] * scale + translate

        self.corner1 = (V3(minimum) * scale + translate).ifloor()
        self.corner2 = (V3(maximum) * scale + translate).iceil()

    def drawVertices(self, vertices, material):
        block = self.materialBlocks[material]
        for vertex in vertices:
            if material != self.drawRecord.get(vertex):
                self.setBlock(vertex, block)
                self.drawRecord[vertex] = material

    def render(self):
        self.drawRecord = {}

        if len(self.materialOrderDict):
            faces = sorted(self.faces, key=lambda a : self.materialOrders[a[0]])
        else:
            faces = self.faces

        for faceCount,(material,face) in enumerate(faces):
            if faceCount % 4000 == 0:
                self.message("{0:.1f}%".format(100. * faceCount / len(self.faces)))

            faceVertices = [self.vertices[v] for v in face]
            self.drawVertices(getFace(faceVertices), material)

def go(filename, args=[]):
    mc = minecraft.Minecraft()

    playerPos = mc.player.getPos()

    mc.postToChat("Preparing")
    mesh = Mesh(filename, minecraft=mc)
    mc.postToChat("Reading")
    mesh.read()
    mc.postToChat("Scaling")

    opts = ""

    if args and (args[0] == '-' or re.match("^-?[a-zA-Z]", args[0])):
       opts = args.pop(0)

    if args:
       s = args.pop(0)
       if s and int(s):
           mesh.size = int(s)

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

    mesh.scale(playerPos, matrix)

    if 'n' not in opts:
        mc.postToChat("Clearing")
        mc.setBlocks(mesh.corner1,mesh.corner2,AIR)
    mc.postToChat("Rendering")
    mesh.render()
    mc.postToChat("Done!")

# main program
if __name__ == "__main__":
    if len(sys.argv) < 2:
        if settings.isPE:
            go("models/RaspberryPi.txt")
        else:
            from tkFileDialog import askopenfilename
            from Tkinter import *
            master = Tk()
            master.wm_title("render")
            master.attributes("-topmost", True)
            Label(master, text='Size').grid(row=0)
            size = Entry(master)
            size.grid(row=0,column=1)
            size.delete(0,END)
            Label(master, text='Yaw').grid(row=1)
            yaw = Entry(master)
            yaw.grid(row=1,column=1)
            yaw.delete(0,END)
            yaw.insert(0,"0")
            Label(master, text='Pitch:').grid(row=2)
            pitch = Entry(master)
            pitch.grid(row=2,column=1)
            pitch.delete(0,END)
            pitch.insert(0,"0")
            Label(master, text='Roll:').grid(row=3)
            roll = Entry(master)
            roll.grid(row=3,column=1)
            roll.delete(0,END)
            roll.insert(0,"0")
            clearing = IntVar()
            c = Checkbutton(master, text="Clear area", variable = clearing)
            c.grid(row=4,column=0,columnspan=2)
            c.select()

            def selectFileAndGo():
                name = askopenfilename(initialdir='models',filetypes=['controlfile {*.txt}', 'all {*}'])
                if name:
                     options = '-'
                     if not clearing:
                         options += 'n'
                     args = [options, size.get(), yaw.get(), pitch.get(), roll.get()]
                     master.destroy()
                     go(name, args)
                else:
                     master.destroy()

            b = Button(master, text="Select file and go",command = selectFileAndGo)
            b.grid(row=5,column=0,columnspan=2,rowspan=2)

            mainloop()
    else:
        go(os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + "models/" + sys.argv[1] + ".txt", sys.argv[2:])

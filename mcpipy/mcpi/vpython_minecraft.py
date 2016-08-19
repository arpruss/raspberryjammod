#
# Use this in place of minecraft.py to test simple scripts without Minecraft
# if you have vpython installed. This only supports a small subset of the full API.
#
# This gets substituted for Minecraft.py if you have the VPYTHON_MCPI environment
# variable set to something. If you have a Linux-style commandline, you can run
# demo scripts against vpython as follows:
#   VPYTHON_MCPI=1 python trefoil2.py
#

from __future__ import absolute_import
from visual import *
import thread
from .util import flatten,floorFlatten
from .block import Block
from .vec3 import Vec3
from os import environ
import time

materialList = [None for i in range(Block.MAX_MATERIAL+1)]
materialList[Block.MATERIAL_DEFAULT] = materials.plastic
materialList[Block.MATERIAL_WOOD] = materials.wood
materialList[Block.MATERIAL_STONE] = materials.rough
materialList[Block.MATERIAL_PLASTIC] = materials.plastic
materialList[Block.MATERIAL_EMISSIVE] = materials.emissive
materialList[Block.MATERIAL_ROUGH] = materials.rough

originalsleep = None

def getMaterial(block):
    return materialList[block.getMaterial()]    

def getColorScaled(block):
    r,g,b,opacity = block.getRGBA()
    return (r/255.,g/255.,b/255.),opacity/255.
    
class Ignore:
    def undefinedFunction(self, *args):
        return []
        
    def __getattr__(self,name):
        return self.undefinedFunction        
	
class Minecraft:
    def __init__(self, connection=None, autoId=True):
        self.scene = {}
        self.x = 0.5
        self.y = 0.5
        self.z = 0.5
        self.yaw = 0

        self.events = Ignore()
        
        self.player = Ignore()
        
        self.player.getPos = lambda : Vec3(self.x,self.y,self.z)
        self.player.getTilePos = lambda : Vec3(int(floor(self.x)),int(floor(self.y)),int(floor(self.z)))
        self.player.getRotation = lambda : self.yaw
        self.player.getPitch = lambda : 0
        
        self.entity = Ignore()

        self.entity.getPos = lambda a: Vec3(self.x,self.y,self.z)
        self.entity.getTilePos = lambda a: Vec3(int(floor(self.x)),int(floor(self.y)),int(floor(self.z)))
        self.entity.getRotation = lambda a: self.yaw
        self.entity.getPitch = lambda a: 0
        
        if environ.get('VPYTHON_MCPI', '1') == 'player':
            self.me = cone(pos=(self.x-0.5,self.y,self.z-0.5), axis=(1,0,0), radius=0.5)
            self.updatePosition()
            thread.start_new_thread(self.moveAround, ())
            scene.bind('keydown', self.keyInput)
        
    def keyInput(self,evt):        
        if evt.key == 'w':
            self.x -= .25 * -sin(radians(self.yaw))
            self.z -= .25 * cos(radians(self.yaw))
            self.needUpdate = True
        elif evt.key == 's':
            self.x += .25 * -sin(radians(self.yaw))
            self.z += .25 * cos(radians(self.yaw))
            self.needUpdate = True
        elif evt.key == 'a':
            self.x += .25 * -sin(radians(self.yaw+90))
            self.z += .25 * cos(radians(self.yaw+90))
            self.needUpdate = True
        elif evt.key == 'd':
            self.x += .25 * -sin(radians(self.yaw-90))
            self.z += .25 * cos(radians(self.yaw-90))
            self.needUpdate = True
        elif evt.key == 'q':
            self.yaw -= 45/2.
            self.needUpdate = True
        elif evt.key == 'e':
            self.yaw += 45./2.
            self.needUpdate = True
        self.yaw %= 360.
        
    def updatePosition(self):
        axis = (sin(radians(self.yaw)), 0, -cos(radians(self.yaw)))
        self.me.pos = (self.x-0.5,self.y,self.z-0.5)        
        self.me.axis = axis
        self.me.visible = True
        self.needUpdate = False
        
    def moveAround(self):
        while True:
            originalsleep(0.05)
            if self.needUpdate:
                self.updatePosition()
        
    def undefinedFunction(self, *args):
        pass
        
    def __getattr__(self, name):
        return self.undefinedFunction
        
    def postToChat(self, message):
        print(message)
		
    def setBlock(self, *args):
        args = map(int, list(floorFlatten(args)))
        for i in range(len(args), 5):
            args.append(0)
            
        coords = tuple(args[0:3])
		
        if args[3] == 0:
            if coords in self.scene:
                self.scene[coords].visible = False
                del self.scene[coords]
        else:
            c,opacity = getColorScaled(Block(args[3],args[4]))
            if coords in self.scene:
                self.scene[coords].visible = False
                del self.scene[coords]            
            m = getMaterial(Block(args[3],args[4]))
            self.scene[coords] = box(pos=tuple(coords), length=1, height=1, width=1, color=c, opacity=opacity, material=m)

    def getHeight(self, *args):
        args = map(int, list(floorFlatten(args)))
        x0 = args[0]
        z0 = args[1]
        h = -20
        for (x,y,z) in self.scene:
            if x == x0 and z == z0 and y > h:
                h = y
        return h

    def setBlocks(self, *args):
        args = map(int, list(floorFlatten(args)))
        for i in range(len(args), 8):
            args.append(0)
            
        if args[6] == 0:
            for x in range(min(args[0],args[3]),max(args[0],args[3])+1):
                for y in range(min(args[1],args[4]),max(args[1],args[4])+1):
                    for z in range(min(args[2],args[5]),max(args[2],args[5])+1):
                        if (x,y,z) in self.scene:
                            self.scene[(x,y,z)].visible = False
                            del self.scene[(x,y,z)]
        else:
            c,opacity = getColorScaled(Block(args[6],args[7]))
            m = getMaterial(Block(args[6],args[7]))
            for x in range(min(args[0],args[3]),max(args[0],args[3])+1):
                for y in range(min(args[1],args[4]),max(args[1],args[4])+1):
                    for z in range(min(args[2],args[5]),max(args[2],args[5])+1):
                        coords = (x,y,z)
                        if coords in self.scene:
                            self.scene[coords].visible = False
                            del self.scene[coords]
                        self.scene[coords] = box(pos=coords, length=1, height=1, width=1, color=c, opacity=opacity, material=m)

    @staticmethod
    def create(address = None, port = None):
        return Minecraft()

# monkey-patch normal sleep function with visual python's
originalsleep = time.sleep
time.sleep = sleep

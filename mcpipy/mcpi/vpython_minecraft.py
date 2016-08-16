#
# Use this in place of minecraft.py to test simple scripts without Minecraft
# if you have vpython installed. This only supports a small subset of the full API.
#

from __future__ import absolute_import
from visual import *
from .util import flatten,floorFlatten
from .block import Block
from .colors import opaquePalette,translucentPalette
from .vec3 import Vec3

def getColorRGB(block):
    if block.id == 0:
        return (255,255,255)
    for collection in (opaquePalette,translucentPalette):
        for c in collection:
            if c[0].id == block.id and c[0].data == block.data:
                return (c[1][0]/255., c[1][1]/255., c[1][2]/255.)
    for collection in (opaquePalette,translucentPalette):
        for c in collection:
            if c[0].id == block.id:
                return (c[1][0]/255., c[1][1]/255., c[1][2]/255.)
	return color.blue	
    
class Object:
    pass
	
class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi."""

    def __init__(self, connection=None, autoId=True):
        self.scene = {}
        self.player = Object()
        
        def empty(*args):
            pass

        self.player.getPos = lambda : Vec3(0,0,0)
        self.player.getTilePos = lambda : Vec3(0,0,0)
        self.player.setPos = empty
        self.player.setTilePos = empty
        
    def postToChat(self, message):
        print(message)
		
    def setBlock(self, *args):
        adjArgs = map(int, list(floorFlatten(args)))
        for i in range(len(adjArgs), 5):
            adjArgs.append(0)
            
        coords = tuple(adjArgs[0:3])
		
        if adjArgs[3] == 0:
            if coords in self.scene:
                self.scene[coords].visible = False
                del self.scene[coords]
        else:
            c = getColorRGB(Block(adjArgs[3],adjArgs[4]))
            self.scene[coords] = box(pos=tuple(coords), length=1, height=1, width=1, color=c)

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
            c = getColorRGB(Block(args[3],args[4]))
            for x in range(min(args[0],args[3]),max(args[0],args[3])+1):
                for y in range(min(args[1],args[4]),max(args[1],args[4])+1):
                    for z in range(min(args[2],args[5]),max(args[2],args[5])+1):
                        self.scene[(x,y,z)] = box(pos=(x,y,z), length=1, height=1, width=1, color=c)

    @staticmethod
    def create(address = None, port = None):
        return Minecraft()

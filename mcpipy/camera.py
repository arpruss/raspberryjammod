from mine import *
import pygame.camera
import colors
from time import sleep
from sys import argv
import random

def clamp(x,a,b):
    return min(b,max(x,a))

mc = Minecraft()
pos = mc.player.getTilePos()

#dither = colors.DitheringMethod(rng=lambda:clamp(random.gauss(0,20),-40,40))
dither = colors.DitheringMethod(rng=lambda:random.uniform(-20,20))
width = 80
if len(argv) >= 2:
   width = int(argv[1])
height = width * 3 // 4

pygame.camera.init()
camlist = pygame.camera.list_cameras()

if camlist:
    cam = pygame.camera.Camera(camlist[0],(640,480))
    current = [[block.AIR for y in range(height)] for x in range(width)]
    random.seed(1234) # ensure same seed for each frame
    while True:
        image = pygame.transform.scale(cam.get_image(), (width,height))
        
        for x,y,block in colors.imageToBlocks(image.get_at, width, height, dither=dither):
            if current[x][y] != block:
                mc.setBlock(pos.x+x,pos.y+height-1-y,pos.z,block)
                current[x][y] = block 
        sleep(2)

else:
   mc.postToChat('Camera not found')

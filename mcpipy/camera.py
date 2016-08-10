from mc import *
import pygame.camera
import colors
from time import sleep
from sys import argv

mc = Minecraft()
pos = mc.player.getTilePos()

dither = True
width = 80
if len(argv) >= 2:
   width = int(argv[1])
height = width * 3 // 4

pygame.camera.init()
camlist = pygame.camera.list_cameras()
if camlist:
   cam = pygame.camera.Camera(camlist[0],(640,480))
   current = [[(-1,-1) for y in range(height)] for x in range(width)]
   while True:
       image = pygame.transform.scale(cam.get_image(), (width,height))
       if not dither:
           for x in range(width):
               for y in range(height):
                   block,_ = colors.rgbToBlock(image.get_at((x,y)))
                   if current[x][y] != block:
                       mc.setBlock(pos.x+x,pos.y+height-1-y,pos.z,block)
                       current[x][y] = block
       else:
           pixels = [[list(image.get_at((x,y))[0:3]) for y in range(height)] for x in range(width)]
           for x in range(width):
               for y in range(height):
                   block,actualRGB = colors.rgbToBlock(pixels[x][y])
                   if current[x][y] != block:
                       mc.setBlock(pos.x+x,pos.y+height-1-y,pos.z,block)
                       current[x][y] = block
                   for i in range(3):
                       err = pixels[x][y][i] - actualRGB[i]
                       if x + 1 < width:
                           pixels[x+1][y][i] += err * 7 // 16
                       if y + 1 < height:
                           if 0 < x:
                               pixels[x-1][y+1][i] += err * 3 // 16
                           pixels[x][y+1][i] += err * 5 // 16
                           if x + 1 < width:
                               pixels[x+1][y+1][i] += err // 16
       sleep(0.5)

else:
   mc.postToChat('Camera not found')

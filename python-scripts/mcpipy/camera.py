from mc import *
import pygame.camera
from time import sleep
from sys import argv

COLORS = ( (35,0, 222,222,222),
		(35,1, 219,125,63),
		(35,2, 180,81,189),
		(35,3, 107,138,201),
		(35,4, 177,166,39),
		(35,5, 66,174,57),
		(35,6, 208,132,153),
		(35,7, 64,64,64),
		(35,8, 155,161,161),
		(35,9, 47,111,137),
		(35,10, 127,62,182),
		(35,11, 46,57,142),
		(35,12, 79,50,31),
		(35,13, 53,71,27),
		(35,14, 151,52,49),
		(35,15, 26,22,22),
		(159,0,210,178,161),
		(159,1,162,84,38),
		(159,2,150,88,109),
		(159,3,113,109,138),
		(159,4,186,133,35),
		(159,5,104,118,53),
		(159,6,162,78,79),
		(159,7,58,42,36),
		(159,8,135,107,98),
		(159,9,87,91,91),
		(159,10,118,70,86),
		(159,11,74,60,91),
		(159,12,77,51,36),
		(159,13,76,83,42),
		(159,14,143,61,47),
		(159,15,37,23,16),
		(155,0,232,228,220),
		(152,0,164,26,9),
		(41,0,250,239,80),
		(173,0,19,19,19) )

def colorDist(a,b):
    return (a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])+(a[2]-b[2])*(a[2]-b[2])

def getBestColor(rgb):
    bestColor = COLORS[0]
    bestDist = 255*255*3
    for c in COLORS:
        d = colorDist(c[2:],rgb)
        if d < bestDist:
            bestDist = d
            bestColor = c
    return bestColor

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
                   block = getBestColor(image.get_at((x,y)))[0:2]
                   if current[x][y] != block:
                       mc.setBlock(pos.x+x,pos.y+height-1-y,pos.z,block)
                       current[x][y] = block
       else:
           pixels = [[list(image.get_at((x,y))[0:3]) for y in range(height)] for x in range(width)]
           for x in range(width):
               for y in range(height):
                   color = getBestColor(pixels[x][y])
                   block = color[0:2]
                   if current[x][y] != block:
                       mc.setBlock(pos.x+x,pos.y+height-1-y,pos.z,block)
                       current[x][y] = block
                   for i in range(3):
                       err = pixels[x][y][i] - color[2+i]
                       if x + 1 < width:
                           pixels[x+1][y][i] += err * 7 // 16
                       if y + 1 < height:
                           if 0 < x:
                               pixels[x-1][y+1][i] += err * 3 // 16
                           pixels[x][y+1][i] += err * 5 // 16
                           if x + 1 < width:
                               pixels[x+1][y+1][i] += err // 16

else:
   mc.postToChat('Camera not found')

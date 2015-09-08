from mc import *
import pygame
import pygame.camera
from time import sleep

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

def rgbToBlock(rgb):
    bestColor = COLORS[0][0:2]
    bestDist = 255*255*3
    for c in COLORS:
        d = colorDist(c[2:],rgb)
        if d < bestDist:
            bestDist = d
            bestColor = c[0:2]
    return bestColor

mc = Minecraft()
pos = mc.player.getTilePos()

pygame.init()
pygame.camera.init()
camlist = pygame.camera.list_cameras()
if camlist:
   cam = pygame.camera.Camera(camlist[0],(640,480))
   while True:
       image = pygame.transform.scale(cam.get_image(), (120,90))
       for x in range(120):
           for y in range(90):
               block = rgbToBlock(image.get_at((x,89-y))[0:3])
               mc.setBlock(pos.x+x,pos.y+y,pos.z,block)
else:
   mc.postToChat('Camera not found')

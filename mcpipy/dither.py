#
# Code by Alexander Pruss and under the MIT license
#

#

from mine import *
import colors
import sys
import os
from PIL import Image
from fonts import FONTS
import random
import text

mc = Minecraft()
pos = mc.player.getTilePos()

filename = sys.argv[1]
if not os.path.isfile(filename):
    filename = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + filename    

if len(sys.argv) > 2:
    height = int(sys.argv[2])
else:
    height = 140
        
image = Image.open(filename).convert('RGBA')

scale = height / float(image.size[1])
width = int(image.size[0] * scale)

def getPixel(z):
    x = z[0] / scale
    if x >= image.size[0]: x = image.size[0] - 1
    y = z[1] / scale
    if y >= image.size[1]: y = image.size[1] - 1
    return image.getpixel((x,image.size[1]-1-y))

def clamp(x,a,b):
    return min(b,max(x,a))
    
dithers = [
    (None, 'undithered'),
    (colors.DitheringMethod(fs=True), 'Floyd-Steinberg'),
    (colors.DitheringMethod(rng=lambda:random.uniform(-10,10)), 'uniform 10'),
    (colors.DitheringMethod(rng=lambda:random.uniform(-20,20)), 'uniform 20'),
    (colors.DitheringMethod(rng=lambda:random.uniform(-40,40)), 'uniform 40'),
    (colors.DitheringMethod(rng=lambda:clamp(random.gauss(0,10),-30,30)), 'gaussian 10/30'),
    (colors.DitheringMethod(rng=lambda:clamp(random.gauss(0,20),-30,30)), 'gaussian 20/30') ]
    
x0 = pos.x

for dither,name in dithers:
    for (x,y,block) in colors.imageToBlocks(getPixel, width, height, dither=dither):
         mc.setBlock(x+x0,y+pos.y,pos.z,block)
    
    text.drawText(mc, FONTS['thin9pt'], 
                        Vec3(x0,pos.y+height+1,pos.z), 
                        Vec3(1,0,0), Vec3(0,1,0), 
                        name, block.SEA_LANTERN, background=None)
    x0 += width + 2
   
#
# Code by Alexander Pruss and under the MIT license
#
# Needs Pillow
#

#
# earth.py [size [filename]]
#

from mine import *
import os.path,sys
from PIL import Image
from pysanka import egg, getPixel

mc = Minecraft()
pos = mc.player.getTilePos()

height = 100
filename = None

if len(sys.argv) > 1:
    height = int(sys.argv[1])
    if len(sys.argv) > 2:
        filename = sys.argv[2]
        if not os.path.isfile(filename):
            filename = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + filename    

if filename is None:
    filename = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + "nasaearth.jpg"
    
    
image = Image.open(filename).convert('RGB')

for (x,y,z,block,theta) in egg(h=height,block=None,sphere=True):
    mc.setBlock(x+pos.x,y+pos.y,z+pos.z,getPixel(image, (theta / (2*pi)) % 1, y / float(height), dither=10))

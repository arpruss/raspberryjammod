from mc import *
import sys
import os
from ast import literal_eval
from PIL import Image

def parseBlock(s):
    try:
        return literal_eval(s)
    except:
        return globals()[s.upper()]

def egg(block=GOLD_BLOCK, h=40, a=2.5, b=1, c=0.1):
    def radius(y):
        if y < 0 or y >= h:
            return 0
        l = y / float(h-1)
        # Formula from: http://www.jolyon.co.uk/myresearch/image-analysis/egg-shape-modelling/
        return h*a*exp((-0.5*l*l+c*l-.5*c*c)/(b*b))*sqrt(1-l)*sqrt(l)/(pi*b)

    for y in range(0,h):
        r = radius(y)
        minimumr = min(r-2,radius(y-1),radius(y+1))
        for x in range(-h,h+1):
            for z in range(-h,h+1):
                myr = sqrt(x*x + z*z)
                if myr <= r and minimumr <= myr:
                    if x==0 and z==0:
                        theta = 0
                    else:
                        theta = atan2(z,x)+pi/2
                    yield (x,y,z,block,theta % (2*pi))
                    
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

def getPixel(image, x, y):
    rgb = image.getpixel(( floor( x * image.size[0] ), image.size[1]-1-floor( y * image.size[1] ) ))
    return getBestColor(rgb)

mc = Minecraft()

if len(sys.argv) > 1:
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        filename = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + filename    
else:
    filename = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + "pysanka.jpg"

image = Image.open(filename).convert('RGB')

if len(sys.argv) > 2:
    height = int(sys.argv[2])
else:
    height = 100
    
if len(sys.argv) > 3:
    repeat = int(sys.argv[3])
else:
    repeat = 2

pos = mc.player.getPos()

for (x,y,z,block,theta) in egg(h=height,block=None):
    mc.setBlock(x+pos.x,y+pos.y,z+pos.z,getPixel(image, (theta * repeat / (2*pi)) % 1, y / float(height)))
   
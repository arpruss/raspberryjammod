#
# Code by Alexander Pruss and under the MIT license
#

#
# pysanka.py [filename [height [oval|N]]]
#  oval: wrap an oval image onto an egg
#  N: wrap a rectangular image onto an egg N times (N is an integer)
#
# Yeah, these arguments are a mess!


from mine import *
import colors
import sys
import os
from PIL import Image
from random import uniform

def egg(block=block.GOLD_BLOCK, h=40, a=2.5, b=1, c=0.1, sphere=False):
    def radius(y):
        if y < 0 or y >= h:
            return 0
        if sphere:
            return sqrt((h/2.)**2 - (y-h/2.)**2)
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
                    
def getPixel(image, x, y, dither=None):
    rgb = image.getpixel(( image.size[0]-1-floor( x * image.size[0] ), image.size[1]-1-floor( y * image.size[1] ) ))
    if dither is not None:
        tweaked = ( rgb[0] + uniform(-dither,dither), rgb[1] + uniform(-dither,dither), rgb[2] + uniform(-dither,dither) )
        return colors.rgbToBlock(tweaked)[0]
    return colors.rgbToBlock(rgb)[0]

if __name__ == '__main__':    
    mc = Minecraft()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            filename = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + filename    
    else:
        filename = os.path.dirname(os.path.realpath(sys.argv[0])) + "/" + "pysanka.jpg"

    if len(sys.argv) > 2:
        height = int(sys.argv[2])
    else:
        height = 100
        
    oval = False
    sphereWrap = False
        
    if len(sys.argv) > 3:
        if sys.argv[3] == "oval":
            oval = True
        elif sys.argv[3] == "sphere":
            sphereWrap = True
        else:
            repeat = int(sys.argv[3])
    else:
        repeat = 2

    pos = mc.player.getPos()

    if oval:
        image = Image.open(filename).convert('RGBA')

        first = None
        last = None
        
        start = [None] * image.size[1]
        stop = [None] * image.size[1]

        for y in range(image.size[1]):
            for x in range(image.size[0]):
                _,_,_,alpha = image.getpixel((x,y))
                if alpha == 255:
                    start[y] = x
                    break
            for x in range(image.size[0]-1,-1,-1):
                _,_,_,alpha = image.getpixel((x,y))
                if alpha == 255:
                    stop[y] = x
                    break
            if start[y] is not None:
                if first is None:
                    first = y    
                last = y
                
        assert first is not None

        for (x,y,z,block,theta) in egg(h=height,block=None):
            imageY = first + int(float(height-1-y)/height*(last-first+1))
            if imageY < first:
                imageY = first
            if imageY > last:
                imageY = last
            imageX = start[imageY]+ int((0.5 - 0.5 * sin(theta)) * (stop[imageY]-start[imageY]))
            if imageX < start[imageY]:
                imageX = start[imageY]
            if imageX > stop[imageY]:
                imageX = stop[imageY]
            mc.setBlock(x+pos.x,y+pos.y,z+pos.z, getPixel(image, imageX, imageY))
    else:
        image = Image.open(filename).convert('RGB')

        for (x,y,z,block,theta) in egg(h=height,block=None):
            mc.setBlock(x+pos.x,y+pos.y,z+pos.z,getPixel(image, (theta * repeat / (2*pi)) % 1, y / float(height), dither=20))
   
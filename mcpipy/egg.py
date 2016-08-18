from mine import *
import sys

def egg(block=block.GOLD_BLOCK, h=40, a=2.5, b=1, c=0.1):
    for y in range(0,h+1):
        l = y / float(h)
        # Formula from: http://www.jolyon.co.uk/myresearch/image-analysis/egg-shape-modelling/
        r = h*a*exp((-0.5*l*l+c*l-.5*c*c)/(b*b))*sqrt(1-l)*sqrt(l)/(pi*b)
        r2 = r*r
        for x in range(-h,h+1):
            for z in range(-h,h+1):
                myr2 = x*x + z*z
                if myr2 <= r2:
                    if x==0 and z==0:
                        theta = 0
                    else:
                        theta = atan2(z,x)
                    yield (x,y,z,block,theta)
					
mc = Minecraft()

if len(sys.argv) >= 2:
    height = int(sys.argv[1])
else:
    height = 50
    
if len(sys.argv) >= 3:
    material = Block.byName(sys.argv[2])
else:
    material = block.GOLD_BLOCK

pos = mc.player.getPos()

for (x,y,z,block,theta) in egg(h=height,block=material):
    mc.setBlock(x+pos.x,y+pos.y,z+pos.z,block)

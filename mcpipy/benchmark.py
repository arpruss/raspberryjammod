from __future__ import print_function
from time import time
from mcpi.minecraft import Minecraft
mc = Minecraft.create()
t = time()
for i in range(1000):
    mc.getBlock(0,0,0)
print("getBlock : {}ms".format(1000.*(time()-t)/1000.))
t = time()
for i in range(10000):
    mc.setBlock(0,0,0,1)
mc.getBlock(0,0,0)
print("setBlock same : {}ms".format(1000.*(time()-t)/10000.))
t = time()
for i in range(10000):
    mc.setBlock(0,0,0,i&1)
mc.getBlock(0,0,0)
print("setBlock different : {}ms".format(1000.*(time()-t)/10000.))

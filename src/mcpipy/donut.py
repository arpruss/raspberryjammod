#!/usr/bin/env python

#
# (c) 2015 Alexander R. Pruss
#

#
# Draw a water-filled donut
#

import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import math

def draw_donut(mcx,mcy,mcz,R,r,mcblock,mcmeta):
  for x in range(-R-r,R+r):
     for y in range(-R-r,R+r):
        xy_dist = math.sqrt(x**2 + y**2)
        if (xy_dist > 0):
           ringx = x / xy_dist * R # nearest point on major ring
           ringy = y / xy_dist * R
           ring_dist_sq = (x-ringx)**2 + (y-ringy)**2

           for z in range(-R-r,R+r):
               if (ring_dist_sq + z**2 <= r**2):
                  mc.setBlock(mcx+x, mcy+z, mcz+y, mcblock, mcmeta)

mc = minecraft.Minecraft.create(server.address)

playerPos = mc.player.getPos()

draw_donut(playerPos.x, playerPos.y + 9, playerPos.z, 18, 9, block.GLASS, 0)
mc.postToChat("Glass donut done")
draw_donut(playerPos.x, playerPos.y + 9, playerPos.z, 18, 6, block.WATER, 0)
mc.postToChat("Water donut done")

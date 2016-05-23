#!/usr/bin/env python

import mcpi.minecraft as minecraft
import mcpi.block as block
import server
import math

def draw_horizontal_disc(cx, cy, cz, radius, block_type, meta):
  for x in range(-radius, radius):
    for z in range(-radius, radius):
      if (x**2 + z**2 <= radius**2):
         mc.setBlock(cx + x, cy, cz + z, block_type, meta)

def draw_spiral(mcx,mcy,mcz,major_radius,minor_radius,height,period,phase,block_type,meta):
  for y in range(0,height - 1):
    theta = math.pi * 2 * y/period + phase
    circle_center_x = mcx + major_radius*math.cos(theta)
    circle_center_z = mcz + major_radius*math.sin(theta)
    draw_horizontal_disc(circle_center_x, mcy + y, circle_center_z, minor_radius, block_type, meta)

mc = minecraft.Minecraft.create(server.address)

playerPos = mc.player.getPos()

draw_spiral(playerPos.x, playerPos.y, playerPos.z, 18, 10, 200, 30, 0, block.GOLD_BLOCK, 0)
draw_spiral(playerPos.x, playerPos.y, playerPos.z, 18, 10, 200, 30, math.pi, block.GOLD_BLOCK, 0)
mc.postToChat("Spiral done")                                                                              

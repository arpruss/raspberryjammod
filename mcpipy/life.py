#
# Conway's Game of Life
# Copyright (c) 2015 Alexander R. Pruss
# MIT License
#
# life.py [size [fraction]
# 
# Default size: 50
# If fraction is omitted, you can draw whatever you like. Otherwise, the specified fraction is used.
# E.g., 
#    life.py 100 0.2
# will draw a 100x100 square, and fill in 20% of the cells.

from mine import *
from time import sleep
from random import random
import sys

def evolve(board):
    height = len(board)
    width = len(board[0])
    newBoard = [[False for i in range(width)] for j in range(height)]
    for row in range(height):
        for col in range(width):
            liveNeighbors = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if row+i >= 0 and row+i < height and col+j >= 0 and col+j < width and (i != 0 or j != 0) and board[row+i][col+j]:
                        liveNeighbors += 1
            if liveNeighbors == 3:
                newBoard[row][col] = True
            elif board[row][col] and liveNeighbors == 2:
                newBoard[row][col] = True
    return newBoard

def border(mc,x0,y0,z0,width,height,block=block.STONE):
    mc.setBlocks(x0-1,y0,z0-1,x0+width,y0,z0-1,block)
    mc.setBlocks(x0-1,y0,z0+height,x0+width,y0,z0+height,block)
    mc.setBlocks(x0-1,y0,z0,x0-1,y0,z0+height-1,block)
    mc.setBlocks(x0+width,y0,z0,x0+width,y0,z0+height-1,block)

def draw(mc,x0,y0,z0,width,height,oldBoard,newBoard,full,empty):
    for row in range(height):
       for col in range(width):
          if oldBoard == None or oldBoard[row][col] != newBoard[row][col]:
             mc.setBlock(x0+col,y0,z0+row,full if newBoard[row][col] else empty)


def life(mc,x0,y0,z0,width,height,empty=block.AIR,full=block.GOLD_BLOCK,delay=0.5,board=None):
    generation = 0
    if board == None:
        board = [[False for i in range(width)] for j in range(height)]
        blocks = mc.getBlocks(x0,y0,z0,x0+width-1,y0,z0+height-1)
        for row in range(height):
            for col in range(width):
                if blocks[col*width+row] != block.AIR.id:
                   board[row][col] = True
        draw(mc,x0,y0,z0,width,height,None,board,full,empty)

    while True:
       if generation % 10 == 0:
           mc.postToChat("Generation %d" % generation)
       sleep(delay)
       newBoard = evolve(board)
       draw(mc,x0,y0,z0,width,height,board,newBoard,full,empty)
       board = newBoard
       generation += 1

if __name__=='__main__':
    mc = Minecraft()
    pos = mc.player.getTilePos();
    x0 = pos.x-25
    y0 = pos.y
    z0 = pos.z-25
    if len(sys.argv) >= 2:
        width = int(sys.argv[1])
        height = width
    else:
        width = 50
        height = 50
    border(mc,x0,y0,z0,width,height)
    if len(sys.argv) >= 3:
        p = float(sys.argv[2])
        mc.postToChat("Occupied fraction: %.3f" % p)
        for row in range(height):
            for col in range(width):
                mc.setBlock(x0+col,y0,z0+row,block.GOLD_BLOCK if random() < p else block.AIR)
    else:
        mc.postToChat("Set up board and right click with sword when ready to go")
        mc.events.clearAll()
        while not mc.events.pollBlockHits():
            sleep(0.1)
    life(mc,x0,y0,z0,width,height)

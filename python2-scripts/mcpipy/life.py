from mc import *
from time import sleep

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

def life(mc,x0,y0,z0,width,height,empty=AIR,full=GOLD_BLOCK,border=STONE,delay=1.):
    mc.setBlocks(x0-1,y0,z0-1,x0+width,y0,z0-1,border)
    mc.setBlocks(x0-1,y0,z0+height,x0+width,y0,z0+height,border)
    mc.setBlocks(x0-1,y0,z0-1,x0-1,y0,z0+height,border)
    mc.setBlocks(x0+width,y0,z0-1,x0+width,y0,z0+height,border)
    board = [[False for i in range(width)] for j in range(height)]
    for row in range(height):
        for col in range(width):
            if mc.getBlock(x0+col,y0,z0+row) != AIR.id:
               board[row][col] = True

    while True:
       for row in range(height):
          for col in range(width):
              mc.setBlock(x0+col,y0,z0+row,full if board[row][col] else empty)
       board = evolve(board)
       sleep(delay)

mc = Minecraft()
pos = mc.player.getTilePos();
life(mc,pos.x-25,pos.y,pos.z-25,50,50)

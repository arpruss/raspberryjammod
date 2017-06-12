from mine import *
from board2d import Board2D
from time import sleep
from random import randint
import input

width = 30
height = 20
mc = Minecraft()
board = Board2D(mc, width, height)
board.fill(block.AIR)

vx = 1
vy = 0
x = width // 2
y = height // 2
length = 3
tail = []

def newGold():
    while True:
        x = randint(0, width-1)
        y = randint(0, height-1)
        if board.getBlock(x,y) == block.AIR:
            board.setBlock(x,y, block.GOLD_BLOCK)
            return

newGold()

while True:
    if x < 0 or x >= width or y < 0 or y >= height or (x,y) in tail:
        board.setBlock(x, y, block.WOOL_RED)        
        board.draw()
        mc.postToChat("Game over")
        break
    tail.append((x,y))
    if len(tail) > length:
        board.setBlock(tail[0], block.AIR)
        del tail[0]
    if board.getBlock(x,y) == block.GOLD_BLOCK:
        length += 1
        newGold()
    board.setBlock(x, y, block.BRICK_BLOCK)        
    board.draw()
    sleep(0.05+1.5/length)
    if input.wasPressedSinceLast(input.UP):
        vy = 1
        vx = 0
    elif input.wasPressedSinceLast(input.DOWN):
        vy = -1
        vx = 0
    elif input.wasPressedSinceLast(input.LEFT):
        vy = 0
        vx = -1
    elif input.wasPressedSinceLast(input.RIGHT):
        vy = 0
        vx = 1
    x += vx
    y += vy

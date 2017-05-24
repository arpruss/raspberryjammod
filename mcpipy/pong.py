from mine import *
from board2d import Board2D
from time import sleep
import input
import random

paddleHeight = 5
width = 40
statusY = 30
statusSize = 11
boardHeight = statusY + statusSize

maxLeftSpeed = 1
maxRightSpeed = 0.35

leftPaddleY = statusY // 2
rightPaddleY = statusY // 2
rightPaddleX = width - 2
leftPaddleX = 1
leftScore = 0
rightScore = 0

mc = Minecraft()
board = Board2D(mc, width, boardHeight, distance=20)

lastMove = -1
redraw = True

ballX = width // 2
ballY = statusY // 2

ball = board.spawnEntity("chicken", ballX, ballY)

while True:
    board.setBlocks(1,1,width-2,statusY-1, block.AIR) 
    board.line(0, statusY, 0, 0, block.WOOL_BLACK)
    board.line(width-1, 0, width-1, statusY, block.WOOL_BLACK)
    board.line(0, statusY, width-1, statusY, block.WOOL_BLACK)
    board.line(0, 0, width-1, 0, block.WOOL_BLACK)
    board.text(width//4, statusY+2, str(leftScore), foreground=block.WOOL_BLACK, background=block.AIR, center=True)                
    board.text(width-width//4, statusY+2, str(rightScore), foreground=block.WOOL_BLACK, background=block.AIR, center=True)            
    board.setBlocks(leftPaddleX, leftPaddleY-paddleHeight//2, leftPaddleX, leftPaddleY+paddleHeight//2, block.WOOL_WHITE)
    board.setBlocks(rightPaddleX, rightPaddleY-paddleHeight//2, rightPaddleX, rightPaddleY+paddleHeight//2, block.WOOL_WHITE)
    ballX = width // 2
    ballY = statusY // 2
    board.entitySetPos(ball, ballX, ballY)
    vX = 0.85 * random.choice([-1,1])
    vY = 0.85 * random.choice([-1,1])
    board.draw()
    if leftScore >= 2 or rightScore >= 2:
        break
    sleep(2)

    while True:
        if input.isPressedNow(input.UP) and leftPaddleY < statusY-1:
            leftPaddleY += maxLeftSpeed
        if input.isPressedNow(input.DOWN) and leftPaddleY > 0:
            leftPaddleY -= maxLeftSpeed
        if vX > 0:
            predictY = (ballY - 1 + vY/vX*(width-2-ballX)) % (2*(statusY-1)) + 1
            if predictY > statusY-1:
                predictY = 2*(statusY-1) - (predictY - 1) + 1
            if abs(predictY-rightPaddleY) >= 1:
                if rightPaddleY < predictY:
                    rightPaddleY += maxRightSpeed
                elif rightPaddleY > predictY:
                    rightPaddleY -= maxRightSpeed

        leftPaddleY = min(max(leftPaddleY, 1+paddleHeight//2), statusY-1-paddleHeight//2)
        rightPaddleY = min(max(rightPaddleY, 1+paddleHeight//2), statusY-1-paddleHeight//2)

        if ballY <= 1.5:
            vY = abs(vY)
        elif ballY >= statusY-0.5:
            vY = -abs(vY)
            
        ballX = ballX + vX
        ballY = ballY + vY
        
        board.setBlocks(1,1,1,statusY-1, block.AIR) 
        board.setBlocks(width-2,1,width-2,statusY-1, block.AIR) 
        board.setBlocks(leftPaddleX, leftPaddleY-paddleHeight//2, leftPaddleX, leftPaddleY+paddleHeight//2, block.WOOL_WHITE)
        board.setBlocks(rightPaddleX, rightPaddleY-paddleHeight//2, rightPaddleX, rightPaddleY+paddleHeight//2, block.WOOL_WHITE)
        board.entitySetPos(ball, ballX, ballY)
        board.draw()
        
        if ballX <= leftPaddleX + 0.5:
            if abs(ballY-floor(leftPaddleY)) <= paddleHeight * 0.5:
                vX = abs(vX)
            else:
                rightScore += 1
                break
        if ballX >= rightPaddleX - 0.5:
            if abs(ballY-floor(rightPaddleY)) <= paddleHeight * 0.5:
                vX = -abs(vX)
            else:
                leftScore += 1
                break

        sleep(.1)

board.text(width//2, statusY//2, "Game", center=True)
board.text(width//2, statusY//2-11, "Over", center=True)
board.draw()
board.stop()

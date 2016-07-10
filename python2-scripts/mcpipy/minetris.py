#
# requires Windows (for input.py to work)
# Copyright (c) 2016 Alexander Pruss. MIT License.
#

#
# Make sure to have input.py and text.py in the same directory.
#


from mc import *
from time import sleep,time
from random import randint
import input
import text
from fonts import FONTS

FONT = 'thin9pt' #metrix7pt
HEIGHT = 20
WIDTH = 10
BORDER = WOOL_BLACK
BACKGROUND = STAINED_GLASS_BLACK

DELAYS = ( 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05)

PIECES = (  (('XXXX',), ('.X','.X','.X','.X')),
            (('XX','XX'),),
            (('XXX', '..X'), ('.X', '.X', 'XX'), ('X','XXX'), ('XX', 'X', 'X')),
            (('XXX', 'X'), ('XX', '.X', '.X'), ('..X', 'XXX'), ('X.', 'X.', 'XX')),
            (('XX', '.XX'), ('.X','XX', 'X.')),
            (('.XX', 'XX'), ('X.', 'XX', '.X')) )

def inputMoveDown():
    return input.wasPressedSinceLast(input.DOWN)
    
def inputMoveLeft():
    return input.wasPressedSinceLast(input.LEFT)
    
def inputMoveRight():
    return input.wasPressedSinceLast(input.RIGHT)

def inputRotateLeft():
    return input.wasPressedSinceLast(input.PRIOR)
    
def inputRotateRight():
    return input.wasPressedSinceLast(input.NEXT)
                
def inputNext():
    return input.wasPressedSinceLast(ord('N'))
    
def inputLevelUp():
    return input.wasPressedSinceLast(ord('L'))
    
def inputPause():
    return input.wasPressedSinceLast(ord('P'))
    
def answerYes():
    input.clearPressBuffer(ord('Y'))
    input.clearPressBuffer(ord('N'))
    while True:
        if input.wasPressedSinceLast(ord('Y')):
            return True
        if input.wasPressedSinceLast(ord('N')):
            return False
        sleep(0.1)

def clearInput():
    for k in (input.DOWN, input.LEFT, input.RIGHT,
                input.PRIOR, input.NEXT, input.UP,
                ord('N'), ord('L'), ord('P'), ord('Y')):
        input.clearPressBuffer(k)
    
def drawBoard():
    mc.setBlocks(left-1, bottom-1, plane, left+WIDTH, bottom-1, plane, BORDER)
    mc.setBlocks(left-1, bottom+HEIGHT, plane, left+WIDTH, bottom+HEIGHT, plane, BORDER)
    mc.setBlocks(left-1, bottom, plane, left, bottom+HEIGHT-1, plane, BORDER)
    mc.setBlocks(left+WIDTH, bottom, plane, left+WIDTH, bottom+HEIGHT-1, plane, BORDER)
    mc.setBlocks(left-1, bottom-1, plane-1, left+WIDTH, bottom+HEIGHT, plane-1, BACKGROUND)
    mc.setBlocks(left, bottom, plane, left+WIDTH-1, bottom+HEIGHT-1, plane, AIR)
    
def pieceWidth(piece):
    return max((len(a) for a in piece))
    
def enumeratePiece(x, y, piece):
    for row in range(len(piece)):
        if y-row < HEIGHT:
            for col in range(len(piece[row])):
                if piece[row][col] == 'X':
                    yield (x+col,y-row)

def movePiece(oldX, oldY, oldPiece, x, y, piece, color):
    new = set(enumeratePiece(x, y, piece))
    if oldPiece:
        old = set(enumeratePiece(oldX, oldY, oldPiece))
        
        for (x,y) in old-new:
            mc.setBlock(x+left, y+bottom, plane, AIR)

        new = new - old

    for (x,y) in new:
        mc.setBlock(x+left, y+bottom, plane, color)

def eraseNext():
    mc.setBlocks(left+WIDTH+2,bottom+3,plane,left+WIDTH+2+3,bottom+6,plane,AIR)
        
def drawNext():
    eraseNext()
    for (x,y) in enumeratePiece(WIDTH+2, 6, nextFamily[nextOrientation]):
        mc.setBlock(x+left, y+bottom, plane, nextColor)
        
def drawBuffer(buffer):
    for x,y in buffer:
        mc.setBlock(x,y,plane,buffer[(x,y)])

def makeNext():
    global nextFamily, nextColor, nextOrientation
    n = randint(0, len(PIECES)-1)
    nextFamily = PIECES[n]
    nextColor = Block(WOOL.id, (n+1) % 16)
    nextOrientation = randint(0, len(nextFamily)-1)        
        
def placePiece():
    global color, family, orientation, descendDelay, droppedFrom, didShowNext
    family = nextFamily
    orientation = nextOrientation
    color = nextColor
    makeNext()
    piece = family[orientation]
    x = WIDTH // 2 - pieceWidth(piece)
    y = HEIGHT + len(piece) - 2
    descendDelay = currentDescendDelay
    droppedFrom = None
    didShowNext = showNext
    if showNext:
        drawNext()
    return (x,y)
    
def fit(x, y, piece):
    for (xx,yy) in enumeratePiece(x, y, piece):
        if yy < 0 or xx >= WIDTH or xx < 0 or board[xx][yy] is not None:
            return False
    return True                    
                    
def descend():
    global descendTimer
    if descendTimer + descendDelay <= time():
        descendTimer += descendDelay
        return True
    return False

def hide():
    mc.setBlocks(left, bottom, plane, left+WIDTH-1, bottom+HEIGHT-1, plane, GLASS)
    text.drawText(mc, FONTS['nicefontbold'], 
                    Vec3(left+WIDTH//2,bottom+5,plane), 
                    Vec3(1,0,0), Vec3(0,1,0), 
                    "P", SEA_LANTERN, align=text.ALIGN_CENTER)

    
def restore(x, y):
    for xx in range(WIDTH):
        for yy in range(HEIGHT):
            mc.setBlock(xx+left,yy+bottom,plane,board[xx][yy] or AIR)
    movePiece(None, None, None, x, y, family[orientation], color)
    
def addPiece(x, y, piece, color):
    global score,level,totalDropped
    
    for (xx,yy) in enumeratePiece(x, y, piece):
        board[xx][yy] = color
        
    dropCount = 0
    while True:
        foundRow = False
        for y in range(HEIGHT):
            full = True
            for x in range(WIDTH):
                if board[x][y] is None:
                    full = False
                    break
            if full:
                dropCount += 1
                foundRow = True
                for y2 in range(y, HEIGHT-1):
                    for x in range(WIDTH):
                        b = board[x][y2+1]
                        board[x][y2] = b
                        mc.setBlock(left+x,bottom+y2,plane,b if b is not None else AIR)
                for x in range(WIDTH):
                    board[x][HEIGHT-1] = None
                    mc.setBlock(left+x,bottom+HEIGHT-1,plane,AIR)
                
        if not foundRow:
            break
            
    if didShowNext:
        score += 3 + (3*(level-1))//2 + droppedFrom
    else:
        score += 5 + 2*(level-1) + droppedFrom
    if dropCount:
        totalDropped += dropCount
        level = 1 + totalDropped // 10 + extraLevels
    updateScoreAndLevel()

def updateText(buffer,x,y,s,align):
    newBuffer = {}
    if s is not None:
        text.drawText(mc, FONTS['thin9pt'], 
                        Vec3(x,y,plane), 
                        Vec3(1,0,0), Vec3(0,1,0), 
                        s, SEA_LANTERN, background=None, align=align, buffer=newBuffer)
    for pos in buffer:
        if pos not in newBuffer:
            mc.setBlock(pos, AIR)
    for pos in newBuffer:
        if pos not in buffer:
            mc.setBlock(pos, SEA_LANTERN)
    return newBuffer        
        
def updateScoreAndLevel():
    global scoreBuffer, levelBuffer, currentDescendDelay, level
    if level > 10:
        level = 10
    scoreBuffer = updateText(scoreBuffer,left+WIDTH+2,bottom+HEIGHT-10,str(score),text.ALIGN_LEFT)
    levelBuffer = updateText(levelBuffer,left-1,bottom+HEIGHT-10,str(level),text.ALIGN_RIGHT)
    currentDescendDelay = DELAYS[level-1]

def clearScoreAndLevel():
    global scoreBuffer, levelBuffer, currentDescendDelay, level
    scoreBuffer = updateText(scoreBuffer,left+WIDTH+2,bottom+HEIGHT-10,None,text.ALIGN_LEFT)
    levelBuffer = updateText(levelBuffer,left-1,bottom+HEIGHT-10,None,text.ALIGN_RIGHT)

def game():
    global score, level, extraLevels, totalDropped, scoreBuffer, levelBuffer, showNext, didShowNext
    global orientation, board, descendTimer, droppedFrom, descendDelay
    
    board = [[None for i in range(HEIGHT)] for j in range(WIDTH)]

    drawBoard()
    score = 0
    level = 1
    extraLevels = 0
    totalDropped = 0
    scoreBuffer = {}
    levelBuffer = {}
    showNext = False
    updateScoreAndLevel()
    makeNext()

    newPiece = True

    while True:
        if newPiece:
            x,y = placePiece()
            oldPiece = None
            if not fit(x, y, family[orientation]):
                break
            draw = True
            newPiece = False
            fall = False
            clearInput()
            descendTimer = time()
        else:
            oldPiece = family[orientation]
            draw = False
        oldX = x
        oldY = y
        
        if inputPause():
            t0 = time()
            hide()
            while not inputPause():
                sleep(0.025)
            clearInput()
            restore(x, y)
            descendTimer += time() - t0

        if not fall:
            if inputLevelUp():
                extraLevels += 1
                level += 1
                updateScoreAndLevel()
                descendDelay = currentDescendDelay
        
            if inputMoveLeft() and fit(x-1, y, family[orientation]):
                x -= 1
                draw = True
                    
            if inputMoveRight() and fit(x+1, y, family[orientation]):
                x += 1
                draw = True
                    
            if inputRotateLeft() and fit(x, y, family[(orientation-1)%len(family)]):
                orientation = (orientation-1)%len(family)
                draw = True
                    
            if inputRotateRight() and fit(x, y, family[(orientation+1)%len(family)]):
                orientation = (orientation+1)%len(family)
                draw = True
                
            if inputMoveDown():
                fall = True
                droppedFrom = y+1-len(family[orientation]) 
                descendDelay = 0.05
                
            if inputNext():
                showNext = not showNext
                if showNext:
                    didShowNext = True
                    drawNext()
                else:
                    eraseNext()
            
        if descend():
            if not fit(x, y-1, family[orientation]):
                if droppedFrom is None:
                    droppedFrom = y+1-len(family[orientation])
                addPiece(x, y, family[orientation], color)
                newPiece = True
            else:
                draw = True
                y -= 1

        if draw:
            movePiece(oldX, oldY, oldPiece, x, y, family[orientation], color)
            
        sleep(0.025)

    return score
    
mc = Minecraft()

mc.postToChat("Left/Right arrow: move")
mc.postToChat("Up: rotate right")
mc.postToChat("PageUp/PageDown: rotate left/right")
mc.postToChat("N: toggle view next")
mc.postToChat("P: pause")
mc.postToChat("L: next level")

playerPos = mc.player.getTilePos()
mc.player.setRotation(180)
mc.player.setPitch(-26)
mc.player.setTilePos(playerPos.x, playerPos.y, playerPos.z + 14)

left = playerPos.x - WIDTH // 2
plane = playerPos.z
bottom = playerPos.y + 1

while True:
    s = game()
    mc.postToChat("Game Over: You got %d points" % s)
    mc.postToChat("Play again? (Y/N)")
    if not answerYes():
        mc.postToChat("Goodbye!")
        break
    clearScoreAndLevel()
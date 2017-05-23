#
# requires Windows (for input.py to work)
#
# Code by Alexander Pruss and under the MIT license
#

#
# Make sure to have input.py and text.py in the same directory.
#


from mine import *
from time import sleep,time
from random import randint
import input
import text
from fonts import FONTS

FONT = 'thin9pt' #metrix7pt
HEIGHT = 20
WIDTH = 10
BORDER = block.WOOL_BLACK
BACKGROUND = block.STAINED_GLASS_BLACK
DISTANCE = 14

DELAYS = ( 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05)

# arrange so width >= height
PIECES = (  ('XXXX',), 
            ('XX','XX'),
            ('XXX', '..X'), 
            ('XXX', 'X'), 
            ('XX', '.XX'), 
            ('.XX', 'XX'))
            
class PieceState(object):
    def __init__(self, piece, rotation, color):
        self.piece = piece
        self.rotation = rotation % 4
        self.color = color
        self.width = max((len(a) for a in self.piece))
        self.height = len(piece)
        
    def getWidth(self):
        if self.rotation % 2 == 0:
            return self.width
        else:
            return self.height

    def getHeight(self):
        if self.rotation % 2 == 0:
            return self.height
        else:
            return self.width

    def getCoordinates(self, x, y):
        if self.rotation % 2:
            dcol = (self.width-self.height)//2

        for row in range(self.height):
            for col in range(len(self.piece[row])):
                if self.piece[row][col] == 'X':
                    if self.rotation == 0:
                        xx = col
                        yy = row
                    elif self.rotation == 2:
                        xx = self.width-1-col
                        yy = self.height-1-row
                    elif self.rotation == 3:
                        xx = dcol+row
                        yy = self.width-1-col
                    elif self.rotation == 1:
                        xx = dcol+self.height-1-row
                        yy = col

                    if y-yy < HEIGHT:
                        yield (x+xx,y-yy)
                        
    def fit(self, x, y, board):
        for (xx,yy) in self.getCoordinates(x, y):
            if yy < 0 or xx >= WIDTH or xx < 0 or board[xx][yy] is not None:
                return False
        return True                    

    def cloneRotated(self, delta):
        return PieceState(self.piece, self.rotation+delta, self.color)

def inputMoveDown():
    return input.wasPressedSinceLast(input.DOWN)
    
def inputMoveLeft():
    return input.wasPressedSinceLast(input.LEFT)
    
def inputMoveRight():
    return input.wasPressedSinceLast(input.RIGHT)

def inputRotateLeft():
    return input.wasPressedSinceLast(input.PRIOR)
    
def inputRotateRight():
    return input.wasPressedSinceLast(input.NEXT) or input.wasPressedSinceLast(input.UP)
                
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
#    mc.setBlocks(left, bottom, plane, left+WIDTH-1, bottom+HEIGHT-1, plane, AIR)
    mc.setBlocks(left, bottom, plane, left+WIDTH-1, bottom+HEIGHT-1, plane+DISTANCE, block.AIR)
    
def movePiece(oldX, oldY, oldPieceState, x, y, pieceState):
    new = set(pieceState.getCoordinates(x, y))
    if oldPieceState:
        old = set(oldPieceState.getCoordinates(oldX, oldY))
        
        for (x,y) in old-new:
            mc.setBlock(x+left, y+bottom, plane, block.AIR)

        new = new - old

    for (x,y) in new:
        mc.setBlock(x+left, y+bottom, plane, pieceState.color)

def eraseNext():
    mc.setBlocks(left+WIDTH+2,bottom+3,plane,left+WIDTH+2+3,bottom+6,plane,block.AIR)
        
def drawNext(nextPieceState):
    eraseNext()
    for (x,y) in nextPieceState.getCoordinates(WIDTH+2, 6):
        mc.setBlock(x+left, y+bottom, plane, nextPieceState.color)
        
def makePieceState():
    n = randint(0, len(PIECES)-1)
    return PieceState(PIECES[n], randint(0,3), Block(block.WOOL.id, (n+1) % 16))
        
def placePiece(state, nextPieceState):
    global descendDelay, droppedFrom, didShowNext
    x = WIDTH // 2 - state.getWidth()
    y = HEIGHT + state.getHeight() - 2
    descendDelay = currentDescendDelay
    droppedFrom = None
    didShowNext = showNext
    if showNext:
        drawNext(nextPieceState)
    return (x,y)
    
def descend():
    global descendTimer
    if descendTimer + descendDelay <= time():
        descendTimer += descendDelay
        return True
    return False

def hide():
    mc.setBlocks(left, bottom, plane, left+WIDTH-1, bottom+HEIGHT-1, plane, block.GLASS)
    text.drawText(mc, FONTS['nicefontbold'], 
                    Vec3(left+WIDTH//2,bottom+5,plane), 
                    Vec3(1,0,0), Vec3(0,1,0), 
                    "P", block.SEA_LANTERN, align=text.ALIGN_CENTER)
    
def restore(x, y, curPieceState):
    for xx in range(WIDTH):
        for yy in range(HEIGHT):
            mc.setBlock(xx+left,yy+bottom,plane,board[xx][yy] or block.AIR)
    movePiece(None, None, None, x, y, curPieceState)
    
def addPiece(x, y, curPieceState):
    global score,level,totalDropped
    
    for (xx,yy) in curPieceState.getCoordinates(x, y):
        board[xx][yy] = curPieceState.color
        
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
                        mc.setBlock(left+x,bottom+y2,plane,b if b is not None else block.AIR)
                for x in range(WIDTH):
                    board[x][HEIGHT-1] = None
                    mc.setBlock(left+x,bottom+HEIGHT-1,plane,block.AIR)
                
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
                        s, block.SEA_LANTERN, background=None, align=align, buffer=newBuffer)
    for pos in buffer:
        if pos not in newBuffer:
            mc.setBlock(pos, block.AIR)
    for pos in newBuffer:
        if pos not in buffer:
            mc.setBlock(pos, block.SEA_LANTERN)
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
    global board, descendTimer, droppedFrom, descendDelay
    
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
    nextPieceState = makePieceState()

    newPiece = True

    while True:
        if newPiece:
            curPieceState = nextPieceState
            nextPieceState = makePieceState()
            x,y = placePiece(curPieceState, nextPieceState)
            oldPieceState = None
            if not curPieceState.fit(x, y, board):
                break
            draw = True
            newPiece = False
            fall = False
            clearInput()
            descendTimer = time()
        else:
            oldPieceState = curPieceState.cloneRotated(0)
            draw = False
        oldX = x
        oldY = y
        
        if inputPause():
            t0 = time()
            hide()
            while not inputPause():
                sleep(0.025)
            clearInput()
            restore(x, y, curPieceState)
            descendTimer += time() - t0

        if not fall:
            if inputLevelUp():
                extraLevels += 1
                level += 1
                updateScoreAndLevel()
                descendDelay = currentDescendDelay
        
            if inputMoveLeft() and curPieceState.fit(x-1, y, board):
                x -= 1
                draw = True
                    
            if inputMoveRight() and curPieceState.fit(x+1, y, board):
                x += 1
                draw = True
                    
            if inputRotateLeft():
                p = curPieceState.cloneRotated(-1)
                if p.fit(x, y, board):
                    curPieceState = p
                    draw = True
                    
            if inputRotateRight():
                p = curPieceState.cloneRotated(1)
                if p.fit(x, y, board):
                    curPieceState = p
                    draw = True
                
            if inputMoveDown():
                fall = True
                droppedFrom = y+1-curPieceState.getHeight() 
                descendDelay = 0.05
                
            if inputNext():
                showNext = not showNext
                if showNext:
                    didShowNext = True
                    drawNext(nextPieceState)
                else:
                    eraseNext()
            
        if descend():
            if not curPieceState.fit(x, y-1, board):
                if droppedFrom is None:
                    droppedFrom = y+1-curPieceState.getHeight()
                addPiece(x, y, curPieceState)
                newPiece = True
            else:
                draw = True
                y -= 1

        if draw:
            movePiece(oldX, oldY, oldPieceState, x, y, curPieceState)
            
        sleep(0.025)

    return score
    
if __name__=="__main__":
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
    mc.player.setTilePos(playerPos.x, playerPos.y, playerPos.z)

    left = playerPos.x - WIDTH // 2
    plane = playerPos.z - DISTANCE
    bottom = playerPos.y + 1

    while True:
        s = game()
        mc.postToChat("Game Over: You got %d points" % s)
        mc.postToChat("Play again? (Y/N)")
        if not answerYes():
            mc.postToChat("Goodbye!")
            break
        clearScoreAndLevel()
        
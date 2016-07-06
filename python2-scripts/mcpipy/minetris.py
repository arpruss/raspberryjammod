#
# requires Windows and pywin32
#
from mc import *
from time import sleep,time
from random import randint
import win32con,win32api

HEIGHT = 22
WIDTH = 9
BORDER = WOOL_BLACK
BACKGROUND = STAINED_GLASS_BLACK

PIECES = (  (('XXXX',), ('.X','.X','.X','.X')),
			(('XX','XX'),),
			(('XXX', '..X'), ('.X', '.X', 'XX'), ('X','XXX'), ('XX', 'X', 'X')),
			(('XXX', 'X'), ('XX', '.X', '.X'), ('..X', 'XXX'), ('X.', 'X.', 'XX')),
			(('XX', '.XX'), ('.X','XX', 'X.')),
			(('.XX', 'XX'), ('X.', 'XX', '.X')) )

def drawBoard():
	mc.setBlocks(left-1, bottom-1, plane, left+WIDTH, bottom-1, plane, BORDER)
	mc.setBlocks(left-1, bottom+HEIGHT, plane, left+WIDTH, bottom+HEIGHT, plane, BORDER)
	mc.setBlocks(left-1, bottom, plane, left, bottom+HEIGHT-1, plane, BORDER)
	mc.setBlocks(left+WIDTH, bottom, plane, left+WIDTH, bottom+HEIGHT-1, plane, BORDER)
	mc.setBlocks(left-1, bottom-1, plane-1, left+WIDTH, bottom+HEIGHT, plane-1, BACKGROUND)
	mc.setBlocks(left, bottom, plane, left+WIDTH-1, bottom+HEIGHT-1, plane, AIR)
	
def pieceWidth(piece):
	return max((len(a) for a in piece[orientation]))
	
def enumeratePiece(x, y, piece):
	for row in range(len(piece)):
		for col in range(len(piece[row])):
			if piece[row][col] == 'X':
				yield (x+col,y-row)
	
def erasePiece(buffer, x, y, piece):
	for (xx,yy) in enumeratePiece(x,y, piece):
		buffer[(left+xx,bottom+yy)] = AIR

def drawPiece(buffer, x, y, piece, color):
	for (xx,yy) in enumeratePiece(x,y, piece):
		if (left+xx,bottom+yy) in buffer and buffer[(left+xx,bottom+yy)] == AIR:
			del buffer[(left+xx,bottom+yy)]
		else:
			buffer[(left+xx,bottom+yy)] = color
				
def drawBuffer(buffer):
	for x,y in buffer:
		mc.setBlock(x,y,plane,buffer[(x,y)])

def placePiece():
	global pieceNum, color, family, orientation, x, y, fall, descendDelay
	pieceNum = randint(0, len(PIECES)-1)
	color = Block(WOOL.id, (pieceNum+1) % 16)
	family = PIECES[pieceNum]
	orientation = 0
	x = WIDTH // 2 - pieceWidth(family[orientation])
	y = HEIGHT - 1		
	descendDelay = currentDescendDelay
	fall = False
	
def fit(x, y, piece):
	for (xx,yy) in enumeratePiece(x, y, piece):
		if yy >= HEIGHT or yy < 0 or xx >= WIDTH or xx < 0 or board[xx][yy] is not None:
			return False
	return True
					
					
def descend():
	global descendTimer
	if descendTimer + descendDelay <= time():
		descendTimer += descendDelay
		return True
	return False
	
def moveDown():
	return (win32api.GetAsyncKeyState(win32con.VK_DOWN)&1)
	
def moveLeft():
	return (win32api.GetAsyncKeyState(win32con.VK_LEFT)&1)
	
def moveRight():
	return (win32api.GetAsyncKeyState(win32con.VK_RIGHT)&1)

def rotateLeft():
	return (win32api.GetAsyncKeyState(win32con.VK_PRIOR)&1)
	
def rotateRight():
	return (win32api.GetAsyncKeyState(win32con.VK_NEXT)&1) or (win32api.GetAsyncKeyState(win32con.VK_UP)&1)
	
def addPiece(x, y, piece, color):
	for (xx,yy) in enumeratePiece(x, y, piece):
		board[xx][yy] = color
	while True:
		foundRow = False
		for y in range(HEIGHT):
			full = True
			for x in range(WIDTH):
				if board[x][y] is None:
					full = False
					break
			if full:
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


mc = Minecraft()

playerPos = mc.player.getTilePos()
mc.player.setRotation(180)
mc.player.setPitch(-30)
mc.player.setTilePos(playerPos.x, playerPos.y, playerPos.z + 10)
left = playerPos.x - WIDTH // 2
plane = playerPos.z
bottom = playerPos.y + 1
board = [[None for i in range(HEIGHT)] for j in range(WIDTH)]
currentDescendDelay = 0.5

drawBoard()

newPiece = True

while True:
	if newPiece:
		placePiece()
		oldPiece = None
		if not fit(x, y, family[orientation]):
			mc.postToChat("Doesn't fit: End of game")
			print "no fit"
			break
		draw = True
		newPiece = False
		descendTimer = time()
	else:
		oldPiece = family[orientation]
		draw = False
	oldX = x
	oldY = y

	if not fall:
		if moveLeft() and fit(x-1, y, family[orientation]):
			x -= 1
			draw = True
				
		if moveRight() and fit(x+1, y, family[orientation]):
			x += 1
			draw = True
				
		if rotateLeft() and fit(x, y, family[(orientation-1)%len(family)]):
			orientation = (orientation-1)%len(family)
			draw = True
				
		if rotateRight() and fit(x, y, family[(orientation+1)%len(family)]):
			orientation = (orientation+1)%len(family)
			draw = True
			
		if moveDown():
			fall = True
			descendDelay = 0.05
		
	if descend():
		if not fit(x, y-1, family[orientation]):
			addPiece(x, y, family[orientation], color)
			newPiece = True
		else:
			draw = True
			y -= 1
	
	if draw:
		buffer = {}
		if oldPiece:
			erasePiece(buffer, oldX, oldY, oldPiece)
		drawPiece(buffer, x, y, family[orientation], color)
		drawBuffer(buffer)
		
	sleep(0.1)
	
print "done"	

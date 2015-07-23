#
# Chess interface for Thomas Ahle's sunfish engine
# Code by Alexander Pruss under the MIT license
#
#
# To work, this needs sunfish.py:
#   https://raw.githubusercontent.com/thomasahle/sunfish/master/sunfish.py
#

from collections import OrderedDict
from mc import *
from vehicle import *
from text import *
from fonts import *
import drawing
import time
import sys

LABEL_BLOCK = REDSTONE_BLOCK

try:
    import _sunfish as sunfish
except:
    try:
        import urllib2
        import os.path
        content = urllib2.urlopen("https://raw.githubusercontent.com/thomasahle/sunfish/master/sunfish.py").read()
        f=open(os.path.join(os.path.dirname(sys.argv[0]),"_sunfish.py"),"w")
        f.write("# From: https://raw.githubusercontent.com/thomasahle/sunfish/master/sunfish.py\n")
        f.write("# Covered by the GPL 2 license\n")
        f.write(content)
        f.close()
        import _sunfish as sunfish
    except:
        print "Failed download: You need sunfish.py for this script."

def getCoords(row,col):
    return (corner.x+8*row+4,corner.y,corner.z+8*col+4)

def toRowCol(n, black):
    row = 7 - ((n - 20) / 10)
    col = n % 10 - 1
    if black:
        col = 7 - col
        row = 7 - row
    return row,col

def toRowColMove(m, black):
    return toRowCol(m[0],black),toRowCol(m[1],black)

def toNumeric(rowCol,black):
    if black:
        col = 7 - rowCol[1]
        row = 7 - rowCol[0]
    else:
        row, col = rowCol 
    return 20 + 10 * (7-row) + 1 + col

def toNumericMove(rowColMove,black):
    return toNumeric(rowColMove[0],black),toNumeric(rowColMove[1],black)

def toAlgebraicMove(rowColMove):
    (r0,c0),(r1,c1) = rowColMove
    return 'abcdefgh'[c0]+str(r0+1)+'abcdefgh'[c1]+str(r1+1)

def drawSquare(row,col):
    block = OBSIDIAN if (col + row) % 2 == 0 else QUARTZ_BLOCK
    mc.setBlocks(corner.x+row*8,corner.y-1,corner.z+col*8,corner.x+row*8+7,corner.y-1,corner.z+col*8+7,block)

def highlightSquare(row,col):
    mc.setBlocks(corner.x+row*8,corner.y-1,corner.z+col*8,
                    corner.x+row*8+7,corner.y-1,corner.z+col*8,REDSTONE_BLOCK)
    mc.setBlocks(corner.x+row*8,corner.y-1,corner.z+col*8,
                    corner.x+row*8,corner.y-1,corner.z+col*8+7,REDSTONE_BLOCK)
    mc.setBlocks(corner.x+row*8+7,corner.y-1,corner.z+col*8,
                    corner.x+row*8+7,corner.y-1,corner.z+col*8+7,REDSTONE_BLOCK)
    mc.setBlocks(corner.x+row*8,corner.y-1,corner.z+col*8+7,
                    corner.x+row*8+7,corner.y-1,corner.z+col*8+7,REDSTONE_BLOCK)

def drawEmptyBoard():
    mc.setBlocks(corner.x,corner.y,corner.z,corner.x+63,corner.y+MAXHEIGHT,corner.z+63,0)
    for row in range(8):
        for col in range(8):
            drawSquare(row,col)
    for col in range(8):
        c = getCoords(-1,col)
        drawText(mc,FONTS['8x8'],Vec3(c[0]-4,corner.y-1,c[2]-4),Vec3(0,0,1),Vec3(1,0,0),"ABCDEFGH"[col],LABEL_BLOCK)
        c = getCoords(8,col)
        drawText(mc,FONTS['8x8'],Vec3(c[0]+4,corner.y-1,c[2]+4),Vec3(0,0,-1),Vec3(-1,0,0),"ABCDEFGH"[col],LABEL_BLOCK)
    for row in range(8):
        c = getCoords(row,-1)
        drawText(mc,FONTS['8x8'],Vec3(c[0]-4,corner.y-1,c[2]-4),Vec3(0,0,1),Vec3(1,0,0),str(row+1),LABEL_BLOCK)
        c = getCoords(row,8)
        drawText(mc,FONTS['8x8'],Vec3(c[0]+4,corner.y-1,c[2]+4),Vec3(0,0,-1),Vec3(-1,0,0),str(row+1),LABEL_BLOCK)

PAWN = (
    (".xx.",
     "xxxx",
     ".xx.",
     ".xx.",
     "xxxx"),
    (".xx.",
     "xxxx",
     ".xx.",
     ".xx.",
     "xxxx"))

KNIGHT = (
   ("...xx.",
    "..xxxx",
    ".xxxxx",
    "xxxx.x",
    ".xxx..",
    ".xxxx.",
    "xxxxxx"),
   ("...xx.",
    "..xxxx",
    ".xxxxx",
    "xxxx.x",
    ".xxx..",
    ".xxxx.",
    "xxxxxx")        
    )

BISHOP = (
          (".xx.",
           "xx.x",
           "x.xx",
           "xxxx",
           ".xx.",
           ".xx.",
           "xxxx"),
          (".xx.",
           "xx.x",
           "x.xx",
           "xxxx",
           ".xx.",
           ".xx.",
           "xxxx"))

ROOK = (
   ("x.xx.x",
    "x.xx.x",
    "xxxxxx",
    ".xxxx.",
    ".xxxx.",
    "xxxxxx"),
   ("x.xx.x",
    "x.xx.x",
    "xxxxxx",
    ".xxxx.",
    ".xxxx.",
    "xxxxxx"))

QUEEN = (
   ("..xx..",
    "x.xx.x",
    "x.xx.x",
    "xxxxxx",
    "xxxxxx",
    "xxxxxx",
    "xxxxxx"),
   ("..xx..",
    "x.xx.x",
    "x.xx.x",
    "xxxxxx",
    "xxxxxx",
    "xxxxxx",
    "xxxxxx"))

KING = (
   ("..xx..",
    "xxxxxx",
    "..xx..",
    "xxxxxx",
    "xxxxxx",
    ".xxxx.",
    "xxxxxx"),
   ("..xx..",
    "xxxxxx",
    "..xx..",
    "xxxxxx",
    "xxxxxx",
    ".xxxx.",
    "xxxxxx"))

BLACK = WOOL_GRAY
WHITE = WOOL_WHITE

pieceBitmaps = {
    'P':PAWN,
    'N':KNIGHT,
    'B':BISHOP,
    'R':ROOK,
    'Q':QUEEN,
    'K':KING
    }

MAXHEIGHT = 8

def toVehicle(bitmaps,block,piece):
    dict = {}
    depth = len(bitmaps)
    height = len(bitmaps[0])
    width = len(bitmaps[0][0])
    for plane in range(depth):
        x = plane-depth/2
        for row in range(height):
            y = row
            for col in range(width):
                z = col-width/2
                if bitmaps[plane][height-1-row][col] == 'x':
                    dict[(x,y,z)] = block
    v = Vehicle(mc,True)
    v.setVehicle(dict)
    v.name = piece
    return v

def animateMovePiece(start,stop):
    a = getCoords(start[0],start[1])
    b = getCoords(stop[0],stop[1])
    piece = pieces[start]
    if not fast:
        line = drawing.getLine(a[0],a[1],a[2],b[0],b[1],b[2])
        for point in line[1:]:
            piece.moveTo(point[0],point[1],point[2])
            time.sleep(0.1)
    piece.moveTo(b[0],b[1],b[2])
    del pieces[start]
    pieces[stop] = piece

def parse(message):
    try:
        if len(message) != 4:
            raise ValueError
        col0 = ord(message[0].lower()) - ord('a')
        if col0 < 0 or col0 > 7:
            raise ValueError
        row0 = ord(message[1]) - ord('1')
        if row0 < 0 or row0 > 7:
            raise ValueError
        col1 = ord(message[2].lower()) - ord('a')
        if col1 < 0 or col1 > 7:
            raise ValueError
        row1 = ord(message[3]) - ord('1')
        if row1 < 0 or row1 > 7:
            raise ValueError
        return (row0,col0),(row1,col1)
    except:
        raise ValueError
        
def getPiece(row,col):
    try:
        return pieces[(row,col)].name
    except KeyError:
        return None

def inputMove():
    moves = []
    mc.events.clearAll()
    while len(moves) < 2:
        try:
            chats = mc.events.pollChatPosts()
            move = parse(chats[0].message)
            for m in moves:
                drawSquare(m[0],m[1])
            return move
        except:
            pass
        hits = mc.events.pollBlockHits()
        if len(hits) > 0:
            c = hits[0].pos
            if ( corner.x <= c.x and corner.y -1 <= c.y and corner.z <= c.z and
                 c.x < corner.x + 64 and c.y < corner.y + MAXHEIGHT and c.z < corner.z + 64 ):
                m = (c.x - corner.x) / 8, (c.z - corner.z) /8
                if len(moves) == 0 or m[0] != moves[0][0] or m[1] != moves[0][1]:
                    highlightSquare(m[0],m[1])
                    moves.append(m)
                    time.sleep(0.2)
                    mc.events.clearAll() # debounce
                    continue
            for m in moves:
                drawSquare(m[0],m[1])
            moves = []
            mc.postToChat('Canceled. Enter another move.')
            time.sleep(0.2)
            mc.events.clearAll() # debounce
        time.sleep(0.2)
    for m in moves:
        drawSquare(m[0],m[1])
    return tuple(moves)

def animateMove(rowColMove):
    pos1 = rowColMove[0]
    pos2 = rowColMove[1]
    highlightSquare(pos1[0],pos1[1])
    piece = getPiece(pos1[0],pos1[1])
    if piece.upper() == 'K' and abs(pos1[1]-pos2[1]) > 1:
        # castling
        animateMovePiece(pos1,pos2)
        if pos2[1] > pos1[1]:
            animateMovePiece((pos1[0],7),(pos1[0],pos2[1]-1))
        else:
            animateMovePiece((pos1[0],0),(pos1[0],pos2[1]+1))
    elif piece.upper() == 'P' and abs(pos2[0]==7):
        # promote to queen (all that's supported by the engine)
        animateMovePiece(pos1,pos2)
        piece = pieces[pos2]
        piece.erase()
        if pos.board[move].islower():
            v = toVehicle(QUEEN, BLACK, 'q')
        else:
            v = toVehicle(QUEEN, WHITE, 'Q')
        pieces[pos2] = v
        c = getCoords(pos2[0],pos2[1])
        v.draw(c[0],c[1],c[2])
        v.blankBehind()
        return
    else:
        victim = None
        redrawPiece = False
        if piece.upper() == 'P' and pos1[1] != pos2[1] and pos2 not in pieces:
            # en Passant
            if pos2[1] > pos1[1]:
                victim = pieces[(pos2[0],pos2[1]-1)]
            else:
                victim = pieces[(pos2[0],pos2[1]+1)]
        elif pos2 in pieces:
            victim = pieces[pos2]
            redrawPiece = True
        animateMovePiece(pos1,pos2)
        if victim is not None:
            victim.erase()
            if redrawPiece:
                piece = pieces[pos2]
                piece.draw(piece.curLocation[0],piece.curLocation[1],piece.curLocation[2])
                piece.blankBehind()
    drawSquare(pos1[0],pos1[1])
    drawSquare(pos2[0],pos2[1])

mc = Minecraft()
options = ''.join(sys.argv[1:])
black = 'b' in options
demo = 'd' in options
fast = 'f' in options
mc.postToChat("Please wait: setting up board.")
corner = mc.player.getTilePos()
corner.x -= 32
corner.z -= 32
drawEmptyBoard()

def myGetBlockWithData(pos):
    """
    On RaspberryJuice, this is a lot faster than querying the server.
    """
    for boardPos in pieces:
        if pos in pieces[boardPos].curVehicle:
            return pieces[boardPos].curVehicle[pos]
    return AIR

# z coordinate is cols
# x coordinate is rows
pieces = {}
pos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0)
for row in range(8):
    for col in range(8):
        piece = pos.board[toNumeric((row,col),False)]
        if piece in pieceBitmaps:
            v = toVehicle(pieceBitmaps[piece], WHITE, piece)
        elif piece.capitalize() in pieceBitmaps:
            v = toVehicle(pieceBitmaps[piece.capitalize()], BLACK, piece)
        else:
            continue 
        #uncomment the following line to optimize speed
        v.getBlockWithData = myGetBlockWithData
        pieces[(row,col)] = v
        c = getCoords(row,col)
        v.draw(c[0],c[1],c[2])
        v.blankBehind()

playerMovesNext = not black

while True:
    if playerMovesNext:
        if black:
            mc.postToChat("Black to move.")
        else:
            mc.postToChat("White to move.")
        if demo:
            sunfish.tp = OrderedDict()
            move,score = sunfish.search(pos)
        else:
            moves = tuple(pos.genMoves())
            move = None
            while move not in moves:
                if move is not None:
                    mc.postToChat("Illegal move.")
                mc.postToChat("Right-click the start and end points with a sword.")
                move = toNumericMove(inputMove(),black)
        rowColMove = toRowColMove(move,black)
        mc.postToChat("Player: "+ toAlgebraicMove(rowColMove))
        animateMove(rowColMove)
        pos = pos.move(move)
    mc.postToChat("Thinking...")
    if demo: sunfish.tp = OrderedDict()
    move,score = sunfish.search(pos)
    if score <= -sunfish.MATE_VALUE:
        mc.postToChat("I resign. You won the game.")
        break
    rowColMove = toRowColMove(move,not black)
    mc.postToChat("Computer: "+toAlgebraicMove(rowColMove))
    animateMove(rowColMove)
    if sunfish.MATE_VALUE <= score:
        mc.postToChat("You lost the game.")
        break
    pos = pos.move(move)
    playerMovesNext = True

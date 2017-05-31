from mine import *
from mcpi.minecraft import flatten
import text
import input
from fonts import FONTS

def flatArgs(a):
    return tuple(int(floor(float(x))) for x in flatten(a))

class FakeMC(object):
    def __init__(self, board):
        self.board = board

    def setBlock(self, *args): # (x,y,z) goes to (x,y)
        a = flatArgs(args)
        self.board.setBlock(a[0], a[2], a[3:])

class Board2D(object):
    def __init__(self, mc, width, height, distance=None, horizontal=False, background=block.STAINED_GLASS_LIGHT_BLUE):
        self.width = width
        self.height = height
        self.board = tuple( [None for i in range(height)] for j in range(width) )
        self.shown = tuple( [None for i in range(height)] for j in range(width) )
        self.mc = mc
        self.horizontal = horizontal
        self.entities = []
        playerPos = mc.player.getTilePos()
        mc.player.setRotation(180)
        if not horizontal:
            if distance is None:
                distance = 14
            self.left = playerPos.x - width // 2
            self.plane = playerPos.z - distance
            self.bottom = playerPos.y + 1            
            mc.player.setPitch(-26)
            mc.player.setTilePos(playerPos.x, playerPos.y, playerPos.z)
            if background is not None:
                mc.setBlocks(self.left,self.bottom,self.plane-1,self.left+width-1,self.bottom+height-1,self.plane-1,background)
        else:
            self.left = playerPos.x - width // 2
            self.plane = playerPos.y - 1
            self.bottom = playerPos.z + 1
            mc.player.setPitch(10)
            mc.player.setTilePos(playerPos.x, playerPos.y+(distance if distance is not None else 0), playerPos.z)
            if background is not None:
                mc.setBlocks(self.left,self.plane-1,self.bottom,self.left+width-1,self.plane-1,self.bottom-(height-1))

        self.fakeMC = FakeMC(self)

    def spawnEntity(self, entityName, *args):
        a = flatArgs(args)
        id = self.mc.spawnEntity(entityName, self._to3d(a[0], a[1]), "{NoAI:1,Time:-1,Silent:1,Invulnerable:1,NoGravity:1}")
        self.entities.append(id)
        return id

    def entitySetPos(self, id, *args):
        a = tuple(float(x) for x in flatten(args))
        self.mc.entity.setPos(id, self._to3d(a[0], a[1]))

    def deleteEntity(self, entity):
        try:
            index = self.entities.index(entity)
            if index >= 0:
                del self.entities[index]
            self.mc.removeEntity(entity)
        except:
            pass

    def stop(self):
        for e in self.entities:
            try:
                self.mc.removeEntity(e)
            except:
                pass

    def setBlock(self, *args):
        """
        setBlock(self, x, y, block)
        """
        a = flatArgs(args)
        if 0 <= a[0] < self.width and 0 <= a[1] < self.height:
            self.board[a[0]][a[1]] = a[2:]

    def getBlock(self, x, y):
        return Block(self.board[x][y])

    def _to3d(self, x, y):
        if self.horizontal:
            return (self.left+x, self.plane, self.bottom-y)
        else:
            return (self.left+x, self.bottom+y, self.plane)

    def setBlocks(self, *args):
        """
        setBlocks(self, x1, y1, x2, y2, block)
        """
        a = flatArgs(args)
        x1, y1, x2, y2 = max(0,min(a[0],a[2])), max(0,min(a[1],a[3])), min(max(a[0],a[2]),self.width-1), min(max(a[1],a[3]),self.height-1)
        for x in range(x1,x2+1):
            for y in range(y1,y2+1):
                self.board[x][y] = a[4:]

    def fill(self, block=block.AIR):
        self.setBlocks(0, 0, self.width-1, self.height-1, block)

    def draw(self):
        for x in range(self.width):
            boardCol = self.board[x]
            shownCol = self.shown[x]
            if boardCol != shownCol:
                for y in range(self.height):
                    if boardCol[y] != shownCol[y]:
                        self.mc.setBlock(self._to3d(x,y), boardCol[y])
                        shownCol[y] = boardCol[y]

    def line(self, x1, y1, x2, y2, block):
        x1 = int(floor(0.5+x1))
        y1 = int(floor(0.5+y1))
        x2 = int(floor(0.5+x2))
        y2 = int(floor(0.5+y2))
        point = [x1,y1]
        dx = x2 - x1
        dy = y2 - y1
        x_inc = -1 if dx < 0 else 1
        l = abs(dx)
        y_inc = -1 if dy < 0 else 1
        m = abs(dy)
        dx2 = l << 1
        dy2 = m << 1

        if l >= m:
            err_1 = dy2 - l
            for i in range(0,l-1):
                self.setBlock(point, block)
                if err_1 > 0:
                    point[1] += y_inc
                    err_1 -= dx2
                err_1 += dy2
                point[0] += x_inc
        elif m > l:
            err_1 = dx2 - m
            for i in range(0,m-1):
                self.setBlock(point, block)
                if err_1 > 0:
                    point[0] += x_inc
                    err_1 -= dy2
                err_1 += dx2
                point[1] += y_inc
        self.setBlock(point, block)
        self.setBlock(x2, y2, block)

    def text(self, x, y, s, foreground=block.WOOL_BLACK, background=block.AIR, font="metrix7pt", center=False):
        text.drawText(self.fakeMC, FONTS[font], Vec3(x,0,y), Vec3(1,0,0), Vec3(0,0,1), s, foreground=foreground, background=background, 
            align=text.ALIGN_CENTER if center else text.ALIGN_LEFT)

    """
    def getMousePosition(self):
        (screenWidth, screenHeight) = input.getScreenSize()
        myAspect = self.height / float(self.width)
        screenAspect = screenHeight / float(screenWidth)

        if myAspect > screenAspect:
            ratio = (self.height - 1) / (screenHeight - 1)
        else:
            ratio = (self.width - 1) / (screenWidth - 1)
            
        (x, y) = input.getMousePosition()

        x = int(floor(0.5 + self.width / 2 + (x - screenWidth / 2) * ratio))
        y = int(floor(0.5 + self.height / 2 + (y - screenHeight / 2) * ratio))

        return min(max(x, 0), self.width-1), min(max(y, 0), self.height-1)
    """

if __name__ == '__main__': 
    import time

    mc = Minecraft()
    board = Board2D(mc, 30, 20, horizontal=True)
    board.fill(block.STAINED_GLASS_LIGHT_BLUE)
    board.setBlock(0,0,block.STAINED_GLASS_MAGENTA)
    board.text(15,5, "Hello!!!", center=True)
    board.draw()

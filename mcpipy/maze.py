from mine import *
from sys import argv
from random import randint

DIRS = ((1,0),(0,1),(-1,0),(0,-1))

def generateMaze(xSize, ySize, start=(0,0), dirs=DIRS, inside=None):
    if inside == None:
        inside = lambda xy : 0 <= xy[0] < xSize and 0 <= xy[1] < ySize
        
    def move(pos, dir):
        return (pos[0]+dirs[dir][0],pos[1]+dirs[dir][1])
        
    nDirs = len(dirs)

    def findDir(v):
        for i in range(nDirs):
            if dirs[i] == v:
                return i
        raise Exception("Mismatched direction")
        
    revDir = tuple( findDir((-dirs[i][0],-dirs[i][1])) for i in range(nDirs) )          

    visited = tuple([False for j in range(ySize)] for i in range(xSize))
    walls = tuple(tuple( [True for j in range(nDirs)] for j in range(ySize) ) for i in range(xSize))
    pos = start
        
    def getVisited(pos):
        return not inside(pos) or visited[pos[0]][pos[1]]
        
    stack = []
    
    while True:
        visited[pos[0]][pos[1]] = True
        nUnvisited = 0
        for dir in range(nDirs):
            if not getVisited(move(pos,dir)):
                nUnvisited += 1
                
        if nUnvisited == 0:
            if stack:
                pos = stack.pop()
                continue
            else:
                break

        n = randint(0,nUnvisited-1)
        dir = 0
        while True:
            if not getVisited(move(pos,dir)):
                if n == 0:
                    break
                n -= 1
            dir += 1
            
        walls[pos[0]][pos[1]][dir] = False
        pos = move(pos,dir)
        walls[pos[0]][pos[1]][revDir[dir]] = False
        
        stack.append(pos)
        
    return walls
        
xSize = 40
ySize = 40
b = block.STONE

if len(argv)>1:
    xSize = int(argv[1])
    ySize = xSize
    if len(argv)>2:
        b = Block.byName(argv[2])
        
mc = Minecraft()        

walls = generateMaze(xSize,ySize)
pos = mc.player.getTilePos()

pos.x += 1
my = pos.y

for x in range(xSize):
    for y in range(ySize):
        mx = 2*x + pos.x
        mz = 2*y + pos.z
        def set(d1,d2):
            mc.setBlock(mx+d1,my,mz+d2,b)
            mc.setBlock(mx+d1,my+1,mz+d2,b)

        for dir in range(len(DIRS)):
            if walls[x][y][dir]:
                set(DIRS[dir][0],DIRS[dir][1])
        set(1,1)
        set(1,-1)
        set(-1,1)
        set(-1,-1)

mc.setBlock(pos.x-1,pos.y,pos.z,block.AIR)
mc.setBlock(pos.x-1,pos.y+1,pos.z,block.AIR)
mc.setBlock(pos.x+2*(xSize-1)+1,pos.y-1,pos.z+2*(ySize-1),block.GOLD_BLOCK)

mc.setBlockWithNBT(pos.x+2*(xSize-1)+1,pos.y,pos.z+2*(ySize-1),block.SIGN('EXIT',headingAngle=270))
mc.setBlock(pos.x+2*(xSize-1)+1,pos.y+1,pos.z+2*(ySize-1),block.AIR)

#
# MIT-licensed code by Alexander Pruss
#

from mc import *
import mcpi.settings
import cmath
import time
import sys
try:
   import multiprocessing
   cpuCount = multiprocessing.cpu_count()
except:
   cpuCount = 1

ESCAPE = 250
if len(sys.argv) < 2:
    SIZE = 100
else:
    SIZE = int(sys.argv[1])
FRACTALSIZE = 2.2

palette = list(reversed([WOOL_WHITE,HARDENED_CLAY_STAINED_WHITE,WOOL_PINK,WOOL_LIGHT_GRAY,WOOL_LIGHT_BLUE,WOOL_MAGENTA,WOOL_PURPLE,HARDENED_CLAY_STAINED_LIGHT_BLUE,HARDENED_CLAY_STAINED_LIGHT_GRAY,HARDENED_CLAY_STAINED_MAGENTA,HARDENED_CLAY_STAINED_PINK,HARDENED_CLAY_STAINED_RED,WOOL_RED,REDSTONE_BLOCK,HARDENED_CLAY_STAINED_ORANGE,WOOL_ORANGE,HARDENED_CLAY_STAINED_YELLOW,WOOL_YELLOW,WOOL_LIME,HARDENED_CLAY_STAINED_LIME,HARDENED_CLAY_STAINED_PURPLE,HARDENED_CLAY_STAINED_CYAN,WOOL_CYAN,WOOL_BLUE,HARDENED_CLAY_STAINED_BLUE,WOOL_GRAY,HARDENED_CLAY_STAINED_GREEN,WOOL_GREEN,HARDENED_CLAY_STAINED_BROWN,WOOL_BROWN,HARDENED_CLAY_STAINED_GRAY,WOOL_BLACK]));

block = WOOL_WHITE # REDSTONE_ORE

def calculate(pos):
    x,z,y = pos[0],pos[1],pos[2]
    cx,cy,cz = x,y,z

    i = 0
    try:
        wentOut = 0
        while i<ESCAPE:
            r = sqrt(x*x+y*y+z*z)
            if r > 2:
               return -1
            if r > wentOut:
               wentOut = r
            theta = acos(z/r)
            phi = atan2(y,x)
            zr = r**8
            theta *= 8
            phi *= 8

            x = cx+zr*sin(theta)*cos(phi)
            y = cy+zr*sin(phi)*sin(theta)
            z = cz+zr*cos(theta)

            i = i + 1
        return wentOut
    except:
        return 0

#
# we could of course just do for x in range(0,size): for y in range(0,size): yield(x,y)
# but it will make users happier if we start at the player
#


def pollZoom():
    global lastHitEvent,lastHitPos
    events = mc.events.pollBlockHits()
    if len(events) == 0:
        return lastHitEvent != None
    lastHitEvent = events[-1]
    lastHitPos = mc.player.getPos()
    return True

def toBulb(centerMC,centerBulb,scale,x,y,z):
    return ((x - centerMC.x) * scale  + centerBulb[0],
                    (y - centerMC.y) * scale  + centerBulb[1],
                    (z - centerMC.z) * scale + centerBulb[2])

def drawCore(core,cores,centerBulb,scale,cornerMC,size,block):
    if core > 0:
        minecraft = Minecraft()
    else:
        minecraft = mc
    centerMC = cornerMC + Vec3(size/2,size/2,size/2)
    count = 0
    for mcX in range(cornerMC.x, cornerMC.x+size):
        if mcX % cores != core:
            continue
#        minecraft.setBlocks(mcX,cornerMC.y,cornerMC.z,mcX,cornerMC.y+size-1,cornerMC.z+size-1,AIR)
        for mcY in range(cornerMC.y, cornerMC.y+size):
            for mcZ in range(cornerMC.z, cornerMC.z+size):
                radius = calculate(toBulb(centerMC,centerBulb,scale,mcX,mcY,mcZ))
                if radius < 0:
                    minecraft.setBlock(mcX,mcY,mcZ,AIR)
                else:
                    i = int(len(palette) / 1.08 * radius)
                    if i >= len(palette):
                        i = len(palette) - 1
                    minecraft.setBlock(mcX,mcY,mcZ,palette[i])
        if core==0 and pollZoom():
            return
    minecraft.postToChat("Core "+str(core+1)+" of "+str(cores)+" has rendered")

def terminateProcesses():
    global processes
    for p in processes:
        try: p.terminate()
        except: pass
    processes = []


def draw():
    global processes
    if cpuCount < 4:
        processes = []
        drawCore(0,1,centerBulb,scale,cornerMC,SIZE,block)
    else:
        cores = cpuCount - 2 # reserve two cores for Minecraft server and client processes
        processes = []
        for i in range (1,cores):
             processes.append(multiprocessing.Process(target=drawCore,args=(i,cores,centerBulb,scale,cornerMC,SIZE,block)))
        for p in processes:
             p.start()
        drawCore(0,cores,centerBulb,scale,cornerMC,SIZE,block)
        if pollZoom():
             terminateProcesses()

if __name__=='__main__':
    mc = Minecraft()
    startPos = mc.player.getTilePos()
    cornerMC = startPos + Vec3(1,0,1)
    centerMC = cornerMC + Vec3(SIZE/2,SIZE/2,SIZE/2)
    centerBulb = (0,0,0)
    initial = True
    scale    = FRACTALSIZE / SIZE
    lastHitEvent = None
    processes = []

    while True:
        mc.player.setPos(startPos)
        mc.postToChat("Scale: "+str(FRACTALSIZE/SIZE/scale))
        draw()
        if not initial:
            mc.player.setPos(centerMC)
        while not pollZoom():
            time.sleep(0.25)
        terminateProcesses()
        processes = []
        if ( lastHitEvent.pos.x < cornerMC.x or
             lastHitEvent.pos.x >= cornerMC.x + SIZE or
             lastHitEvent.pos.y < cornerMC.y or
             lastHitEvent.pos.y >= cornerMC.y + SIZE or
             lastHitEvent.pos.z < cornerMC.z or
             lastHitEvent.pos.z >= cornerMC.z + SIZE ):
                mc.postToChat("resetting")
                centerBulb = (0,0,0)
                scale = FRACTALSIZE / SIZE
                initial = True
        else:
                mc.postToChat("zooming")
                centerBulb = toBulb(centerMC,centerBulb,scale,lastHitPos.x,lastHitPos.y,lastHitPos.z)
                scale /= 8
                initial = False
        lastHitEvent = None

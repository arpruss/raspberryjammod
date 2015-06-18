from mc import *
import text8x8
import datetime
import time
import sys

foreground = SEA_LANTERN
background = AIR

try:
    if len(sys.argv) > 1:
        foreground = int(sys.argv[1])
except:
    pass

try:
    if len(sys.argv) > 2:
        background = int(sys.argv[2])
except:
    pass

mc = Minecraft()
pos = mc.player.getTilePos()
forward = text8x8.angleToTextDirection(mc.player.getRotation())

prevTime = ""

while True:
    curTime = datetime.datetime.now().strftime("%I:%M:%S %p")
    if curTime[0]=='0':
        curTime[0] = ' '
    if prevTime != curTime:
        text8x8.drawText8x8(mc, pos, forward, Vec3(0,1,0), curTime, foreground, background)
        prevTime = curTime
    time.sleep(0.1)

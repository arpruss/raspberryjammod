#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
import text
import datetime
import time
import sys
import fonts

foreground = block.SEA_LANTERN # this needs Minecraft 1.8
background = block.AIR

try:
    foreground = Block.byName(sys.argv[1])
except:
    pass

try:
    background = Block.byName(sys.argv[2])
except:
    pass

mc = Minecraft()
pos = mc.player.getTilePos()
forward = text.angleToTextDirection(mc.player.getRotation())

prevTime = ""

while True:
    curTime = datetime.datetime.now().strftime("%I:%M:%S %p")
    if curTime[0]=='0':
        curTime = ' ' + curTime[1:]
    if prevTime != curTime:
        for i in range(len(curTime)):
            if i >= len(prevTime) or prevTime[i] != curTime[i]:
                text.drawText(mc, fonts.FONTS['8x8'], pos + forward * (8*i), forward, Vec3(0,1,0), curTime[i:], foreground, background)
                break
        prevTime = curTime
    time.sleep(0.1)

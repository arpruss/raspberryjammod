from mc import *
import text8x8
import datetime
import time
import sys

foreground = SEA_LANTERN
background = AIR

if len(sys.argv) > 1:
    foreground = eval(sys.argv[1])

if len(sys.argv) > 2:
    background = eval(sys.argv[2])

mc = Minecraft()
pos = mc.player.getTilePos()
forward = text8x8.angleToTextDirection(mc.player.getRotation())

while True:
    t = datetime.datetime.now().strftime("%I:%M:%S %p")
    if t[0]=='0':
        t[0] = ' '
    text8x8.drawText8x8(mc, pos, forward, Vec3(0,1,0), t, foreground, background)
    time.sleep(0.5)

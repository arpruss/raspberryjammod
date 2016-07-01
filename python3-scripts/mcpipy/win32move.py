from mc import *
from time import sleep
import win32con,win32api

mc = Minecraft()

lastPlatform = None
lastPlatformBlock = None

UNSOLID = set([WATER_FLOWING.id,WATER_STATIONARY.id,AIR.id,LAVA_FLOWING.id,LAVA_STATIONARY.id])

while True:
    pos = mc.player.getTilePos()
    move = False
    if win32api.GetAsyncKeyState(win32con.VK_NEXT):
        pos.y -= 1
        move = True
    if win32api.GetAsyncKeyState(win32con.VK_PRIOR):
        pos.y += 1
        move = True
    if win32api.GetAsyncKeyState(win32con.VK_LEFT):
        pos.x += 1
        move = True
    if win32api.GetAsyncKeyState(win32con.VK_RIGHT):
        pos.x -= 1
        move = True
    if win32api.GetAsyncKeyState(win32con.VK_UP):
        pos.z += 1
        move = True
    if win32api.GetAsyncKeyState(win32con.VK_DOWN):
        pos.z -= 1
        move = True
    if move:
        block = mc.getBlock(pos.x,pos.y-1,pos.z)
        if block in UNSOLID:
            drew = Vec3(pos.x,pos.y-1,pos.z)
            mc.setBlock(drew,GLASS)
        else:
            drew = None
        mc.player.setTilePos(pos)
        if lastPlatform and (not drew or lastPlatform != drew):
            mc.setBlock(lastPlatform,AIR)
            lastPlatform = None
        if drew:
            lastPlatform = drew
            lastPlatformBlock = block
    sleep(0.2)
    
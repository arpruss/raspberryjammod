import mcpi.minecraft as minecraft
import server
import time
from math import *
from mcpi.block import *
from mcturtle import *
import code

def inputLine(prompt):
    mc.events.clearAll()
    while True:
        chats = mc.events.pollChatPosts()
        for c in chats:
            if c.entityId == playerId:
                print c.message
                return c.message
        time.sleep(0.2)

mc = minecraft.Minecraft.create(server.address)
playerPos = mc.player.getPos()
playerId = mc.getPlayerId()
t = Turtle(mc)

mc.postToChat("Enter python code into chat, type quit() to quit.")
i = code.interact(banner="", readfunc=inputLine, local=locals())

#
# Code under the MIT license by Alexander Pruss
#
# This script only works on Raspberry Jam
#

import mcpi.minecraft as minecraft
import time
from math import *
from mcpi.block import *
import code
import sys


def quit():
    sys.exit()

def inputLine(prompt):
    mc.events.clearAll()
    while True:
        chats = mc.events.pollChatPosts()
        for c in chats:
            if c.entityId == playerId:
                print c.message
                if c.message == 'quit':
                    return 'quit()'
                elif c.message == ' ':
                    return ''
                else:
                    return c.message
        time.sleep(0.2)

mc = minecraft.Minecraft()
playerPos = mc.player.getPos()
playerId = mc.getPlayerId()

mc.postToChat("Enter python code into chat, type 'quit' to quit.")
i = code.interact(banner="Minecraft Python ready", readfunc=inputLine, local=locals())

from . import mcpi.minecraft as minecraft
from . import server
import time
from math import *
from .mcpi.block import *

mc = minecraft.Minecraft.create(server.address)
playerPos = mc.player.getPos()
playerId = mc.getPlayerId()

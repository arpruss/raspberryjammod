from mine import *
from sys import argv
mc = Minecraft()
mc.player.setTilePos(int(argv[1]), int(argv[2]), int(argv[3]))

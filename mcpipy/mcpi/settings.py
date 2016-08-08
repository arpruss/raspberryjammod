from os import environ

MINECRAFT_POCKET_EDITION = 0
MINECRAFT_PI = 1
MINECRAFT_DESKTOP = 2

minecraftType = MINECRAFT_DESKTOP

try:
     minecraftType = int(environ['MINECRAFT_TYPE'])
except:
     pass

isPE = ( minecraftType != MINECRAFT_DESKTOP )


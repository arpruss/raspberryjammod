#
# MIT-licensed code by Alexander R. Pruss
#
# Useful for checking which interpreter RaspberryJamMod's /py command is picking up.
#

from . import mc
import sys
import os

mc = mc.Minecraft()
mc.postToChat("Python interpreter "+sys.executable+" "+sys.version)
mc.postToChat("Invoking user "+os.environ['MINECRAFT_PLAYER_NAME']+" "+os.environ['MINECRAFT_PLAYER_ID'])

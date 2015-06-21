#
# Code under the MIT license by Alexander R. Pruss
#
# Useful for checking which interpreter RaspberryJamMod's /py command is picking up.
#

import mc
import sys
import os

mc = mc.Minecraft()
mc.postToChat("Python interpreter "+sys.executable+" "+sys.version)
try:
    userName = os.environ['MINECRAFT_PLAYER_NAME']
except:
    userName = "unspecified"
try:
    userId = os.environ['MINECRAFT_PLAYER_ID']
except:
    userId = "unspecified"
mc.postToChat("Invoked by user "+userName+" "+userId)

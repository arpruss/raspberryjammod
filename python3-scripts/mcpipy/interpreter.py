#
# MIT-licensed code by Alexander R. Pruss
#
# Useful for checking which interpreter RaspberryJamMod's /py command is picking up.
#

import mc
import sys

mc.Minecraft().postToChat("Python interpreter "+sys.executable+" "+sys.version)

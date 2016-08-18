#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
import sys
import time
from NeuroPy.NeuroPy import NeuroPy

mc = Minecraft()

#
# the True argument is needed for a BrainFlex unit hacked to work
# at 57600 using
# http://www.instructables.com/id/Mindflex-EEG-with-raw-data-over-Bluetooth/
#
eeg = NeuroPy("COM11",57600,True)

meditation = len(sys.argv) > 1 and sys.argv[1].startswith("m")

up = 60
down = 40

def callback(a):
    mc.postToChat(a)
    if a > up:
       pos = mc.player.getPos()
       pos.y = pos.y + 1
       if mc.getBlock(pos.x,pos.y,pos.z) == block.AIR.id:
          mc.player.setPos(pos)
    elif a < down:
       pos = mc.player.getPos()
       pos.y = pos.y - 1
       if mc.getBlock(pos.x,pos.y,pos.z) == block.AIR.id:
          mc.player.setPos(pos)

if meditation:
    eeg.setCallBack("meditation", callback)
else:
    eeg.setCallBack("attention", callback)


mc.postToChat("Connecting to EEG")
eeg.start()

if meditation:
    mc.postToChat("To fly up, be meditative")
else:
    mc.postToChat("To fly up, be attentive")

while True:
    time.sleep(10)

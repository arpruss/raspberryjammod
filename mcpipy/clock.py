#
# Code by Alexander Pruss and under the MIT license
#

from drawing import *
import time

d = Drawing()

class Hand:
    def __init__(self, center, scale, length, width, material, backMaterial):
        self.center = center
        self.length = length
        self.width = width
        self.scale = scale
        self.previousValue = None
        self.material = material
        self.backMaterial = backMaterial

    def update(self, value):
        d.penwidth(self.width)
        if self.previousValue != None and self.previousValue != value:
            self.drawLine(self.previousValue, self.backMaterial)
        self.drawLine(value, self.material)
        self.previousValue = value

    def drawLine(self, value, block):
        angle = pi / 2 - (value % self.scale) * 2 * pi / self.scale
        d.line(self.center[0],self.center[1],self.center[2],
               self.center[0] + self.length * cos(angle),
               self.center[1] + self.length * sin(angle),
               self.center[2], block)

radius = 20

playerPos = d.mc.player.getPos()

center = (playerPos.x, playerPos.y + radius, playerPos.z - radius)

for x in range(-radius, radius+1):
    for y in range(-radius, radius+1):
        if x**2+y**2 <= radius**2:
            d.point(center[0]+x, center[1]+y, center[2]-3, block.WOOL_BLACK)

d.penwidth(1)
for tick in range(0,12):
    d.line(center[0]+0.85*radius*cos(tick * 2 * pi / 12),center[1]+0.85*radius*sin(tick * 2 * pi / 12), center[2]-3,
           center[0]+radius*cos(tick * 2 * pi / 12),center[1]+radius*sin(tick * 2 * pi / 12), center[2]-3,
           block.WOOL_BLUE)

hourHand = Hand(center, 12, radius * 0.5, 3, block.GOLD_BLOCK, block.AIR)
minuteHand = Hand(center, 60, radius * 0.8, 2, block.GOLD_BLOCK, block.AIR)
secondHand = Hand((center[0],center[1],center[2]+1), 60, radius * 0.8, 1, block.WOOL_RED, block.AIR) 

while True:
    t = time.localtime()
    hourHand.update(t[3])
    minuteHand.update(t[4])
    secondHand.update(t[5])
    time.sleep(1)
    

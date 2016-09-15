from mine import *
from drawing import *
from random import choice

mc = Minecraft()
drawing = Drawing(mc)

pos = mc.player.getTilePos()
radius = 10

A = block.WOOL_ORANGE
C = block.WOOL_GREEN
G = block.WOOL_BLUE
T = block.WOOL_RED

blocks = { "A":(A,T), "C":(C,G), "T":(T,A), "G":(G,C) }
# sequence taken from somewhere in chromosome 5, retrieved via Wolfram Alpha
sequence = "CAAAAGTGTGGGGAAATTAATTTGGGAATTACTCTCCTCATTGAAAAATATCTCATTTGCTAAAATAAGACAGTAAAACAGTACAGTTTAAATATTTATAAAAATAGGAAAGTTTGGCAAAAAGAGAGGAGTACACACCTGTGACTACTGAGTTGCTGTGAAAATTTCATTTCCTGATACAAAATTGTCTAAAGCACTTG"

def getPair(i):
    return blocks[sequence[-i-1]]
    
prev = None
skip = 2
for y in range(240):
    theta = y * pi / (skip*10)
    y1 = pos.y + y
    x1 = pos.x - radius * cos(theta)
    x2 = pos.x + radius * cos(theta)
    z1 = pos.z + radius * sin(theta)
    z2 = pos.z - radius * sin(theta)
    if y % skip == 0:
        pair = getPair(y//skip)
        drawing.penwidth(1)
        drawing.line(x1,y1,z1,pos.x,y1,pos.z,pair[0])
        drawing.line(x2,y1,z2,pos.x,y1,pos.z,pair[1])
    
    if prev is not None:
        drawing.penwidth(2)
        drawing.line(prev[0],prev[1],prev[2],x1,y1,z1,block.WOOL_WHITE)
        drawing.line(prev[3],prev[4],prev[5],x2,y1,z2,block.WOOL_WHITE)
    prev = x1,y1,z1,x2,y1,z2

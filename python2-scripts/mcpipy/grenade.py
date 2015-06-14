#
# MIT-licensed code by Alexander Pruss
#

#
# python grenade.py [speed [gravity]]
#
# Throws a grenade with the specified speed in m/s (default: 15) and specified
# gravitational acceleration (default: earth) in m/s^2 or given by listing a planet,
# sun, moon or pluto.
#

from mc import *
import time
import sys

GRAVITIES = {
    'sun':274,
    'mercury':3.59,
    'venus':8.87,
    'earth':9.81,
    'moon':1.62,
    'mars':3.77,
    'jupiter':25.95,
    'saturn':11.08,
    'uranus':10.67,
    'neptune':14.07,
    'pluto':0.42
    }

def getPath(center, azi, alt, v0):
    vx = v0 * cos(alt) * sin(-azi)
    vy = v0 * sin(alt)
    vz = v0 * cos(alt) * cos(-azi)
    t = 0
    x = center.x + cos(alt) * sin(-azi) * 2
    y = center.y + sin(alt) * 2 + 2
    z = center.z + cos(alt) * cos(-azi) * 2
    path = [(t,Vec3(round(x),round(y),round(z)))]
    while not mc.getBlock(x,y,z):
        v = sqrt(vx*vx+vy*vy+vz*vz)
        if v < 1:
            dt = 0.5
        else:
            dt = 0.5/v
        v1x = vx
        v1y = vy - g * dt
        v1z = vz
        x += (vx+v1x)/2 * dt
        y += (vy+v1y)/2 * dt
        z += (vz+v1z)/2 * dt
        vx = v1x
        vy = v1y
        vz = v1z
        t += dt
        path.append( ( t,Vec3(round(x),round(y),round(z)) ) )
    return path

def drawGrenade(dictionary, pos, material):
    if pos is None:
        return
    dictionary[(pos.x-1,pos.y,pos.z)] = material
    dictionary[(pos.x+1,pos.y,pos.z)] = material
    dictionary[(pos.x,pos.y-1,pos.z)] = material
    dictionary[(pos.x,pos.y+1,pos.z)] = material
    dictionary[(pos.x,pos.y,pos.z-1)] = material
    dictionary[(pos.x,pos.y,pos.z+1)] = material

def getXYZ(path, t1):
    for t,xyz in path:
        if t1<=t:
            return xyz
    return path[-1][1]

mc = Minecraft()

try:
    v0 = int(sys.argv[1])
except:
    v0 = 15

if 3 <= len(sys.argv):
    try:
        g = float(sys.argv[2])
    except:
        g = GRAVITIES[sys.argv[2].lower()]
else:
    g = GRAVITIES['earth']

center = mc.player.getPos()
azi = mc.player.getRotation() * pi/180.
alt = -mc.player.getPitch() * pi/180.

horizontal0 = 2
vertical0 = 2

path = getPath(center, azi, alt, v0)

dictionary = {}
drawGrenade(dictionary, path[0][1], TNT)
prev = path[0][1]
t0 = time.time()

while True:
    t = time.time() - t0
    pos = getXYZ(path,t)
    dictionary = {}
    drawGrenade(dictionary, prev, AIR)
    drawGrenade(dictionary, pos, TNT)
    for key in dictionary:
        mc.setBlock(key,dictionary[key])
    prev=pos
    time.sleep(0.1)
    if t > path[-1][0]:
        break

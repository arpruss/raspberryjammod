#
# This script uses RaspberryJamMod's ability to capture all hits, not just sword hits, to provide symmetric
# drawing. Stand at the center of symmetry. By default, you get north-south and east-west mirroring, but you
# can include other transformations on the commandline:
#
#    n : northsouth flip
#    e : east west flip
#    u : up down flip
#
#    nw : nw - se flip
#    ne : ne - sw flip
#
#    90 : 90, 180 and 270 degrees in the plane
#    180 : 180 degrees in the plane
#
# Code by Alexander Pruss under MIT license.
#

from mcpi.minecraft import Minecraft
import sys
import time

xn = ( (1,0,0), 
       (0,1,0),
       (0,0,-1) )
xe = ( (-1,0,0),
       (0,1,0),
       (0,0,1) )
xu = ( (1,0,0),
       (0,-1,0),
       (0,0,-1) )
xnw = ( (0,0,-1),
        (0,1,0),
        (-1,0,0) )
xne = ( (0,0,1),
        (0,1,0),
        (1,0,0 ) )
x90 = ( (0,0,1),
        (0,1,0),
        (-1,0,0) )
xid = ( (1,0,0),
        (0,1,0),
        (0,0,1) )

faces = ( (0,-1,0), (0,1,0), (0,0,-1), (0,0,1), (-1,0,0), (1,0,0), (0,0,0) )

def mulMat(a,b):
    return tuple(tuple(a[i][0]*b[0][j]+a[i][1]*b[1][j]+a[i][2]*b[2][j] for j in range(3)) for i in range(3))

def mulMatVec(a,b):
    return tuple(a[i][0]*b[0]+a[i][1]*b[1]+a[i][2]*b[2] for i in range(3))

def subVec(a,b):
    return tuple(a[i]-b[i] for i in range(3))

def addVec(a,b):
    return tuple(a[i]+b[i] for i in range(3))

x180 = mulMat(x90,x90)

if __name__ == "__main__":
    def copy(v):
        block = mc.getBlockWithNBT(v)
        for mat in transforms:
            v2 = addVec(mulMatVec(mat,subVec(v,center)),center)
            mc.setBlockWithNBT(v2,block)


    if len(sys.argv) <= 1:
        transforms = set( [xn,xe] )
    else:
        transforms = set()
        for opt in sys.argv[1:]:
            if opt == 'n':
                transforms.add(xn)
            elif opt == 'e':
                transforms.add(xe)
            elif opt == 'u':
                transforms.add(xu)
            elif opt == 'nw':
                transforms.add(xnw)
            elif opt == 'ne':
                transforms.add(xne)
            elif opt == '90':
                transforms.add(x90)
            elif opt == '180':
                transforms.add(x180)

    mc = Minecraft()

    playerPos = mc.player.getPos()

    center = tuple(0.5 * round(2 * x) - 0.5 for x in playerPos)

    if len(transforms) == 0:
        mc.postToChat("No recognized symmetries.")
        exit()

    mc.conn.send("events.setting","restrict_to_sword",0)

    transforms.add(xid)
    old = set()

    while len(old) < len(transforms):
        old = transforms
        transforms = set()
        for a in old:
            for b in old:
                transforms.add(mulMat(a,b))

    mc.postToChat("Will be drawing {} copies".format(len(transforms)))

    transforms.remove(xid)

    mc.events.clearAll()

    while True:
        hits = mc.events.pollBlockHits()
        time.sleep(0.25)
        for h in hits:
            v = tuple(x for x in h.pos)
            copy(v)
            copy(addVec(v,faces[h.face]))
            
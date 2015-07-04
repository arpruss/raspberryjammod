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
#  Alternately you can do translational symmetry with:
#    t N x y z : translate N times by vector (x,y,z)
#
# Code by Alexander Pruss under MIT license.
#

from mcpi.minecraft import Minecraft
import mcpi.block as block
from functools import partial
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
    def copy(v,airOnly=False):
        b = mc.getBlockWithNBT(v)
        if airOnly and b.id != block.AIR.id:
            return
        v1 = addVec(v,(0.5,0.5,0.5))
        for t in transforms:
            mc.setBlockWithNBT(t(v1),b)

    mc = Minecraft()

    playerPos = mc.player.getPos()

    transforms = []
    if len(sys.argv) > 5 and sys.argv[1][0] == 't':
        n = int(sys.argv[2])
        transforms = []
        x,y,z = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
        for k in range(1,n+1):
            transforms.append(lambda v,k=k : addVec(v,(k*x,k*y,k*z)))
    else:
        if len(sys.argv) <= 1:
            matrices = set( [xn,xe] )
        else:
            matrices = set([xid])
            for opt in sys.argv[1:]:
                if opt == 'n':
                    matrices.add(xn)
                elif opt == 'e':
                    matrices.add(xe)
                elif opt == 'u':
                    matrices.add(xu)
                elif opt == 'nw':
                    matrices.add(xnw)
                elif opt == 'ne':
                    matrices.add(xne)
                elif opt == '90':
                    matrices.add(x90)
                elif opt == '180':
                    matrices.add(x180)
            if len(matrices) == 0:
                mc.postToChat("No recognized symmetries.")
                exit()

        matrices.add(xid)
        old = set()

        while len(old) < len(matrices):
            old = matrices
            matrices = set()
            for a in old:
                for b in old:
                    matrices.add(mulMat(a,b))
        matrices.remove(xid)
        for m in matrices:
            transforms.append(lambda v,m=m : addVec(mulMatVec(m,subVec(v,center)),center))

    center = tuple(0.5 * round(2 * x) for x in playerPos)

    mc.conn.send("events.setting","restrict_to_sword",0)

    mc.postToChat("Will be drawing {} copies".format(1+len(transforms)))

    mc.events.clearAll()

    while True:
        hits = mc.events.pollBlockHits()
        time.sleep(0.25)
        for h in hits:
            v = tuple(x for x in h.pos)
            copy(v,airOnly=True)
            copy(addVec(v,faces[h.face]))
            
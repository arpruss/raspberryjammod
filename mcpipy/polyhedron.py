from __future__ import print_function
#The software in this file is copyright 2003,2004 Simon Tatham and copyright 2015 Alexander Pruss
#Based on code from http://www.chiark.greenend.org.uk/~sgtatham/polyhedra/
#
#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation files
#(the "Software"), to deal in the Software without restriction,
#including without limitation the rights to use, copy, modify, merge,
#publish, distribute, sublicense, and/or sell copies of the Software,
#and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT.  IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE
#FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from math import pi, asin, atan2, cos, sin, sqrt
import string
import random
import drawing
import sys

# Python code to find the crossing point of two lines.

# This function is optimised for big-integer or FP arithmetic: it
# multiplies up to find two big numbers, and then divides them. So
# if you use it on integers it will give the most accurate answer
# it possibly can within integers, but might overflow if you don't
# use longs. I haven't carefully analysed the FP properties, but I
# can't see it going _too_ far wrong.
#
# Of course there's no reason you can't feed it rationals if you
# happen to have a Rational class. It only does adds, subtracts,
# multiplies, divides and tests of equality on its arguments, so
# any data type supporting those would be fine.

def crosspoint(xa1,ya1,xa2,ya2,xb1,yb1,xb2,yb2):
    "Give the intersection point of the (possibly extrapolated) lines\n"\
    "segments (xa1,ya1)-(xa2,ya2) and (xb1,yb1)-(xb2,yb2)."
    dxa = xa2-xa1
    dya = ya2-ya1
    dxb = xb2-xb1
    dyb = yb2-yb1
    # Special case: if gradients are equal, die.
    if dya * dxb == dxa * dyb:
        return None
    # Second special case: if either gradient is horizontal or
    # vertical.
    if dxa == 0:
        # Because we've already dealt with the parallel case, dxb
        # is now known to be nonzero. So we can simply extrapolate
        # along the b line until it hits the common value xa1==xa2.
        return (xa1, (xa1 - xb1) * dyb / dxb + yb1)
    # Similar cases for dya == 0, dxb == 0 and dyb == 0.
    if dxb == 0:
        return (xb1, (xb1 - xa1) * dya / dxa + ya1)
    if dya == 0:
        return ((ya1 - yb1) * dxb / dyb + xb1, ya1)
    if dyb == 0:
        return ((yb1 - ya1) * dxa / dya + xa1, yb1)

    # General case: all four gradient components are nonzero. In
    # this case, we have
    #
    #     y - ya1   dya           y - yb1   dyb
    #     ------- = ---    and    ------- = ---
    #     x - xa1   dxa           x - xb1   dxb
    #
    # We rewrite these equations as
    #
    #     y = ya1 + dya (x - xa1) / dxa
    #     y = yb1 + dyb (x - xb1) / dxb
    #
    # and equate the RHSes of each
    #
    #     ya1 + dya (x - xa1) / dxa = yb1 + dyb (x - xb1) / dxb
    #  => ya1 dxa dxb + dya dxb (x - xa1) = yb1 dxb dxa + dyb dxa (x - xb1)
    #  => (dya dxb - dyb dxa) x =
    #          dxb dxa (yb1 - ya1) + dya dxb xa1 - dyb dxa xb1
    #
    # So we have a formula for x
    #
    #         dxb dxa (yb1 - ya1) + dya dxb xa1 - dyb dxa xb1
    #     x = -----------------------------------------------
    #                        dya dxb - dyb dxa
    #
    # and by a similar derivation we also obtain a formula for y
    #
    #         dya dyb (xa1 - xb1) + dxb dya yb1 - dxa dyb ya1
    #     y = -----------------------------------------------
    #                        dya dxb - dyb dxa

    det = dya * dxb - dyb * dxa
    xtop = dxb * dxa * (yb1-ya1) + dya * dxb * xa1 - dyb * dxa * xb1
    ytop = dya * dyb * (xa1-xb1) + dxb * dya * yb1 - dxa * dyb * ya1

    return (xtop / det, ytop / det)

def makePoints(n):
    points = []

    for i in range(n):
        # Invent a randomly distributed point.
        #
        # To distribute points uniformly over a spherical surface, the
        # easiest thing is to invent its location in polar coordinates.
        # Obviously theta (longitude) must be chosen uniformly from
        # [0,2*pi]; phi (latitude) must be chosen in such a way that
        # the probability of falling within any given band of latitudes
        # must be proportional to the total surface area within that
        # band. In other words, the probability _density_ function at
        # any value of phi must be proportional to the circumference of
        # the circle around the sphere at that latitude. This in turn
        # is proportional to the radius out from the sphere at that
        # latitude, i.e. cos(phi). Hence the cumulative probability
        # should be proportional to the integral of that, i.e. sin(phi)
        # - and since we know the cumulative probability needs to be
        # zero at -pi/2 and 1 at +pi/2, this tells us it has to be
        # (1+sin(phi))/2.
        #
        # Given an arbitrary cumulative probability function, we can
        # select a number from the represented probability distribution
        # by taking a uniform number in [0,1] and applying the inverse
        # of the function. In this case, this means we take a number X
        # in [0,1], scale and translate it to obtain 2X-1, and take the
        # inverse sine. Conveniently, asin() does the Right Thing in
        # that it maps [-1,+1] into [-pi/2,pi/2].

        theta = random.random() * 2*pi
        phi = asin(random.random() * 2 - 1)
        points.append((cos(theta)*cos(phi), sin(theta)*cos(phi), sin(phi)))


    # For the moment, my repulsion function will be simple
    # inverse-square, followed by a normalisation step in which we pull
    # each point back to the surface of the sphere.

    while 1:
        # Determine the total force acting on each point.
        forces = []
        for i in range(len(points)):
            p = points[i]
            f = (0,0,0)
            ftotal = 0
            for j in range(len(points)):
                if j == i: continue
                q = points[j]

                # Find the distance vector, and its length.
                dv = (p[0]-q[0], p[1]-q[1], p[2]-q[2])
                dl = sqrt(dv[0]**2 + dv[1]**2 + dv[2]**2)

                # The force vector is dv divided by dl^3. (We divide by
                # dl once to make dv a unit vector, then by dl^2 to
                # make its length correspond to the force.)
                dl3 = dl ** 3
                fv = (dv[0]/dl3, dv[1]/dl3, dv[2]/dl3)

                # Add to the total force on the point p.
                f = (f[0]+fv[0], f[1]+fv[1], f[2]+fv[2])

            # Stick this in the forces array.
            forces.append(f)

            # Add to the running sum of the total forces/distances.
            ftotal = ftotal + sqrt(f[0]**2 + f[1]**2 + f[2]**2)

        # Scale the forces to ensure the points do not move too far in
        # one go. Otherwise there will be chaotic jumping around and
        # never any convergence.
        if ftotal > 0.25:
            fscale = 0.25 / ftotal
        else:
            fscale = 1

        # Move each point, and normalise. While we do this, also track
        # the distance each point ends up moving.
        dist = 0
        for i in range(len(points)):
            p = points[i]
            f = forces[i]
            p2 = (p[0] + f[0]*fscale, p[1] + f[1]*fscale, p[2] + f[2]*fscale)
            pl = sqrt(p2[0]**2 + p2[1]**2 + p2[2]**2)
            p2 = (p2[0] / pl, p2[1] / pl, p2[2] / pl)
            dv = (p[0]-p2[0], p[1]-p2[1], p[2]-p2[2])
            dl = sqrt(dv[0]**2 + dv[1]**2 + dv[2]**2)
            dist = dist + dl
            points[i] = p2

        # Done. Check for convergence and finish.
        #sys.stderr.write(str(dist) + "\n")
        if dist < 1e-6:
            return points

def genFacesFace(points,x0,y0,z0,scale):
    # Draw each face of the polyhedron.
    #
    # Originally this function produced a PostScript diagram of
    # each plane, showing the intersection lines with all the other
    # planes, numbering which planes they were, and outlining the
    # central polygon. This gives enough information to construct a
    # net of the solid. However, it now seems more useful to output
    # a 3D model of the polygon, but the PS output option is still
    # available if required.

    faces = []
    vertices = {}

    for i in range(len(points)):
        x, y, z = points[i]

        # Begin by rotating the point set so that this point
        # appears at (0,0,1). To do this we must first find the
        # point's polar coordinates...
        theta = atan2(y, x)
        phi = asin(z)
        # ... and construct a matrix which first rotates by -theta
        # about the z-axis, thus bringing the point to the
        # meridian, and then rotates by pi/2-phi about the y-axis
        # to bring the point to (0,0,1).
        #
        # That matrix is therefore
        #
        #  ( cos(pi/2-phi)  0 -sin(pi/2-phi) ) ( cos(-theta) -sin(-theta) 0 )
        #  (       0        1        0       ) ( sin(-theta)  cos(-theta) 0 )
        #  ( sin(pi/2-phi)  0  cos(pi/2-phi) ) (      0            0      1 )
        #
        # which comes to
        #
        #  ( cos(theta)*sin(phi)  sin(theta)*sin(phi)  -cos(phi) )
        #  (     -sin(theta)          cos(theta)           0     )
        #  ( cos(theta)*cos(phi)  sin(theta)*cos(phi)   sin(phi) )

        matrix = [
        [ cos(theta)*sin(phi),  sin(theta)*sin(phi),  -cos(phi) ],
        [     -sin(theta)    ,      cos(theta)     ,      0     ],
        [ cos(theta)*cos(phi),  sin(theta)*cos(phi),   sin(phi) ]]

        rpoints = []
        for j in range(len(points)):
            if j == i: continue
            xa, ya, za = points[j]
            xb = matrix[0][0] * xa + matrix[0][1] * ya + matrix[0][2] * za
            yb = matrix[1][0] * xa + matrix[1][1] * ya + matrix[1][2] * za
            zb = matrix[2][0] * xa + matrix[2][1] * ya + matrix[2][2] * za
            rpoints.append((j, xb, yb, zb))

        # Now. For each point in rpoints, we find the tangent plane
        # to the sphere at that point, and find the line where it
        # intersects the uppermost plane Z=1.
        edges = []
        for j, x, y, z in rpoints:
            # The equation of the plane is xX + yY + zZ = 1.
            # Combining this with the equation Z=1 is trivial, and
            # yields the linear equation xX + yY = (1-z). Two
            # obvious points on this line are those with X=0 and
            # Y=0, which have coordinates (0,(1-z)/y) and
            # ((1-z)/x,0).
            if x == 0 or y == 0:
                continue # this point must be diametrically opposite us
            x1, y1 = 0, (1-z)/y
            x2, y2 = (1-z)/x, 0

            # Find the point of closest approach between this line
            # and the origin. This is most easily done by returning
            # to the original equation xX+yY=(1-z); this clearly
            # shows the line to be perpendicular to the vector
            # (x,y), and so the closest-approach point is where X
            # and Y are in that ratio, i.e. X=kx and Y=ky. Thus
            # kx^2+ky^2=(1-z), whence k = (1-z)/(x^2+y^2).
            k = (1-z)/(x*x+y*y)
            xx = k*x
            yy = k*y

            # Store details of this line.
            edges.append((x1,y1, x2,y2, xx,yy, i, j))

            # Find the intersection points of this line with the
            # edges of the square [-2,2] x [-2,2].
            xyl = crosspoint(x1, y1, x2, y2, -2, -2, -2, +2)
            xyr = crosspoint(x1, y1, x2, y2, +2, -2, +2, +2)
            xyu = crosspoint(x1, y1, x2, y2, -2, +2, +2, +2)
            xyd = crosspoint(x1, y1, x2, y2, -2, -2, +2, -2)
            # Throw out any which don't exist, or which are beyond
            # the limits.
            xys = []
            for xy in [xyl, xyr, xyu, xyd]:
                if xy == None: continue
                if xy[0] < -2 or xy[0] > 2: continue
                if xy[1] < -2 or xy[1] > 2: continue
                xys.append(xy)

        # The diagram we have just drawn is going to be a complex
        # stellated thing, with many intersection lines shown that
        # aren't part of the actual face of the polyhedron because
        # they are beyond its edges. Now we narrow our focus to
        # find the actual edges of the polygon.

        # We begin by notionally growing a circle out from the
        # centre point until it touches one of the lines. This line
        # will be an edge of the polygon, and furthermore the point
        # of contact will be _on_ the edge of the polygon. In other
        # words, we pick the edge whose closest-approach point is
        # the shortest distance from the origin.
        best = None
        n = None
        for j in range(len(edges)):
            xx,yy = edges[j][4:6]
            d2 = xx * xx + yy * yy
            if best == None or d2 < best:
                best = d2
                n = j

        assert n != None
        e = edges[n]
        startn = n
        # We choose to look anticlockwise along the edge. This
        # means mapping the vector (xx,yy) into (-yy,xx).
        v = (-e[5],e[4])
        p = (e[4],e[5])
        omit = -1  # to begin with we omit the intersection with no other edge
        poly = []
        while 1:
            # Now we have an edge e, a point p on the edge, and a
            # direction v in which to look along the edge. Examine
            # this edge's intersection points with all other edges,
            # and pick the one which is closest to p in the
            # direction of v (discarding any which are _behind_ p).
            xa1, ya1, xa2, ya2 = e[0:4]
            best = None
            n2 = None
            xp = yp = None
            for j in range(len(edges)):
                if j == omit or j == n:
                    continue # ignore this one
                xb1, yb1, xb2, yb2 = edges[j][0:4]
                xcyc = crosspoint(xa1, ya1, xa2, ya2, xb1, yb1, xb2, yb2)
                if xcyc == None:
                    continue # this edge is parallel to e
                xc, yc = xcyc
                dotprod = (xc - p[0]) * v[0] + (yc - p[1]) * v[1]
                if dotprod < 0:
                    continue
                if best == None or dotprod < best:
                    best = dotprod
                    n2 = j
                    xp, yp = xc, yc
            assert n2 != None
            # Found a definite corner of the polygon. Save its
            # coordinates, and also save the numbers of the three
            # planes at whose intersection the point lies.
            poly.append((xp, yp, e[6], e[7], edges[n2][7]))
            # Now move on. We must now look along the new edge.
            e = edges[n2]
            p = xp, yp     # start looking from the corner we've found
            omit = n       # next time, ignore the corner we've just hit!
            n = n2
            # v is slightly tricky. We are moving anticlockwise
            # around the polygon; so we first rotate the previous v
            # 90 degrees left, and then we choose whichever
            # direction along the new edge has a positive dot
            # product with this vector.
            vtmp = (-v[1], v[0])
            v = (-e[5],e[4])
            if v[0] * vtmp[0] + v[1] * vtmp[1] < 0:
                v = (e[5], -e[4])
            # Terminate the loop if we have returned to our
            # starting edge.
            if n == startn:
                break

        # Save everything we need to write out a 3D model later on.
        # In particular this involves keeping the coordinates of
        # the points, for which we will need to find the inverse of
        # the rotation matrix so as to put the points back where
        # they started.
        #
        # The inverse rotation matrix is
        #
        #  (  cos(-theta) sin(-theta) 0 ) (  cos(pi/2-phi)  0 sin(pi/2-phi) )
        #  ( -sin(-theta) cos(-theta) 0 ) (       0        1        0       )
        #  (      0            0      1 ) ( -sin(pi/2-phi)  0 cos(pi/2-phi) )
        #
        # which comes to
        #
        #  ( cos(theta)*sin(phi)  -sin(theta)  cos(theta)*cos(phi) )
        #  ( sin(theta)*sin(phi)   cos(theta)  sin(theta)*cos(phi) )
        #  (      -cos(phi)            0             sin(phi)      )
        
        imatrix = [
        [ cos(theta)*sin(phi),  -sin(theta),  cos(theta)*cos(phi) ],
        [ sin(theta)*sin(phi),   cos(theta),  sin(theta)*cos(phi) ],
        [      -cos(phi)     ,       0     ,        sin(phi)      ]]

        facelist = []
        for p in poly:
            xa, ya = p[0:2]
            za = 1
            xb = imatrix[0][0] * xa + imatrix[0][1] * ya + imatrix[0][2] * za
            yb = imatrix[1][0] * xa + imatrix[1][1] * ya + imatrix[1][2] * za
            zb = imatrix[2][0] * xa + imatrix[2][1] * ya + imatrix[2][2] * za
            planes = list(p[2:5])
            planes.sort()
            planes = tuple(planes)
            if planes not in vertices:
                vertices[planes] = []
            vertices[planes].append((xb, yb, zb))
            facelist.append(planes)

        faces.append((i, facelist))

    # Now output the polygon description.
    #
    # Each polygon has been prepared in its own frame of reference,
    # so the absolute coordinates of the vertices will vary
    # depending on which polygon they were prepared in. For this
    # reason I have kept _every_ version of the coordinates of each
    # vertex, so we can now average them into a single canonical value.
    pointDict = {}
    for key, value in vertices.items():
        xt = yt = zt = n = 0
        xxt = yyt = zzt = 0
        for x, y, z in value:
            xt = xt + x
            yt = yt + y
            zt = zt + z
            xxt = xxt + x*x
            yyt = yyt + y*y
            zzt = zzt + z*z
            n = n + 1
        pointDict[key] = (x0+scale*xt/n, y0+scale*yt/n, z0+scale*zt/n)

    faceList = []
    for i, vlist in faces:
        f = []
        for key in vlist:
            f.append(pointDict[key])
        faceList.append(f)

    return faceList

def genFacesVertex(points,x0,y0,z0,size):
    n = len(points)
    hulledges = {}
    for i in range(n-1):
        xi, yi, zi = points[i]
        for j in range(i+1, n):
            xj, yj, zj = points[j]

            # We begin by rotating our frame of reference so that both
            # points are in the x=0 plane, have the same z coordinate,
            # and that z coordinate is positive. In other words, we
            # rotate the sphere so that the radius bisecting the line
            # between the two points is the vector (0,0,1), and then
            # rotate around the z-axis so that the two points hit
            # opposite sides of the x-y plane. We expect to end up with
            # our two points being of the form (0,y,z) and (0,-y,z)
            # with z > 0.

            # Begin by rotating so that the midway point appears at
            # (0,0,1). To do this we must first find the midway point
            # and its polar coordinates...
            mx = (xi + xj) / 2
            my = (yi + yj) / 2
            mz = (zi + zj) / 2
            md = sqrt(mx**2 + my**2 + mz**2)
            # Very silly special case here: md might be zero. This
            # means that the midway point between the two points is the
            # origin, i.e. the points are exactly diametrically
            # opposite on the sphere. In this situation we can
            # legitimately pick _any_ point on the great circle half
            # way between them as a representative mid-way point; so
            # we'll simply take an arbitrary vector perpendicular to
            # point i.
            if md == 0:
                # We'll take the vector product of point i with some
                # arbitrarily chosen vector which isn't parallel to it.
                # I'll find the absolute-smallest of the three
                # coordinates of i, and choose my arbitrary vector to
                # be the corresponding basis vector.
                if abs(mx) <= abs(my) and abs(mx) <= abs(mz):
                    mx, my, mz = 0, -zi, yi
                elif abs(my) <= abs(mx) and abs(my) <= abs(mz):
                    mx, my, mz = zi, 0, -xi
                else: # abs(mz) <= abs(mx) and abs(mz) <= abs(my)
                    mx, my, mz = -yi, xi, 0
                # Now recompute the distance so we can normalise as
                # before.
                md = sqrt(mx**2 + my**2 + mz**2)
            mx = mx / md
            my = my / md
            mz = mz / md
            theta = atan2(my, mx)
            phi = asin(mz)
            # ... and construct a matrix which first rotates by -theta
            # about the z-axis, thus bringing the point to the
            # meridian, and then rotates by pi/2-phi about the y-axis
            # to bring the point to (0,0,1).
            #
            # That matrix is therefore
            #
            #  ( cos(pi/2-phi)  0 -sin(pi/2-phi) ) ( cos(-theta) -sin(-theta) 0 )
            #  (       0        1        0       ) ( sin(-theta)  cos(-theta) 0 )
            #  ( sin(pi/2-phi)  0  cos(pi/2-phi) ) (      0            0      1 )
            #
            # which comes to
            #
            #  ( cos(theta)*sin(phi)  sin(theta)*sin(phi)  -cos(phi) )
            #  (     -sin(theta)          cos(theta)           0     )
            #  ( cos(theta)*cos(phi)  sin(theta)*cos(phi)   sin(phi) )
            matrix1 = [
            [ cos(theta)*sin(phi),  sin(theta)*sin(phi),  -cos(phi) ],
            [     -sin(theta)    ,      cos(theta)     ,      0     ],
            [ cos(theta)*cos(phi),  sin(theta)*cos(phi),   sin(phi) ]]

            # Now pick an arbitrary point out of the two (point i will
            # do fine), rotate it via this matrix, determine its angle
            # psi from the y-axis, and construct the simple rotation
            # matrix
            #
            #  ( cos(-psi) -sin(-psi) 0 )
            #  ( sin(-psi)  cos(-psi) 0 )
            #  (     0          0     1 )
            #
            # which brings it back to the y-axis.
            xi1 = matrix1[0][0] * xi + matrix1[0][1] * yi + matrix1[0][2] * zi
            yi1 = matrix1[1][0] * xi + matrix1[1][1] * yi + matrix1[1][2] * zi
            # (no need to compute zi since we don't use it in this case)
            psi = atan2(-xi1, yi1)
            matrix2 = [
            [ cos(-psi), -sin(-psi), 0 ],
            [ sin(-psi),  cos(-psi), 0 ],
            [     0    ,      0    , 1 ]]

            # Now combine those matrices to produce the real one.
            matrix = []
            for y in range(3):
                mrow = []
                for x in range(3):
                    s = 0
                    for k in range(3):
                        s = s + matrix2[y][k] * matrix1[k][x]
                    mrow.append(s)
                matrix.append(mrow)

            # Test code to check that all that worked.
            #
            # This prints the transformed values of the two points, so
            # we can check that they have zero x coordinates, the y
            # coordinates are negatives of each other, and the z
            # coordinates are the same.
            #
            #xi1 = matrix[0][0] * xi + matrix[0][1] * yi + matrix[0][2] * zi
            #yi1 = matrix[1][0] * xi + matrix[1][1] * yi + matrix[1][2] * zi
            #zi1 = matrix[2][0] * xi + matrix[2][1] * yi + matrix[2][2] * zi
            #print (100000 + xi1) - 100000, yi1, zi1
            #xj1 = matrix[0][0] * xj + matrix[0][1] * yj + matrix[0][2] * zj
            #yj1 = matrix[1][0] * xj + matrix[1][1] * yj + matrix[1][2] * zj
            #zj1 = matrix[2][0] * xj + matrix[2][1] * yj + matrix[2][2] * zj
            #print (100000 + xj1) - 100000, yj1, zj1
            #
            # And this computes the product of the matrix and its
            # transpose, which should come to the identity matrix since
            # it's supposed to be orthogonal.
            #
            #testmatrix = []
            #for y in range(3):
            #    mrow = []
            #    for x in range(3):
            #       s = 0
            #       for k in range(3):
            #           s = s + matrix[y][k] * matrix[x][k]
            #       mrow.append((10000000 + s) - 10000000)
            #    testmatrix.append(mrow)
            #print testmatrix

            # Whew. So after that moderately hairy piece of linear
            # algebra, we can now transform our point set so that when
            # projected into the x-z plane our two chosen points become
            # 1. Do so.
            ppoints = []
            for k in range(n):
                xk, yk, zk = points[k]
                xk1 = matrix[0][0] * xk + matrix[0][1] * yk + matrix[0][2] * zk
                #yk1 = matrix[1][0] * xk + matrix[1][1] * yk + matrix[1][2] * zk
                zk1 = matrix[2][0] * xk + matrix[2][1] * yk + matrix[2][2] * zk
                ppoints.append((xk1, zk1))

            # The point of all that was to produce a plane projection
            # of the point set, under which the entire edge we're
            # considering becomes a single point. Now what we do is to
            # see whether that _point_ is on the 2-D convex hull of the
            # projected point set.
            #
            # To do this we will go through all the other points and
            # figure out their bearings from the fulcrum point. Then
            # we'll sort those bearings into angle order (which is of
            # course cyclic modulo 2pi). If the fulcrum is part of the
            # convex hull, we expect there to be a gap of size > pi
            # somewhere in that set of angles, indicating that a line
            # can be drawn through the fulcrum at some angle such that
            # all the other points are on the same side of it.

            # First, compensate for any rounding errors in the above
            # linear algebra by averaging the (theoretically exactly
            # equal) projected coordinates of points i and j to get
            # coords which we will use as our canonical fulcrum.
            fx = (ppoints[i][0] + ppoints[j][0]) / 2
            fz = (ppoints[i][1] + ppoints[j][1]) / 2
            # Now find the list of angles.
            angles = []
            for k in range(n):
                if k == i or k == j: continue
                x, z = ppoints[k]
                angle = atan2(z - fz, x - fx)
                angles.append(angle)
            # Sort them.
            angles.sort()
            # Now go through and look for a gap of size pi. There are
            # two possible ways this can happen: either two adjacent
            # elements in the list are separated by more than pi, or
            # the two end elements are separated by _less_ than pi.
            hull = 0
            for k in range(len(angles)-1):
                if angles[k+1] - angles[k] > pi:
                    hull = 1
                    break
            if angles[-1] - angles[0] < pi:
                hull = 1

            if hull:
                hulledges[(i,j)] = 1

    # Now we know the set of edges involved in the polyhedron, we need
    # to combine them into faces. To do this we will have to consider
    # each edge, going _both_ ways.
    followedges = {}
    for i in range(n):
        xi, yi, zi = points[i]
        for j in range(n):
            xj, yj, zj = points[j]
            if i == j: continue
            if not ((i,j) in hulledges or (j,i) in hulledges): continue

            # So we have an edge from point i to point j. We imagine we
            # are walking along that edge from i to j with the
            # intention of circumnavigating the face to our left. So
            # when we reach j, we must turn left on to another edge,
            # and the question is which edge that is.
            #
            # To do this we will begin by rotating so that point j is
            # at (0,0,1). This has been done in several other parts of
            # this code base so I won't comment it in full yet again...
            theta = atan2(yj, xj)
            phi = asin(zj)
            matrix = [
            [ cos(theta)*sin(phi),  sin(theta)*sin(phi),  -cos(phi) ],
            [     -sin(theta)    ,      cos(theta)     ,      0     ],
            [ cos(theta)*cos(phi),  sin(theta)*cos(phi),   sin(phi) ]]

            # Now we are looking directly down on point j. We can see
            # some number of convex-hull edges coming out of it; we
            # determine the angle at which each one emerges, and find
            # the one which is closest to the i-j edge on the left.
            angles = []
            for k in range(n):
                if k == j: continue
                if not ((k,j) in hulledges or (j,k) in hulledges):
                    continue
                xk, yk, zk = points[k]
                xk1 = matrix[0][0] * xk + matrix[0][1] * yk + matrix[0][2] * zk
                yk1 = matrix[1][0] * xk + matrix[1][1] * yk + matrix[1][2] * zk
                #zk1 = matrix[2][0] * xk + matrix[2][1] * yk + matrix[2][2] * zk
                angles.append((atan2(xk1, yk1), k))
            # Sort by angle, in reverse order.
            angles.sort(key=lambda x : -x[0])
            # Search for i and take the next thing below it. Wrap
            # round, of course: if angles[0] is i then we want
            # angles[-1]. Conveniently this will be done for us by
            # Python's array semantics :-)
            k = None
            for index in range(len(angles)):
                if angles[index][1] == i:
                    k = angles[index-1][1]
                    break
            assert k != None
            followedges[(i,j)] = (j,k)

    # Now we're about ready to output our polyhedron definition. The
    # only thing we're missing is the surface normals, and we'll do
    # those as we go along.

    # Now, the faces. We'll simply delete entries from followedges() as
    # we go around, so as to avoid doing any face more than once.
    faceList = []

    while len(followedges) > 0:
        # Pick an arbitrary key in followedges.
        start = this = list(followedges.keys())[0]
        vertices = []
        while 1:
            p = points[this[0]]
            vertices.append((x0+size*p[0],y0+size*p[1],z0+size*p[2]))
            next = followedges[this]
            del followedges[this]
            this = next
            if this == start:
                break
        faceList.append(vertices)

    return faceList


def polyhedron(d,n,faceMode,x,y,z,size,faceBlock,edgeBlock=None):
    print("Generating points")
    points = makePoints(n)
    if faceMode:
        print("Generating faces with face construction")
        faces = genFacesFace(points,x,y,z,size/2)
    else:
        print("Generating faces with vertex construction")
        faces = genFacesVertex(points,x,y,z,size/2)
    print("Drawing faces")
    for face in faces:
        d.face(face,faceBlock)
    print("Drawing edges")
    if edgeBlock:
        for face in faces:
            prev = face[-1]
            for vertex in face:
                d.line(prev[0],prev[1],prev[2],vertex[0],vertex[1],vertex[2],edgeBlock)
                prev = vertex

if __name__ == "__main__":
    import mcpi.block as block
    
    d = drawing.Drawing()

    if len(sys.argv)>1:
        n = int(sys.argv[1])
    else:
        n = 7

    faceMode = len(sys.argv)>2 and sys.argv[2][0] == "f"

    if len(sys.argv)>3:
        size = int(sys.argv[3])
    else:
        size = 50

    pos = d.mc.player.getPos()
    polyhedron(d,n,faceMode,pos.x, pos.y, pos.z, size, block.GLASS, block.STONE)

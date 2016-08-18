#
# Code by Alexander Pruss and under the MIT license
#

from mineturtle import *

def tree(depth):
    t.up(30)
    t.go(20)
    if depth > 1:
       tree(depth-1)
    t.back(20)
    t.down(60)
    t.go(20)
    if depth > 1:
       tree(depth-1)
    t.back(20)
    t.up(30)

t = Turtle()
t.follow()
t.verticalangle(90)
t.pendelay(0)
t.go(20)
tree(5)

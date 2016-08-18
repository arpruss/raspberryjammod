#
# Code by Alexander Pruss and under the MIT license
#

from mineturtle import *
t = Turtle()
t.pendelay(0)
t.turtle(None)

def tree(counter,branchLen):
  if counter == 0:
    return
  t.go(branchLen)
  for i in range(4):
    t.pitch(30)
    tree(counter-1,branchLen*0.75)
    t.pitch(-30)
    t.roll(90)
  t.back(branchLen)

t.penblock(block.WOOD)
t.verticalangle(90)
tree(6,20)
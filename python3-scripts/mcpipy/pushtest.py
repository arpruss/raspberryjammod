from turtle import *

t = Turtle()
t.turtle(HORSE)

for i in range(5):
  z = t.save()
  t.go(10)
  t.restore(z)
  t.right(30)
t.turtle(None)

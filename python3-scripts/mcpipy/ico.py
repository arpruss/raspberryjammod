from turtle import *
import random

t = Turtle()
t.pendelay(0)
t.turtle(None)

def teta():
  t.roll(120)

def tetb():
  t.pitch(109.47122064)
  t.roll(120)
  t.pitch(-109.47122064)
  
def a():
  t.roll(72)

def b():
  t.pitch(63.4349488)
  t.roll(72)
  t.pitch(-63.4349488)

def draw():
  t.go(20)
  t.back(20)

while(True):
  if random.random() < 0.5:
      a()
  else:
      b()
  draw()
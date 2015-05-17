from turtle import *
t = Turtle()
t.penblock(GOLD_BLOCK)
t.pendelay(0)
for i in range(7):
    t.go(50)
    t.up(180.-180./7)

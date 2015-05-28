# defective for some reason!
import lsystem
from turtle import *
t = Turtle()
t.pendelay(0)
t.turtle(None)
t.penblock(STAINED_GLASS_PURPLE)

rules = { 'M': 'OA++pA----NA[-OA----MA]++',
          'N': '+OA--PA[---MA--NA]+',
          'O': '-MA++NA[+++OA++PA]-',
          'P': '--OA++++MA[+PA++++NA]--NA',
          'A': '' }
axiom = '[N]++[N]++[N]++[N]++[N]'

dictionary = {
  'A': lambda: t.go(20),
  '+': lambda: t.right(36),
  '-': lambda: t.left(36),
  '[': lambda: t.push(),
  ']': lambda: t.pop()
  }

lsystem.lsystem(axiom, rules, dictionary, 5)

#
# Copyright (c) 2015 Alexander Pruss
# L-system with turtle graphics
#

from turtle import *

def playProgram(s, dictionary):
    for c in s:
        if c in dictionary:
            dictionary[c]()

def evolve(axiom, rules, levelCount):
    for i in range(levelCount):
        for r in rules:
            axiom = axiom.replace(r[0], r[1])
    return axiom


def lsystem(axiom, rules, dictionary, levelCount):
    out = evolve(axiom, rules, levelCount)
    playProgram(out, dictionary)

if __name__ == "__main__":
    t = Turtle()
    t.pendelay(0)
    t.penup()
    t.turtle(None)
    t.go(10)
    t.verticalangle(90)
    t.pendown()
    t.penblock(WOOD)

# a fairly simple example with rules from http://www.nbb.cornell.edu/neurobio/land/OldStudentProjects/cs490-94to95/hwchen/
#    rules = [('F','F[-&<F][<++&F]||F[--&>F][+&F]')]
#
#    angle = 22.5
#
#    dictionary = {
#        '[': t.push,
#        ']': t.pop,
#        'F': lambda: t.go(5),
#        '-': lambda: t.yaw(-angle),
#        '+': lambda: t.yaw(angle),
#        '&': lambda: t.pitch(angle),
#        '^': lambda: t.pitch(-angle),
#        '<': lambda: t.roll(-angle),
#        '>': lambda: t.roll(angle),
#        '|': lambda: t.pitch(180)
#        }
#
#    lsystem('F', rules, dictionary, 3)


#
# A more complex example with 
# rules from http://www.geekyblogger.com/2008/04/tree-and-l-system.html
#     
    rules = [('A','^fB>>>B>>>>>B'), ('B','[^^f>>>>>>A]')]
              
    axiom = 'fA'
    angle = 15
    thickness = 8
    length = 15
    material = WOOD
    t.penwidth(thickness)
    t.penblock(material)

    stack = []
    def push():
        global length
        global thickness
        stack.append((length,thickness))
        t.push()
        thickness = thickness * 0.6
        length = length * 0.75
        if thickness < 1:
            thickness = 1
        if length <= 1:
            t.penblock(LEAVES)
        t.penwidth(thickness)

    def pop():
        global length
        global thickness
        length,thickness = stack.pop()
        t.pop()

    dictionary = {
        '[': push,
        ']': pop,
        '^': lambda: t.pitch(angle),
        '>': lambda: t.roll(angle),
        'f': lambda: t.go(length)
    }

    lsystem(axiom, rules, dictionary, 10)

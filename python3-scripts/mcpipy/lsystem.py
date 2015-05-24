#
# Copyright (c) 2015 Alexander Pruss
# L-system with turtle graphics
#

from turtle import *

def playProgram(s, dictionary):
    for c in s:
        if c in dictionary:
            dictionary[c]()

#
# if the rules are a dictionary, all substitutions are done simultaneously
# otherwise, the substitutions are done in sequence
#
# I think simultaneous substitution is the proper L-system way, but the 
# Geeky Blogger tree looks better, and more like Geeky Blogger's picture 
# when done sequentially.
#
def evolve(axiom, rules, levelCount):
    for i in range(levelCount):
        if isinstance(rules, dict):
            out = ""
            for c in axiom:
                if c in rules:
                    out += rules[c]
                else:
                    out += c
            axiom = out
        else:
            for rule in rules:
                axiom = axiom.replace(rule[0], rule[1])

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
#    rules = {'F':'F[-&<F][<++&F]||F[--&>F][+&F]'}
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
    rules = (('A','^fB>>>B>>>>>B'), ('B','[^^f>>>>>>A]'))

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

    lsystem(axiom, rules, dictionary, 11)
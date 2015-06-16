#Martin O'Hanlon
#www.stuffaboutcode.com
#Minecraft Turtle Example
import minecraftturtle
import mcpi.minecraft as minecraft
import mcpi.block as block


def f(turtle, length, depth):
   if depth == 0:
     turtle.forward(length)
   else:
     f(turtle, length/3, depth-1)
     turtle.right(60)
     f(turtle, length/3, depth-1)
     turtle.left(120)
     f(turtle, length/3, depth-1)
     turtle.right(60)
     f(turtle, length/3, depth-1)

#create connection to minecraft
mc = minecraft.Minecraft.create()

#get players position
pos = mc.player.getPos()

#create minecraft turtle
steve = minecraftturtle.MinecraftTurtle(mc, pos)

#set speed
steve.speed(0)

#fractal
f(steve, 500, 6)


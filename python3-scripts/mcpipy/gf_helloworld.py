#! /usr/bin/python
from . import mcpi.minecraft as minecraft
from . import server

""" hello world test app

    @author: goldfish"""

mc = minecraft.Minecraft.create( server.address )
mc.postToChat("Hello, Minecraft!")

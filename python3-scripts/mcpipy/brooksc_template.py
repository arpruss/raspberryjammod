#!/usr/bin/env python

#import the minecraft.py module from the minecraft directory
from . import mcpi.minecraft as minecraft
#import minecraft block module
from . import mcpi.block as block
#import time, so delays can be used
from . import server

def main():
    mc = minecraft.Minecraft.create(server.address)
    # write the rest of your code here...
    mc.postToChat("Hello MCPIPY World!")


if __name__ == "__main__":
    main()

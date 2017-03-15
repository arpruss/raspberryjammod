#
# Code by Alexander Pruss and under the MIT license
#

import mcpi.block as block
from random import uniform
import math
import colors

opaqueBlocks = [
  block.BONE_BLOCK,
  block.CLAY,
  block.COAL_BLOCK,
  block.COAL_ORE,
  block.DIRT_COARSE,
  block.DIAMOND_BLOCK,
  block.DIAMOND_ORE,
  block.DIRT,
  block.EMERALD_BLOCK,
  block.EMERALD_ORE,
  block.END_BRICKS,
  block.END_STONE,
  block.GOLD_BLOCK,
  block.GOLD_ORE,
  block.HARDENED_CLAY,
  block.HARDENED_CLAY_STAINED_BLACK,
  block.HARDENED_CLAY_STAINED_BLUE,
  block.HARDENED_CLAY_STAINED_BROWN,
  block.HARDENED_CLAY_STAINED_CYAN,
  block.HARDENED_CLAY_STAINED_GRAY,
  block.HARDENED_CLAY_STAINED_GREEN,
  block.HARDENED_CLAY_STAINED_LIGHT_BLUE,
  block.HARDENED_CLAY_STAINED_LIME,
  block.HARDENED_CLAY_STAINED_MAGENTA,
  block.HARDENED_CLAY_STAINED_ORANGE,
  block.HARDENED_CLAY_STAINED_PINK,
  block.HARDENED_CLAY_STAINED_PURPLE,
  block.HARDENED_CLAY_STAINED_RED,
  block.HARDENED_CLAY_STAINED_LIGHT_GRAY,
  block.HARDENED_CLAY_STAINED_WHITE,
  block.HARDENED_CLAY_STAINED_YELLOW,
  block.ICE_PACKED,
  block.IRON_BLOCK,
  block.IRON_ORE,
  block.LAPIS_LAZULI_BLOCK,
  block.LAPIS_LAZULI_ORE,
  block.NETHERRACK,
  block.NETHER_WART_BLOCK,
  block.NOTEBLOCK,
  block.OBSIDIAN,
  block.WOOD_PLANKS_ACACIA,
  block.WOOD_PLANKS_DARK_OAK,
  block.WOOD_PLANKS_BIRCH,
  block.WOOD_PLANKS_JUNGLE,
  block.WOOD_PLANKS_OAK,
  block.WOOD_PLANKS_SPRUCE,
  block.PRISMARINE_BRICKS,
  block.PRISMARINE_DARK,
  block.PRISMARINE,
  block.PURPUR_BLOCK,
  block.QUARTZ_BLOCK,
  block.REDSTONE_BLOCK,
  block.REDSTONE_ORE,
  block.RED_NETHER_BRICK,
  block.RED_SANDSTONE_SMOOTH,
  block.SANDSTONE_SMOOTH,
  block.SLIME_BLOCK,
  block.SOUL_SAND,
  block.SPONGE,
  block.STONE,
  block.STONE_ANDESITE,
  block.STONE_ANDESITE_SMOOTH,
  block.STONE_DIORITE,
  block.STONE_DIORITE_SMOOTH,
  block.STONE_GRANITE,
  block.STONE_GRANITE_SMOOTH,
  block.WOOL_BLACK,
  block.WOOL_BLUE,
  block.WOOL_BROWN,
  block.WOOL_CYAN,
  block.WOOL_GRAY,
  block.WOOL_GREEN,
  block.WOOL_LIGHT_BLUE,
  block.WOOL_LIME,
  block.WOOL_MAGENTA,
  block.WOOL_ORANGE,
  block.WOOL_PINK,
  block.WOOL_PURPLE,
  block.WOOL_RED,
  block.WOOL_LIGHT_GRAY,
  block.WOOL_WHITE,
  block.WOOL_YELLOW
];

translucentBlocks = [
  block.STAINED_GLASS_BLACK,
  block.STAINED_GLASS_BLUE,
  block.STAINED_GLASS_BROWN,
  block.STAINED_GLASS_CYAN,
  block.STAINED_GLASS_GRAY,
  block.STAINED_GLASS_GREEN,
  block.STAINED_GLASS_LIGHT_BLUE,
  block.STAINED_GLASS_LIME,
  block.STAINED_GLASS_MAGENTA,
  block.STAINED_GLASS_ORANGE,
  block.STAINED_GLASS_PINK,
  block.STAINED_GLASS_PURPLE,
  block.STAINED_GLASS_RED,
  block.STAINED_GLASS_LIGHT_GRAY,
  block.STAINED_GLASS_WHITE,
  block.STAINED_GLASS_YELLOW,
];

def toPalette(blocks):
    palette = []
    for b in blocks:
        palette.append((b,b.getRGBA()[0:3]))
    return palette

opaquePalette = toPalette(opaqueBlocks)
translucentPalette = toPalette(translucentBlocks)

def rgbDist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

def rgbToBlock(rgb, palette=opaquePalette, randomDither=None):
    if randomDither is not None:
        rgb = (rgb[0]+uniform(-randomDither,randomDither),
                rgb[1]+uniform(-randomDither,randomDither),
                rgb[2]+uniform(-randomDither,randomDither))
    bestColor = palette[0]
    bestDist = 255*3
    for c in palette:
        d = rgbDist(c[1],rgb)
        if d < bestDist:
            bestDist = d
            bestColor = c
    return bestColor
    
def hsvToRGB(h,s,v):
    h %= 360.
    c = v * s 
    x = c * (1-abs( ((h/60.) % 2.)  - 1 ))
    m = v - c 
    if 0 <= h < 60:
        r,g,b = (c,x,0)
    elif 60 <= h < 120:
        r,g,b = (x,c,0)
    elif 120 <= h < 180:
        r,g,b = (0,c,x)
    elif 180 <= h < 240:
        r,g,b = (0,x,c)
    elif 240 <= h < 300:
        r,g,b = (x,0,c)
    else:
        r,g,b = (c,0,x)
    return (int((r+m)*255), int((g+m)*255), int((b+m)*255))
    
class DitheringMethod(object):
    def __init__(self, rng=None, fs=False):
        self.rng = rng
        self.fs = fs
        
    def isEmpty(self):
        return self.rng is None and not self.fs
    
def imageToBlocks(getPixel, width, height, palette=opaquePalette, dither=None):
    if dither is None or dither.isEmpty():
        for x in range(width):
            for y in range(height):
                yield x,y,rgbToBlock(getPixel((x,y)), palette=palette)
    elif dither.rng is not None:
        for x in range(width):
            for y in range(height):
                rgb = getPixel((x,y))
                yield x,y,rgbToBlock((rgb[0]+dither.rng(),rgb[1]+dither.rng(),rgb[2]+dither.rng()), palette=palette)
    elif dither.fs:
        pixels = tuple(tuple(list(getPixel((x,y))) for y in range(height)) for x in range(width))
        for x in range(width):
            for y in range(height):
                block,actualRGB = rgbToBlock(pixels[x][y], palette=palette)
                yield x,y,block
                for i in range(3):
                    err = pixels[x][y][i] - actualRGB[i]
                    if x + 1 < width:
                        pixels[x+1][y][i] += err * 7 // 16
                    if y + 1 < height:
                        if 0 < x:
                            pixels[x-1][y+1][i] += err * 3 // 16
                        pixels[x][y+1][i] += err * 5 // 16
                        if x + 1 < width:
                            pixels[x+1][y+1][i] += err // 16
    else:
        raise ValueError('Unknown dithering algorithm')

if __name__ == '__main__':
    from mine import Minecraft
    
    mc = Minecraft()
    pos = mc.player.getTilePos()
    
    r = 50
    cx = pos.x
    cy = pos.y + r
    cz = pos.z
    
    for x in range(-r,r+1):
        for y in range(-r,r+1):
            d = math.sqrt(x*x+y*y)/r
            if d<=1:
                if x == 0 and y == 0:
                    theta = 0
                else:
                    theta = math.atan2(y,x) * 180. / math.pi
                rgb = hsvToRGB(theta, d, 1)
                mc.setBlock(cx+x,cy+y,cz,rgbToBlock(rgb, randomDither=30))

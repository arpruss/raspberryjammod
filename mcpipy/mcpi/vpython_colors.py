import mcpi.block as block
from random import uniform
import math

opaquePalette=[
  (block.BONE_BLOCK, (225, 221, 201)),
  (block.CLAY, (159, 164, 177)),
  (block.COAL_BLOCK, (19, 19, 19)),
  (block.COAL_ORE, (115, 115, 115)),
  (block.DIRT_COARSE, (119, 86, 59)),
  (block.DIAMOND_BLOCK, (98, 219, 214)),
  (block.DIAMOND_ORE, (129, 140, 143)),
  (block.DIRT, (134, 96, 67)),
  (block.EMERALD_BLOCK, (81, 217, 117)),
  (block.EMERALD_ORE, (110, 129, 116)),
  (block.END_BRICKS, (226, 231, 171)),
  (block.END_STONE, (221, 224, 165)),
  (block.GOLD_BLOCK, (249, 236, 79)),
  (block.GOLD_ORE, (143, 140, 125)),
  (block.HARDENED_CLAY, (151, 93, 67)),
  (block.HARDENED_CLAY_STAINED_BLACK, (37, 23, 16)),
  (block.HARDENED_CLAY_STAINED_BLUE, (74, 60, 91)),
  (block.HARDENED_CLAY_STAINED_BROWN, (77, 51, 36)),
  (block.HARDENED_CLAY_STAINED_CYAN, (87, 91, 91)),
  (block.HARDENED_CLAY_STAINED_GRAY, (58, 42, 36)),
  (block.HARDENED_CLAY_STAINED_GREEN, (76, 83, 42)),
  (block.HARDENED_CLAY_STAINED_LIGHT_BLUE, (113, 109, 138)),
  (block.HARDENED_CLAY_STAINED_LIME, (104, 118, 53)),
  (block.HARDENED_CLAY_STAINED_MAGENTA, (150, 88, 109)),
  (block.HARDENED_CLAY_STAINED_ORANGE, (162, 84, 38)),
  (block.HARDENED_CLAY_STAINED_PINK, (162, 78, 79)),
  (block.HARDENED_CLAY_STAINED_PURPLE, (118, 70, 86)),
  (block.HARDENED_CLAY_STAINED_RED, (143, 61, 47)),
  (block.HARDENED_CLAY_STAINED_LIGHT_GRAY, (135, 107, 98)),
  (block.HARDENED_CLAY_STAINED_WHITE, (210, 178, 161)),
  (block.HARDENED_CLAY_STAINED_YELLOW, (186, 133, 35)),
  (block.ICE_PACKED, (165, 195, 245)),
  (block.IRON_BLOCK, (219, 219, 219)),
  (block.IRON_ORE, (136, 130, 127)),
  (block.LAPIS_LAZULI_BLOCK, (39, 67, 138)),
  (block.LAPIS_LAZULI_ORE, (102, 112, 135)),
  (block.NETHERRACK, (111, 54, 53)),
  (block.NETHER_WART_BLOCK, (117, 6, 7)),
  (block.NOTEBLOCK, (101, 68, 51)),
  (block.OBSIDIAN, (20, 18, 30)),
  (block.WOOD_PLANKS_ACACIA, (169, 92, 51)),
  (block.WOOD_PLANKS_DARK_OAK, (61, 40, 18)),
  (block.WOOD_PLANKS_BIRCH, (196, 179, 123)),
  (block.WOOD_PLANKS_JUNGLE, (154, 110, 77)),
  (block.WOOD_PLANKS_OAK, (157, 128, 79)),
  (block.WOOD_PLANKS_SPRUCE, (104, 78, 47)),
  (block.PRISMARINE_BRICKS, (100, 160, 143)),
  (block.PRISMARINE_DARK, (60, 88, 75)),
  (block.PRISMARINE, (100, 152, 142)),
  (block.PURPUR_BLOCK, (166, 122, 166)),
  (block.QUARTZ_BLOCK, (236, 233, 226)),
  (block.REDSTONE_BLOCK, (171, 28, 9)),
  (block.REDSTONE_ORE, (133, 107, 107)),
  (block.RED_NETHER_BRICK, (68, 4, 7)),
  (block.RED_SANDSTONE_SMOOTH, (168, 86, 31)),
  (block.SANDSTONE_SMOOTH, (220, 212, 162)),
  (block.SLIME_BLOCK, (121, 200, 101)),
  (block.SOUL_SAND, (85, 64, 52)),
  (block.SPONGE, (195, 196, 85)),
  (block.STONE, (125, 125, 125)),
  (block.STONE_ANDESITE, (131, 131, 131)),
  (block.STONE_ANDESITE_SMOOTH, (133, 133, 135)),
  (block.STONE_DIORITE, (180, 180, 183)),
  (block.STONE_DIORITE_SMOOTH, (183, 183, 186)),
  (block.STONE_GRANITE, (153, 114, 99)),
  (block.STONE_GRANITE_SMOOTH, (159, 115, 98)),
  (block.WOOL_BLACK, (26, 22, 22)),
  (block.WOOL_BLUE, (46, 57, 142)),
  (block.WOOL_BROWN, (79, 51, 31)),
  (block.WOOL_CYAN, (47, 111, 137)),
  (block.WOOL_GRAY, (64, 64, 64)),
  (block.WOOL_GREEN, (53, 71, 27)),
  (block.WOOL_LIGHT_BLUE, (107, 138, 201)),
  (block.WOOL_LIME, (66, 174, 57)),
  (block.WOOL_MAGENTA, (180, 81, 189)),
  (block.WOOL_ORANGE, (219, 125, 63)),
  (block.WOOL_PINK, (208, 132, 153)),
  (block.WOOL_PURPLE, (127, 62, 182)),
  (block.WOOL_RED, (151, 52, 49)),
  (block.WOOL_LIGHT_GRAY, (155, 161, 161)),
  (block.WOOL_WHITE, (222, 222, 222)),
  (block.WOOL_YELLOW, (177, 166, 39)),
]

translucentPalette=[
  (block.STAINED_GLASS_BLACK, (25, 25, 25)),
  (block.STAINED_GLASS_BLUE, (51, 76, 178)),
  (block.STAINED_GLASS_BROWN, (102, 76, 51)),
  (block.STAINED_GLASS_CYAN, (76, 127, 153)),
  (block.STAINED_GLASS_GRAY, (76, 76, 76)),
  (block.STAINED_GLASS_GREEN, (102, 127, 51)),
  (block.STAINED_GLASS_LIGHT_BLUE, (102, 153, 216)),
  (block.STAINED_GLASS_LIME, (127, 204, 25)),
  (block.STAINED_GLASS_MAGENTA, (178, 76, 216)),
  (block.STAINED_GLASS_ORANGE, (216, 127, 51)),
  (block.STAINED_GLASS_PINK, (242, 127, 165)),
  (block.STAINED_GLASS_PURPLE, (127, 63, 178)),
  (block.STAINED_GLASS_RED, (153, 51, 51)),
  (block.STAINED_GLASS_LIGHT_GRAY, (153, 153, 153)),
  (block.STAINED_GLASS_WHITE, (255, 255, 255)),
  (block.STAINED_GLASS_YELLOW, (229, 229, 51)),
  (block.GLASS, (60, 67, 68)),
]

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
    from mc import Minecraft
    
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

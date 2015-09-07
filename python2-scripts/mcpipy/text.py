#
# Code under the MIT license by Alexander R. Pruss
#

import sys
import time
import mcpi.minecraft as minecraft

# vectors must be minecraft.Vec3
def drawGlyph(mc, pos, forwardVec, upVec, glyph, foreground, background=None):
    bitmap = glyph[3]
    height = len(bitmap)
    width = glyph[0]
    offset = glyph[1]
    delta = glyph[2]

    for i in range(height):
        pixelPos = pos + upVec*(height-1-i) + forwardVec*offset
        for j in range(width):
            if not foreground is None and 0 != bitmap[i] & (1 << (width-1-j)):
                mc.setBlock(pixelPos, foreground)
            elif not background is None and 0 == bitmap[i] & (1 << (width-1-j)):
                mc.setBlock(pixelPos, background)
            pixelPos += forwardVec
    return pos + forwardVec*delta


def drawText(mc, font, pos, forwardVec, upVec, text, foreground, background=None):
    try:
        text = text.decode("cp1252")
    except:
        text = text.decode("iso8859_1")
    pixelPos = pos.clone()
    height = len(font[32][3])
    numLines = text.count("\n")+1
    pixelPos += upVec * ((numLines-1) * height)
    lineStart = pixelPos.clone()
    for c in text:
        value = ord(c)

        if value == 10:
            lineStart += upVec * (-height)
            pixelPos = lineStart.clone()
        else:
            try:
               glyph = font[value]
            except:
               glyph = font[32]
            pixelPos = drawGlyph(mc, pixelPos, forwardVec, upVec, glyph, foreground, background)
    return pixelPos

def angleToTextDirectionCardinal(angle):
    return angleToTextDirection(90 * round(angle/90))

def angleToTextDirection(angle):
    direction = int(round((angle % 360) / 45))
    if direction == 0:
        return minecraft.Vec3(-1,0,0)
    elif direction == 1:
        return minecraft.Vec3(-1,0,-1)
    elif direction == 2:
        return minecraft.Vec3(0,0,-1)
    elif direction == 3:
        return minecraft.Vec3(1,0,-1)
    elif direction == 4:
        return minecraft.Vec3(1,0,0)
    elif direction == 5:
        return minecraft.Vec3(1,0,1)
    elif direction == 6:
        return minecraft.Vec3(0,0,1)
    else:
        return minecraft.Vec3(-1,0,1)

if __name__ == '__main__':
    import fonts
    import mcpi.block as block

    mc = minecraft.Minecraft()
    pos = mc.player.getPos()
    forward = angleToTextDirection(mc.player.getRotation())
    foreground = 169 # sea lantern
    background = block.OBSIDIAN

    if len(sys.argv) <= 1:
        text = "Hello, world!\nWelcome to Minecraft."
    else:
        del sys.argv[0]
        text = " ".join(sys.argv)

    drawText(mc, fonts.FONTS['tallfont'], pos, forward, minecraft.Vec3(0,1,0), text, foreground, background)

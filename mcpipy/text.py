#
# Code under the MIT license by Alexander R. Pruss
#

import sys
import time
import mcpi.minecraft as minecraft

ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER = 2

# vectors must be minecraft.Vec3
def drawGlyph(mc, pos, forwardVec, upVec, glyph, foreground, background=None, buffer=None):
    bitmap = glyph[3]
    height = len(bitmap)
    width = glyph[0]
    offset = glyph[1]
    delta = glyph[2]

    for i in range(height):
        pixelPos = pos + upVec*(height-1-i) + forwardVec*offset
        for j in range(width):
            if foreground is not None and 0 != bitmap[i] & (1 << (width-1-j)):
                if buffer is not None:
                    buffer[(pixelPos.x,pixelPos.y,pixelPos.z)] = foreground
                else:
                    mc.setBlock(pixelPos, foreground)
            elif background is not None and 0 == bitmap[i] & (1 << (width-1-j)):
                if buffer is not None:
                    buffer[(pixelPos.x,pixelPos.y,pixelPos.z)] = background
                else:
                    mc.setBlock(pixelPos, background)
            pixelPos += forwardVec
    return pos + forwardVec*delta

def textLength(font, text):
    l = 0
    for value in text:
        try:
           glyph = font[value]
        except:
           glyph = font[32]
        l += glyph[2]
    return l

def drawText(mc, font, pos, forwardVec, upVec, text, foreground=None, background=None, align=ALIGN_LEFT, buffer=None):
    try:
        text = bytearray(text.encode("cp1252"))
    except:
        text = bytearray(text.encode("iso8859_1"))
    pixelPos = pos.clone()
    height = len(font[32][3])
    lines = text.split(b'\n')
    pixelPos += upVec * ((len(lines)-1)* height)
    lineStart = pixelPos.clone()
    for line in lines:
        pixelPos = lineStart.clone()
        if align == ALIGN_RIGHT:
            pixelPos -= forwardVec * textLength(font, line)
        elif align == ALIGN_CENTER:
            pixelPos -= forwardVec * (0.5 * textLength(font, line))
                
        for value in line:
            try:
               glyph = font[value]
            except:
               glyph = font[32]
            pixelPos = drawGlyph(mc, pixelPos, forwardVec, upVec, glyph, foreground, background, buffer)

        lineStart += upVec * (-height)
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
    foreground = block.SEA_LANTERN
    background = block.OBSIDIAN

    if len(sys.argv) <= 1:
        text = "Hello, world!\nWelcome to Minecraft."
    else:
        del sys.argv[0]
        text = " ".join(sys.argv)

    drawText(mc, fonts.FONTS['metrix7pt'], pos, forward, minecraft.Vec3(0,1,0), text, foreground, background, align=ALIGN_RIGHT)

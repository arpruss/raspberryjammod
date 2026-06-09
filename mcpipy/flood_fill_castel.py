from mine import *
from mineturtle import *

castle_2 = {
    "fill":[ 
          {"pos":(-230,0,0), "material":block.GRASS } 
        , {"pos":(-230,0,-300), "material":block.GRASS } 
        , {"pos":(0,0,-350), "material":block.WATER_STATIONARY } 
        , {"pos":(100,5,-50), "material":block.END_BRICKS } 
        , {"pos":(100,10,-50), "material":block.END_BRICKS } 
        , {"pos":(100,15,-50), "material":block.END_BRICKS } 
    ],
    "walls": [ 
          { "height":5, "material":block.END_BRICKS, "angle":0, "trans":(-240,0,-410), "length":160, "depth":0, "koch_flake":"FLFLFLFLFLF"}
        , { "height":1, "material":block.END_BRICKS, "angle":0, "trans":(370,0,-510), "length":230, "depth":2, "koch_flake":"FLFRFLFLFLFRFLFRFLFRFLFLFLFRFLFRFLFRFLFLFLFRFLFRFLFRFLFLFLFRFLFRFLFRFLFLFLFRFLFRFLFRFLFLFLFRFLF"}
        , { "height":16, "material":block.END_BRICKS, "angle":30, "trans":(-85,0,-165), "length":85, "depth":1, "koch_flake":"FLFRFLFLFLFRFLFLFLFRFLFLFLFRFLFLFLFRFLFLFLFRFLF"}
        , { "height":16, "material":block.END_BRICKS, "angle":30, "trans":(110,0,-160), "length":20, "depth":0, "koch_flake":"FLFLFLFLFLF"} 
        ]
    }

def DrawCastle(mc, fred, castle, scale=1.0):
    pos = mc.player.getPos()
    fred.goto(pos.x, pos.y, pos.z)
    fred.angle(0.0)
    fred_default = fred.save()

    for wall in castle["walls"]:
        fred.penblock(wall["material"])
        for height in range(wall["height"]):
            fred.penup()
            fred.restore(fred_default)
            fred.angle(0.0)
            fred.left(wall["angle"])
            fred.goto(
                wall["trans"][0] * scale, 
                pos.y + wall["trans"][1] + height,
                wall["trans"][2] * scale
                )
            DrawKochFlake(fred, wall["length"] * scale, wall["depth"], wall["koch_flake"])

    # must do the flood fill after the boundaries are drawn
    for fill in castle["fill"]:
        fill_pos = (fill["pos"][0] * scale, pos.y+fill["pos"][1], fill["pos"][2] * scale)
        Fill(mc, fill_pos, fill["material"])

    fred.goto(0.99, 0.99, 0.99)

def DrawKochFlake(fred, length, depth, koch_flake):
    fred.pendown()
    for move in koch_flake:
        if move == "F":
            fred.go(length / (3 ** (depth - 1)))
        elif move == "L":
            fred.left(60)
        elif move == "R":
            fred.right(120)
    fred.penup()

def _get_nextPos(pos):
    return [
          (pos[0]-1, pos[1], pos[2])
        , (pos[0]+1, pos[1], pos[2])
        , (pos[0], pos[1], pos[2]-1)
        , (pos[0], pos[1], pos[2]+1)
    ]
def _int_pos(pos):
    return (int(pos[0]), int(pos[1]), int(pos[2]))

def Fill(mc, pos, matrial, overflow_protection = 10000):
    pos = _int_pos(pos)
    initial_material = mc.getBlock(pos)
    visited = []
    stack = [pos]

    while len(stack) > 0:
        this_pos = stack.pop()
        mc.setBlock(this_pos, matrial)
        visited.append(pos)
        next_pos_ar = _get_nextPos(this_pos)
        for next_pos in next_pos_ar:
            if next_pos in visited:
                continue
            next_pos_material = mc.getBlock(next_pos)
            if mc.getBlock(next_pos) == initial_material:
                stack.append(next_pos)
        overflow_protection += -1
        if overflow_protection <= 0:
            break

t = Turtle()
t.pendelay(0)
mc = Minecraft()

DrawCastle(mc, t, castle_2, 0.15)

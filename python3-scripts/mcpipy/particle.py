from .mc import *
mc = Minecraft()
mc.conn.send("world.spawnParticle", "mobappearance", 0.5,0.5,0.5, 0.2,0.2,0.2, 0, 10)

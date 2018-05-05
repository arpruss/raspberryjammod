from mine import *
mc = Minecraft()
mc.conn.send("world.setBlocks",0,0,0,5,5,5,Block(63, 15, '{Text4:"{\\"text\\":\\"\\"}",Text3:"{\\"text\\":\\"\\"}",Text2:"{\\"text\\":\\"\\"}",id:"minecraft:sign",Text1:"{\\"text\\":\\"hello\\"}"}'))

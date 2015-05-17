import mcpi.minecraft as minecraft
import server
mc = minecraft.Minecraft.create(server.address)
print(mc.events.pollBlockHits())
print(mc.events.pollChatPosts())


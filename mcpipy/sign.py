from mine import *
mc = Minecraft()
mc.setBlockWithNBT(mc.player.getTilePos(),block.SIGN("Hello,","World",headingAngle=180))

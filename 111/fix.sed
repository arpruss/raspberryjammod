s/Blocks\.air/Blocks.AIR/g
s/MobEffects\.levitation/MobEffects.LEVITATION/g
s/MobEffects\.nightVision/MobEffects.NIGHT_VISION/g
s/\.thePlayer/\.player/g
s/\.theWorld/\.world/g
s/\[1\.9,1\.9\.4)/[1.11,1.12)/
s/NOMINAL_VERSION\s*=\s*1009000/NOMINAL_VERSION = 1011000/
s/getTabCompletionOptions/getTabCompletions/g
s/getCommandName/getName/g
s/getCommandAliases/getAliases/g
s/addChatComponentMessage/sendMessage/g
s/addChatMessage/sendMessage/g
s/getCommandUsage/getUsage/g 
s/spawnEntityInWorld/spawnEntity/g
s/createEntityByName/createEntityByIDFromName/g
s/worldServers/worlds/g
s/getUnformattedTextForChat/getUnformattedComponentText/g
s/getPlayerList()\.getPlayerList()/getPlayerList().getPlayers()/g
s/getEntityID(e/getID(e.getClass()/g
s/for (String entityTypeName : EntityList.getEntityNameList()) { if (EntityList.getIDFromString(entityTypeName) >= 0) { bdr.append(EntityList.getIDFromString(entityTypeName)); bdr.append(","); bdr.append(entityTypeName); bdr.append("|"); }/for (ResourceLocation rl: EntityList.getEntityNameList()) { if (EntityList.getClass(rl) != null) { bdr.append(EntityList.getID(EntityList.getClass(rl))); bdr.append(","); bdr.append(rl.getResourcePath()); bdr.append("|"); }/g

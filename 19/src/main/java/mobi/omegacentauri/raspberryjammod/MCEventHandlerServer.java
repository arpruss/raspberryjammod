package mobi.omegacentauri.raspberryjammod;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.DamageSource;
import net.minecraft.world.World;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.entity.living.LivingHurtEvent;
import net.minecraftforge.event.entity.living.LivingDeathEvent;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;

public class MCEventHandlerServer extends MCEventHandler {
	public MCEventHandlerServer() {
		super();
		doRemote = false;
	}
	
	@SubscribeEvent
	public void onChatEvent(ServerChatEvent event) {
		System.out.println("onChatEvent "+event.getMessage());
		APIHandler.ChatDescription cd = new APIHandler.ChatDescription(event.getPlayer().getEntityId(), event.getMessage());
		for (APIHandler apiHandler : apiHandlers)
			apiHandler.addChatDescription(cd);		
	}
	
	@SubscribeEvent
	public void onServerTick(TickEvent.ServerTickEvent event) {
		runQueue();
	}
	
	@Override
	protected World[] getWorlds() {
		return RaspberryJamMod.minecraftServer.worldServers;
	}
	
	@SubscribeEvent
	public void onLivingHurtEvent(LivingHurtEvent event) {
		if (event.getEntity() instanceof EntityPlayer &&
				((RaspberryJamMod.noFallDamage && 
				event.getSource().damageType == "fall") ||
				(RaspberryJamMod.noInWallDamage && 
				event.getSource().damageType == "inWall"))) {
				event.setCanceled(true);
		}
	}

	@SubscribeEvent
	public void onLivingDeathEvent(LivingDeathEvent event) {
		if (event.getEntity() instanceof EntityPlayer) 
            for (APIHandler apiHandler : apiHandlers)
                apiHandler.died(event.getEntity().getEntityId());		
	}

	@SubscribeEvent
	public void onEntityJoinWorldEvent(EntityJoinWorldEvent event) {
		if (event.getEntity() instanceof EntityPlayer) 
            for (APIHandler apiHandler : apiHandlers)
                apiHandler.joined(event.getEntity().getEntityId());		
	}
}

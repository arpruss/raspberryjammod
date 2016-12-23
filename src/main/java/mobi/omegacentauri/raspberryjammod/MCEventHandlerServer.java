package mobi.omegacentauri.raspberryjammod;

import net.minecraft.server.MinecraftServer;
import net.minecraft.world.World;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.event.entity.living.LivingDeathEvent;

public class MCEventHandlerServer extends MCEventHandler {
	public MCEventHandlerServer() {
		super();
		doRemote = false;
	}
	
	@SubscribeEvent
	public void onChatEvent(ServerChatEvent event) {
		APIHandler.ChatDescription cd = new APIHandler.ChatDescription(event.player.getEntityId(), event.message);

		for (APIHandler apiHandler : apiHandlers)
			apiHandler.addChatDescription(cd);
	}
	
	@SubscribeEvent
	public void onServerTick(TickEvent.ServerTickEvent event) {
		runQueue();
	}
	
	@Override
	protected World[] getWorlds() {
		return MinecraftServer.getServer().worldServers;
	}

	@SubscribeEvent
	public void onLivingDeathEvent(LivingDeathEvent event) {
		if (event.getEntity() instanceof EntityPlayer) 
            for (APIHandler apiHandler : apiHandlers)
                apiHandler.died(event.getEntity().getEntityId());		
	}
}

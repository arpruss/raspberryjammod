package mobi.omegacentauri.raspberryjammod;

import net.minecraft.server.MinecraftServer;
import net.minecraft.world.World;
import net.minecraftforge.event.ServerChatEvent;
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
}

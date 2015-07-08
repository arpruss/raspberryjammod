package mobi.omegacentauri.raspberryjammod;

import mobi.omegacentauri.raspberryjammod.MCEventHandler.ChatDescription;
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
		ChatDescription cd = new ChatDescription(event.player.getEntityId(), event.message);
		synchronized(chats) {
			if (chats.size() >= MAX_CHATS)
				chats.remove(0);
			chats.add(cd);
		}
	}

	@SubscribeEvent
	public void onServerTick(TickEvent.ServerTickEvent event) {
		if (!pause) {
			synchronized(serverActionQueue) {
				for (ServerAction entry: serverActionQueue) {
					if (! RaspberryJamMod.serverActive)
						break;
					entry.execute();
				}
				serverActionQueue.clear();
			}
		}
		else if (! RaspberryJamMod.serverActive) {
			synchronized(serverActionQueue) {
				serverActionQueue.clear();
			}
		}
	}
}

package mobi.omegacentauri.raspberryjammod;

import java.io.IOException;

import mobi.omegacentauri.raspberryjammod.MCEventHandler.ChatDescription;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.World;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.world.WorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class MCEventHandlerClientOnly extends MCEventHandler {
	private APIServer apiServer;
	private boolean active;

	public MCEventHandlerClientOnly() {
		super();
		doRemote = true;
	}

	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onWorldLoadEvent(WorldEvent.Load event) {
		try{
			// the eventhandler is unregistered, so it doesn't do much
			System.out.println("RaspberryJamMod client only API");
			active = true;
			apiServer = new APIServer(this, RaspberryJamMod.clientOnlyPortNumber, false);
	
			new Thread(new Runnable() {
				@Override
				public void run() {
					try {
						apiServer.communicate();
					} catch(IOException e) {
						System.out.println("RaspberryJamMod error "+e);
					}
					finally {
						System.out.println("Closing RaspberryJamMod client-only API");
						if (apiServer != null) {
							apiServer.close();
							apiServer = null;
						}
					}
				}
	
			}).start();
		}
		catch (Exception e) {}
	}
	
	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onWorldUnloadEvent(WorldEvent.Unload event) {
		active = false;
		
		if (apiServer != null) {
			apiServer.close();
			apiServer = null;
		}
	}
	
	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onChatEvent(ServerChatEvent event) {
		ChatDescription cd = new ChatDescription(event.player.getEntityId(), event.message);
		synchronized(chats) {
			if (chats.size() >= MAX_CHATS)
				chats.remove(0);
			chats.add(cd);
		}
	}

	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onClientTick(TickEvent.ClientTickEvent event) {
		if (!pause) {
			synchronized(serverActionQueue) {
				for (ServerAction entry: serverActionQueue) {
					if (! active)
						break;
					entry.execute();
				}
				serverActionQueue.clear();
			}
		}
		else if (! active) {
			synchronized(serverActionQueue) {
				serverActionQueue.clear();
			}
		}
	}
}

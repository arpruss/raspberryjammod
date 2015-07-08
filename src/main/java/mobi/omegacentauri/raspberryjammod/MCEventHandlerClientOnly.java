package mobi.omegacentauri.raspberryjammod;

import java.io.IOException;

import mobi.omegacentauri.raspberryjammod.MCEventHandler.ChatDescription;
import net.minecraft.client.Minecraft;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.World;
import net.minecraftforge.client.event.ClientChatReceivedEvent;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.world.WorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class MCEventHandlerClientOnly extends MCEventHandler {
	private APIServer apiServer;

	public MCEventHandlerClientOnly() {
		super();
		doRemote = true;
	}

	@SubscribeEvent
	public void onChatEvent(ClientChatReceivedEvent event) {
		System.out.println("ClientChatEvent on client side: "+event.message.toString());
		ChatDescription cd = new ChatDescription(Minecraft.getMinecraft().thePlayer.getEntityId(), 
				event.message.toString());
		synchronized(chats) {
			if (chats.size() >= MAX_CHATS)
				chats.remove(0);
			chats.add(cd);
		}
	}
	
	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onChatEvent(ServerChatEvent event) {
		System.out.println("ServerChatEvent on client side: "+event.message);
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
		runQueue();
	}
}

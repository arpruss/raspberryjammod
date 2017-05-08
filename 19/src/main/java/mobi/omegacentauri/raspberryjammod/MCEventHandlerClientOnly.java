package mobi.omegacentauri.raspberryjammod;

import java.io.IOException;

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
	protected World[] worlds = { null };

	public MCEventHandlerClientOnly() {
		super();
		doRemote = true;
	}
    
    private static String fixMessage(String s) {
        if (s.startsWith("<> ")) return s.substring(3); else return s;
    }

	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onChatEvent(ClientChatReceivedEvent event) {
		APIHandler.ChatDescription cd = new APIHandler.ChatDescription(Minecraft.getMinecraft().thePlayer.getEntityId(), 
				fixMessage(event.getMessage().getUnformattedTextForChat()));
		for (APIHandler apiHandler: apiHandlers)
			apiHandler.addChatDescription(cd);
	}
	
	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onClientTick(TickEvent.ClientTickEvent event) {
		runQueue();
	}

	@Override
	protected World[] getWorlds() {
		worlds[0] = Minecraft.getMinecraft().theWorld;
		return worlds;
	}
}

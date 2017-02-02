package mobi.omegacentauri.raspberryjammod;

import java.io.IOException;
import java.net.InetSocketAddress;

import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.init.MobEffects;
import net.minecraft.potion.PotionEffect;
import net.minecraftforge.client.event.RenderLivingEvent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.world.WorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.common.network.FMLNetworkEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class ClientEventHandler {
	private volatile boolean nightVision = false;
	private int clientTickCount = 0;
	private MCEventHandlerClientOnly apiEventHandler = null;
	private APIServer apiServer = null;
//	private boolean registeredCommands = false;

	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onClientTick(TickEvent.ClientTickEvent event) {
		if (nightVision && clientTickCount % 1024 == 0) {
			Minecraft mc = Minecraft.getMinecraft();
			if (mc != null) {
				EntityPlayerSP player = Minecraft.getMinecraft().thePlayer;
				
				if (player != null) {
					player.addPotionEffect(new PotionEffect(MobEffects.nightVision, 4096));
				}
			}
		}
		clientTickCount++;
	} 

	public void setNightVision(boolean b) {
		nightVision = b;
	}

	public boolean getNightVision() {
		return nightVision;
	}

	@SideOnly(Side.CLIENT)
	@SubscribeEvent
	public void onClientConnectedToServer(FMLNetworkEvent.ClientConnectedToServerEvent event) {
		try {
			Object address = event.getManager().getRemoteAddress();
			if (address instanceof InetSocketAddress) {
				RaspberryJamMod.serverAddress = ((InetSocketAddress) address).getAddress().getHostAddress();
				System.out.println("Server address "+RaspberryJamMod.serverAddress);
			}
			else {
				System.out.println("No IP address");
			}
		} catch(Exception e) {
			RaspberryJamMod.serverAddress = null;
		}
	}


	@SideOnly(Side.CLIENT)
	@SubscribeEvent
	public void onWorldUnloaded(WorldEvent.Unload event) {
		if (! RaspberryJamMod.clientOnlyAPI)
			return;

		System.out.println("Closing world: "+event.getWorld());
		
		closeAPI();
	}	
	
	@SideOnly(Side.CLIENT)
	@SubscribeEvent
	public void onSpecialsPre(RenderLivingEvent.Specials.Pre<?> event) {
		if (RaspberryJamMod.noNameTags)
			event.setCanceled(true);
	}
	
	@SideOnly(Side.CLIENT)
	public void registerCommand(ScriptExternalCommand c) {
		net.minecraftforge.client.ClientCommandHandler.instance.registerCommand(c);
		RaspberryJamMod.scriptExternalCommands.add(c);
	}
	
	@SideOnly(Side.CLIENT)
	@SubscribeEvent
	public void onWorldLoaded(WorldEvent.Load event) {
		RaspberryJamMod.synchronizeConfig();
		System.out.println("Loading world: "+event.getWorld());

		if (RaspberryJamMod.clientOnlyAPI) {
			registerCommand(new PythonExternalCommand(true));
			registerCommand(new AddPythonExternalCommand(true));
		}
//		else 
//       {
			registerCommand(new LocalPythonExternalCommand(true));
			registerCommand(new AddLocalPythonExternalCommand(true));
//		}
		
		if (!RaspberryJamMod.clientOnlyAPI)
			return;
		
		if (apiEventHandler == null) {
            apiEventHandler = new MCEventHandlerClientOnly();
			MinecraftForge.EVENT_BUS.register(apiEventHandler);
		}

        if (apiServer == null)
			try {
				System.out.println("RaspberryJamMod client only API");
				RaspberryJamMod.apiActive = true;
				if (apiServer == null) {
					RaspberryJamMod.currentPortNumber = -1;
					apiServer = new APIServer(apiEventHandler, RaspberryJamMod.portNumber, RaspberryJamMod.searchForPort ? 65535 : RaspberryJamMod.portNumber, 
							RaspberryJamMod.wsPort,
							true);
					RaspberryJamMod.currentPortNumber = apiServer.getPortNumber();
	
					new Thread(new Runnable() {
						@Override
						public void run() {
							try {
								apiServer.communicate();
							} catch(IOException e) {
								System.out.println("RaspberryJamMod error "+e);
							}
							finally {
								closeAPI();
							}
						}
					}).start();
				}
			}
			catch (Exception e) {}
	}

	public void closeAPI() {
		RaspberryJamMod.closeAllScripts();
		for (int i = RaspberryJamMod.scriptExternalCommands.size()-1; i>=0; i--) {
			ScriptExternalCommand c = RaspberryJamMod.scriptExternalCommands.get(i);
			if (c.clientSide) {
				System.out.println("Unregistering "+c.getClass());
				RaspberryJamMod.unregisterCommand(net.minecraftforge.client.ClientCommandHandler.instance,c);
				RaspberryJamMod.scriptExternalCommands.remove(i);
			}		
		}
		RaspberryJamMod.apiActive = false;
		if (apiEventHandler != null) {
            MinecraftForge.EVENT_BUS.unregister(apiEventHandler);
            apiEventHandler = null;
		}
		if (apiServer != null) {
			apiServer.close();
			apiServer = null;
		}
	}
}

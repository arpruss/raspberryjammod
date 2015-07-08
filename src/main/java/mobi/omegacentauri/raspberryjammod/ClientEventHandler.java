package mobi.omegacentauri.raspberryjammod;

import java.beans.EventSetDescriptor;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.gui.GuiChat;
import net.minecraft.client.gui.GuiScreen;
import net.minecraft.event.ClickEvent;
import net.minecraft.item.ItemStack;
import net.minecraft.item.ItemSword;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.potion.Potion;
import net.minecraft.potion.PotionEffect;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.BlockPos;
import net.minecraft.util.EnumFacing;
import net.minecraft.util.IChatComponent;
import net.minecraft.world.EnumDifficulty;
import net.minecraft.world.World;
import net.minecraftforge.client.event.MouseEvent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.CommandEvent;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.event.terraingen.InitMapGenEvent;
import net.minecraftforge.event.world.WorldEvent;
import net.minecraftforge.fml.common.FMLCommonHandler;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class ClientEventHandler {
	private volatile boolean nightVision = false;
	private int clientTickCount = 0;
	private MCEventHandlerClientOnly eventHandler = null;
	private APIServer apiServer;

	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onClientTick(TickEvent.ClientTickEvent event) {
		if (nightVision && clientTickCount % 1024 == 0) {
			EntityPlayerSP player = Minecraft.getMinecraft().thePlayer;
			
			if (player != null) {
				player.addPotionEffect(new PotionEffect(Potion.nightVision.id, 4096));
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

	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onWorldLoadEvent(WorldEvent.Load event) {
		if (! RaspberryJamMod.clientOnlyAPI)
			return;

		if (eventHandler != null) {
			FMLCommonHandler.instance().bus().unregister(eventHandler);
		}
		eventHandler = new MCEventHandlerClientOnly();
		FMLCommonHandler.instance().bus().register(eventHandler);
		MinecraftForge.EVENT_BUS.register(eventHandler);

		try {
			// the eventhandler is unregistered, so it doesn't do much
			System.out.println("RaspberryJamMod client only API");
			RaspberryJamMod.serverActive = true;
			if (apiServer == null) {
				apiServer = new APIServer(eventHandler, RaspberryJamMod.portNumber, true);
		
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
		}
		catch (Exception e) {}
	}
	
	@SubscribeEvent
	@SideOnly(Side.CLIENT)
	public void onWorldUnloadEvent(WorldEvent.Unload event) {
		if (eventHandler != null) {
			RaspberryJamMod.serverActive = false;
			FMLCommonHandler.instance().bus().unregister(eventHandler);
			eventHandler = null;
		}
		if (! RaspberryJamMod.clientOnlyAPI && apiServer != null) {
			apiServer.close();
			apiServer = null;
		}
	}	

}

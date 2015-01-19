package mobi.omegacentauri.raspberryjammod;

import ibxm.Player;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.InputMismatchException;
import java.util.Scanner;

import net.minecraft.block.state.BlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.multiplayer.WorldClient;
import net.minecraft.init.Blocks;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.FMLCommonHandler;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;

@Mod(modid = RaspberryJamMod.MODID, version = RaspberryJamMod.VERSION, name = RaspberryJamMod.NAME)
public class RaspberryJamMod
{
	public static final String MODID = "raspberryjammod";
	public static final String VERSION = "0.0";
	public static final String NAME = "Raspberry Jam Mod";

	@EventHandler
	public void init(FMLInitializationEvent event)
	{
		// some example code
		System.out.println("Raspberry Jam Mod started");
		
		final OnServerTick onServerTick = new OnServerTick();
		FMLCommonHandler.instance().bus().register(onServerTick);

		new Thread(new Runnable() {

			@Override
			public void run() {
				MinecraftCommunicator mcc = null;
				try {
					mcc = new MinecraftCommunicator(onServerTick);
					mcc.communicate();
				} catch(IOException e) {
					System.out.println("RaspberryJamMod error "+e);
				}
				finally {
					if (mcc != null)
						mcc.close();
				}
			}

		}).start();
	}

}

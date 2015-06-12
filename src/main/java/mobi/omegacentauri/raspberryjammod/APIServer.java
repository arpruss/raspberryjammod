package mobi.omegacentauri.raspberryjammod;

// TODO: getHeight() should check block queue

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Method;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.InputMismatchException;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Scanner;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityList;
import net.minecraft.entity.EntityLiving;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.init.Blocks;
import net.minecraft.nbt.JsonToNBT;
import net.minecraft.nbt.NBTException;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.network.play.server.S43PacketCamera;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.BlockPos;
import net.minecraft.util.ChatComponentText;
import net.minecraft.util.IChatComponent;
import net.minecraft.util.Vec3;
import net.minecraft.util.Vec3i;
import net.minecraft.world.World;
import net.minecraft.world.WorldSettings;
import net.minecraft.world.chunk.Chunk;

public class APIServer {
	private static final int MAX_CONNECTIONS = 64;
	final private ServerSocket serverSocket;
	private MCEventHandler eventHandler;
	private boolean listening = true;
	private int connectionsActive = 0;

	public APIServer(MCEventHandler eventHandler) throws IOException {
		this.eventHandler = eventHandler;
		if (RaspberryJamMod.allowRemote) {
		    serverSocket = new ServerSocket(RaspberryJamMod.portNumber);
		}
        else {
            serverSocket = new ServerSocket(RaspberryJamMod.portNumber, 50, InetAddress.getByName("127.0.0.1"));
        }
	}

	void communicate() throws IOException {
		while(listening) {
			Socket connectionSocket = null;
			if (! RaspberryJamMod.concurrent) {
				try {
					socketCommunicate(serverSocket.accept());
				} catch(Exception e) {}
			}
			else {
				try {
					if (connectionsActive < MAX_CONNECTIONS) {
						final Socket socket = serverSocket.accept();
						connectionsActive++;
						new Thread(new Runnable(){
							@Override
							public void run() {
								socketCommunicate(socket);
								connectionsActive--;
							}}).start();
					}
					else {
						// Too many connections: sleep hoping one or more go away
						try {
							Thread.sleep(1000);
						}
						catch (Exception e) {}
					}
				} catch(Exception e) {}
			}
		}
	}

	private void socketCommunicate(Socket connectionSocket) {
		DataOutputStream writer = null;
		BufferedReader reader = null;

		try {
			String clientSentence;

			reader = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
			writer = new DataOutputStream(connectionSocket.getOutputStream());

			APIHandler api = new APIHandler(eventHandler, writer);

			while(null != (clientSentence = reader.readLine())) {
				api.process(clientSentence);
			}
		} catch (Exception e) {
			System.out.println(""+e);
		}
		finally {
			if (connectionSocket != null) 
				try {
					connectionSocket.close();
				} catch (IOException e) {
				}
			if (reader != null) 
				try {
					reader.close();
				} catch (IOException e) {
				}
			if (writer != null) 
				try {
					writer.close();
				} catch (IOException e) {
				}
		}
	}

	public void close() {
		listening = false;
		try {
			if (serverSocket != null)
				serverSocket.close();
		} catch (IOException e) {
		}
	}
}

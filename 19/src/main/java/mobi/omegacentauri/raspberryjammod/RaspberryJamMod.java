
package mobi.omegacentauri.raspberryjammod;

import ibxm.Player;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

import scala.collection.script.Script;

import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.multiplayer.WorldClient;
import net.minecraft.command.CommandHandler;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.init.Blocks;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.World;
import net.minecraftforge.client.ClientCommandHandler;
import net.minecraftforge.common.ForgeHooks;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.common.config.Configuration;
import net.minecraftforge.common.config.Property;
import net.minecraftforge.event.ForgeEventFactory;
import net.minecraftforge.fml.common.FMLCommonHandler;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartedEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;
import net.minecraftforge.fml.common.event.FMLServerStoppedEvent;
import net.minecraftforge.fml.common.event.FMLServerStoppingEvent;
import net.minecraftforge.fml.common.event.FMLStateEvent;
import net.minecraftforge.fml.common.network.FMLNetworkEvent;
import net.minecraftforge.fml.common.registry.EntityRegistry;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

@Mod(modid = RaspberryJamMod.MODID, version = RaspberryJamMod.VERSION, name = RaspberryJamMod.NAME,
guiFactory = "mobi.omegacentauri.raspberryjammod.GuiFactory", acceptableRemoteVersions="*", 
acceptedMinecraftVersions="[1.9,1.9.4)")
public class RaspberryJamMod
{
	public static final String MODID = "raspberryjammod";
	public static final String VERSION = "0.94";
	public static final String NAME = "Raspberry Jam Mod";
	private APIServer fullAPIServer = null;
	private PythonExternalCommand pythonExternalCommand = null;
	private NightVisionExternalCommand nightVisionExternalCommand = null;
	private CameraCommand cameraCommand = null;
	public static List<ScriptExternalCommand> scriptExternalCommands = new ArrayList<ScriptExternalCommand>();
	public static Configuration configFile;
	static int portNumber = 4711;
	static int wsPort = 14711;
	public static boolean concurrent = true;
	public static boolean leftClickToo = true;
	public static boolean allowRemote = true;
	public static boolean globalChatMessages = true;
	public static String pythonInterpreter = "python";
	public static boolean integrated = true;
	public static volatile boolean apiActive = false;
	public static String serverAddress = null;
	private ClientEventHandler clientEventHandler = null;
	static boolean clientOnlyAPI = false;
	static boolean searchForPort = false;
	private MCEventHandler serverEventHandler = null;
	//private MinecraftServer s;
	public static MinecraftServer minecraftServer;
	public static int currentPortNumber;
	public static boolean noFallDamage = false;
	public static boolean noInWallDamage = false;
	public static boolean globalImmutable = false;
	public static boolean absoluteCoordinates = false;
	public static volatile boolean noNameTags = false;
    public static final int NOMINAL_VERSION = 1009000;

	@Mod.EventHandler
	public void preInit(FMLPreInitializationEvent event) {
		integrated = true;
		try {
			Class.forName("net.minecraft.client.Minecraft");
		}
		catch (ClassNotFoundException e) {
			integrated = false;
		}

		configFile = new Configuration(event.getSuggestedConfigurationFile());
		configFile.load();
		System.out.println("configFile = "+configFile.getConfigFile().getPath());
		//		KeyBindings.init();

		synchronizeConfig();
	}

//	@Mod.EventHandler // doesn't work in 1.9 for some reason, but we don't need it anyway yet
//	@SideOnly(Side.CLIENT)
//	public void onConfigChanged(net.minecraftforge.fml.client.event.ConfigChangedEvent.OnConfigChangedEvent event) {
//		System.out.println("config changed");
//	}

	@Mod.EventHandler
	@SideOnly(Side.CLIENT)
	public void Init(FMLInitializationEvent event) {
		System.out.println("FMLInitializationEvent");
		clientEventHandler = new ClientEventHandler();
		MinecraftForge.EVENT_BUS.register(clientEventHandler);
		FMLCommonHandler.instance().bus().register(clientEventHandler);
		nightVisionExternalCommand = new NightVisionExternalCommand(clientEventHandler);
		net.minecraftforge.client.ClientCommandHandler.instance.registerCommand(nightVisionExternalCommand);
		cameraCommand = new CameraCommand();
		net.minecraftforge.client.ClientCommandHandler.instance.registerCommand(cameraCommand);
	}

	public static void synchronizeConfig() {
		portNumber = configFile.getInt("Port Number", Configuration.CATEGORY_GENERAL, 4711, 0, 65535, "Port number");
		wsPort = configFile.getInt("Websocket Port", Configuration.CATEGORY_GENERAL, 14711, 0, 65535, "Websocket port");
		searchForPort = configFile.getBoolean("Port Search if Needed", Configuration.CATEGORY_GENERAL, false, "Port search if needed");
		concurrent = configFile.getBoolean("Multiple Connections", Configuration.CATEGORY_GENERAL, true, "Multiple connections");
		allowRemote = configFile.getBoolean("Remote Connections", Configuration.CATEGORY_GENERAL, true, "Remote connections");
		leftClickToo = configFile.getBoolean("Detect Sword Left-Click", Configuration.CATEGORY_GENERAL, false, "Detect sword left-click");
		pythonInterpreter = configFile.getString("Python Interpreter", Configuration.CATEGORY_GENERAL, "python", "Python interpreter");
		globalChatMessages = configFile.getBoolean("Messages Go To All", Configuration.CATEGORY_GENERAL, true, "Messages go to all");
		clientOnlyAPI = configFile.getBoolean("Read-Only Client-Based API", Configuration.CATEGORY_GENERAL, false, "Read-only API");
		noFallDamage = configFile.getBoolean("Disable Fall Damage", Configuration.CATEGORY_GENERAL, false, "Disable fall damage");
		noInWallDamage = configFile.getBoolean("Disable Stuck-In-Wall Damage", Configuration.CATEGORY_GENERAL, false, "Disable stuck-in-wall damage");
		globalImmutable = configFile.getBoolean("Immutability Setting Is Global", Configuration.CATEGORY_GENERAL, false, "Immutability setting applies to all players");
		absoluteCoordinates = configFile.getBoolean("Absolute Coordinates", Configuration.CATEGORY_GENERAL, false, "Use absolute coordinates in scripts");
		//		clientOnlyPortNumber = configFile.getInt("Port Number for Client-Only API", Configuration.CATEGORY_GENERAL, 0, 0, 65535, "Client-only API port number (normally 0)");

		if (configFile.hasChanged())
			configFile.save();
	}

	public static int closeAllScripts() {
		int count = 0;
		for (ScriptExternalCommand c : scriptExternalCommands)
			count += c.close();
		return count;
	}
	
	@Mod.EventHandler
	public void onServerStopping(FMLServerStoppingEvent event) {
		if (clientOnlyAPI) {
			minecraftServer = null;
			return;
		}

		apiActive = false;

		if (serverEventHandler != null) {
			FMLCommonHandler.instance().bus().unregister(serverEventHandler);
			serverEventHandler = null;
		}

		if (fullAPIServer != null) {
			fullAPIServer.close();
		}
		closeAllScripts();
		for (int i = scriptExternalCommands.size() - 1; i >= 0 ; i--) {
			ScriptExternalCommand c = scriptExternalCommands.get(i);
			if (!c.clientSide) {
				unregisterCommand((CommandHandler)minecraftServer.getCommandManager(), c);
				scriptExternalCommands.remove(i);
			}
		}
		minecraftServer = null;
	}
	
	@Mod.EventHandler
	public void onServerStarting(FMLServerStartingEvent event) {
		synchronizeConfig();
		
		if (clientOnlyAPI)
			return;

		minecraftServer = event.getServer();

		if (clientEventHandler != null)
                    clientEventHandler.closeAPI();

		apiActive = true;

		serverEventHandler = new MCEventHandlerServer();
		FMLCommonHandler.instance().bus().register(serverEventHandler);
		MinecraftForge.EVENT_BUS.register(serverEventHandler);
		try {
			currentPortNumber = -1;
			fullAPIServer = new APIServer(serverEventHandler, portNumber, searchForPort ? 65535 : portNumber, wsPort, false);
			currentPortNumber = fullAPIServer.getPortNumber(); 
			System.out.println("Current port number "+currentPortNumber);

			new Thread(new Runnable() {
				@Override
				public void run() {
					try {
						fullAPIServer.communicate();
					} catch(IOException e) {
						System.out.println("RaspberryJamMod error "+e);
					}
					finally {
						System.out.println("Closing RaspberryJamMod");
						if (fullAPIServer != null)
							fullAPIServer.close();
					}
				}

			}).start();
		} catch (IOException e1) {
			System.out.println("Threw "+e1);
		}

		ScriptExternalCommand[] commands = new ScriptExternalCommand[] {
				new PythonExternalCommand(false),
				new AddPythonExternalCommand(false)
		};
		for (ScriptExternalCommand c : commands) {
			event.registerServerCommand(c);
			scriptExternalCommands.add(c);
		}
	}

	static public Field findField(Class c, String name) throws NoSuchFieldException {
		do {
			try {
//				for (Field f : c.getDeclaredFields()) {
//					System.out.println(f.getName()+" "+f.getType());
//				}
				return c.getDeclaredField(name);
			}
			catch (Exception e) {
//				System.out.println(""+e);
			}
		} while(null != (c = c.getSuperclass()));
		throw new NoSuchFieldException(name);
	}

	static public Field findFieldByType(Class c, String typeName) throws NoSuchFieldException {
		do {
			for (Field f : c.getDeclaredFields()) 
				if (f.getGenericType().toString().equals(typeName))
					return f;
		} while(null != (c = c.getSuperclass()));
		throw new NoSuchFieldException(typeName);
	}

	static public void unregisterCommand(CommandHandler ch, ICommand c) {
		try {
			Map commandMap = ch.getCommands();
			for (String alias: (List<String>)c.getCommandAliases()) {
				try {
					commandMap.remove(alias);
				} catch(Exception e) {}
			}

			try {
				commandMap.remove(c.getCommandName());
			} catch(Exception e) {}

			Field commandSetField = findFieldByType(ch.getClass(), "java.util.Set<net.minecraft.command.ICommand>");
			
			System.out.println("Found command set field "+commandSetField.getName());
			
//			try {
//				commandSetField = findField(ch.getClass(),"commandSet");
//			} catch (NoSuchFieldException e) {
//				commandSetField = findField(ch.getClass(), "field_71561_b");
//			}
			commandSetField.setAccessible(true);
			Set commandSet = (Set) commandSetField.get(ch);
			commandSet.remove(c);
		}
		catch (Exception e) {
			System.err.println("Oops "+e);
		}
	}
}

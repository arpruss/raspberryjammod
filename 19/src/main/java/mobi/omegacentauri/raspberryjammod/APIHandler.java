package mobi.omegacentauri.raspberryjammod;

// TODO: getHeight() should check block queue

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.InputMismatchException;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Scanner;
import java.util.Set;
import java.util.UUID;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.main.GameConfiguration;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityList;
import net.minecraft.entity.EntityLiving;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.init.Blocks;
import net.minecraft.init.MobEffects;
import net.minecraft.item.ItemStack;
import net.minecraft.item.ItemSword;
import net.minecraft.nbt.JsonToNBT;
import net.minecraft.nbt.NBTException;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.potion.PotionEffect;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.EnumFacing;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Vec3d;
import net.minecraft.util.math.Vec3i;
import net.minecraft.util.text.TextComponentString;
import net.minecraft.world.World;
import net.minecraft.world.WorldServer;
import net.minecraft.world.WorldSettings;
import net.minecraft.world.chunk.Chunk;
import net.minecraftforge.client.model.ModelLoader;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;

public class APIHandler {
	// world.checkpoint.save/restore, player.setting, world.setting(nametags_visible,*),
	// camera.setFixed() unsupported
	// camera.setNormal(id) and camera.setFollow(id) uses spectating, and so it moves the
	// player along with the entity that was set as camera
	protected static final String CHATGLOBAL = "chat.post";
	protected static final String APISUPPORTS = "api.supports";
	protected static final String APIVERSION = "api.version";
	protected static final String SETBLOCK = "world.setBlock";
	protected static final String SETBLOCKS = "world.setBlocks"; 
	protected static final String GETBLOCK = "world.getBlock";
	protected static final String GETBLOCKWITHDATA = "world.getBlockWithData";
	protected static final String GETBLOCKS = "world.getBlocks";
	protected static final String GETBLOCKSWITHDATA = "world.getBlocksWithData";
	protected static final String GETHEIGHT = "world.getHeight"; 
	protected static final String WORLDSPAWNENTITY = "world.spawnEntity";
	protected static final String WORLDSPAWNPARTICLE = "world.spawnParticle";
	protected static final String WORLDDELETEENTITY = "world.removeEntity";
	protected static final String WORLDGETPLAYERIDS = "world.getPlayerIds"; 	
	protected static final String WORLDGETPLAYERID = "world.getPlayerId"; 
	protected static final String WORLDSETTING = "world.setting";
	
	protected static final String WORLDSETTING_WORLD_IMMUTABLE = "world_immutable";
	protected static final String WORLDSETTING_INCLUDE_NBT = "include_nbt_with_data";
	protected static final String WORLDSETTING_NAMETAGS_VISIBLE = "nametags_visible";
//	protected static final String WORLDSETTING_PAUSE_DRAWING = "pause_drawing";
	
	protected static final String EVENTSSETTING_RESTRICT_TO_SWORD = "restrict_to_sword";
	protected static final String EVENTSSETTING_DETECT_LEFT_CLICK = "detect_left_click";

//	protected static final String GETLIGHTLEVEL = "block.getLightLevel"; // EXPERIMENTAL AND UNSUPPORTED
//	protected static final String SETLIGHTLEVEL = "block.setLightLevel"; // EXPERIMENTAL AND UNSUPPORTED


	protected static final String EVENTSBLOCKHITS = "events.block.hits";
	protected static final String EVENTSCHATPOSTS = "events.chat.posts";
	protected static final String EVENTSCLEAR = "events.clear";
	protected static final String EVENTSSETTING = "events.setting";

	// camera.*
	protected static final String SETFOLLOW = "setFollow";
	protected static final String SETNORMAL = "setNormal";
	protected static final String GETENTITYID = "getEntityId";
	protected static final String SETDEBUG = "setDebug"; // EXPERIMENTAL AND UNSUPPORTED
	protected static final String SETDISTANCE = "setDistance"; // EXPERIMENTAL AND UNSUPPORTED

	// player.* or entity.*
	// adding any commands here requires adjusting tooManyPlayerCommandArguments()
	// and entityOrPlayerCommands.
	protected static final String GETDIRECTION = "getDirection";
	protected static final String GETPITCH = "getPitch";
	protected static final String GETPOS = "getPos";
	protected static final String GETROTATION = "getRotation";
	protected static final String GETTILE = "getTile";
	protected static final String GETNAMEUUID = "getNameAndUUID";
	protected static final String GETNAME = "getName";
	protected static final String SETDIMENSION = "setDimension"; // EXPERIMENTAL AND UNSUPPORTED
	protected static final String SETDIRECTION = "setDirection";
	protected static final String SETPITCH = "setPitch";
	protected static final String SETPOS = "setPos";
	protected static final String SETROTATION = "setRotation";
	protected static final String SETTILE = "setTile";
	protected static final String CHAT = "chat.post";
	
	protected String[] fullCommands = {
			 CHATGLOBAL,
			 APIVERSION,
			 APISUPPORTS,
			 SETBLOCK, 
			 "+",
			 SETBLOCKS, 
			 GETBLOCK, 
			 GETBLOCKWITHDATA, 
			 GETBLOCKS,
			 GETBLOCKSWITHDATA,
			 GETHEIGHT, 
			 WORLDSPAWNENTITY,
			 WORLDSPAWNPARTICLE,
			 WORLDDELETEENTITY,
			 WORLDGETPLAYERIDS, 	
			 WORLDGETPLAYERID, 
			 WORLDSETTING,
//			 GETLIGHTLEVEL,
//			 SETLIGHTLEVEL,
			 EVENTSBLOCKHITS,
			 EVENTSCHATPOSTS,
			 EVENTSCLEAR,
			 EVENTSSETTING,
	};
	
	protected String[] worldSettings = {
			WORLDSETTING_WORLD_IMMUTABLE, 
			WORLDSETTING_INCLUDE_NBT,
			WORLDSETTING_NAMETAGS_VISIBLE
	};
	
	protected String[] eventsSettings = {
			EVENTSSETTING_RESTRICT_TO_SWORD,
			EVENTSSETTING_DETECT_LEFT_CLICK
	};
	
	protected String[] cameraCommands = {
			SETFOLLOW,
			SETNORMAL,
			GETENTITYID,
			SETDEBUG,
			SETDISTANCE
	};
	
	protected String[] entityOrPlayerCommands = {
			 GETDIRECTION,
			 GETPITCH,
			 GETPOS,
			 GETROTATION,
			 GETTILE,
			 GETNAMEUUID,
             GETNAME,
			 SETDIRECTION,
			 SETTILE,
			 SETPOS,
			 SETDIMENSION,
			 SETPITCH,
			 SETROTATION,
			 CHAT
	};
    
    protected static final String[][] ENTITY_RENAME_111 = {
        {"areaeffectcloud", "area_effect_cloud"},
        {"armorstand", "armor_stand"},
        {"cauldron", "brewing_stand"},
        {"cavespider", "cave_spider"},
        {"minecartchest", "chest_minecart"},
        {"control", "command_block"},
        {"minecartcommandblock", "commandblock_minecart"},
        {"dldetector", "daylight_detector"},
        {"trap", "dispenser"},
        {"dragonfireball", "dragon_fireball"},
        {"thrownegg", "egg"},
        {"enchanttable", "enchanting_table"},
        {"endgateway", "end_gateway"},
        {"airportal", "end_portal"},
        {"enderchest", "ender_chest"},
        {"endercrystal", "ender_crystal"},
        {"enderdragon", "ender_dragon"},
        {"thrownenderpearl", "ender_pearl"},
        {"eyeofendersignal", "eye_of_ender_signal"},
        {"fallingsand", "falling_block"},
        {"fireworksrocketentity", "fireworks_rocket"},
        {"flowerpot", "flower_pot"},
        {"minecartfurnace", "furnace_minecart"},
        {"minecarthopper", "hopper_minecart"},
        {"entityhorse", "horse"},
        {"itemframe", "item_frame"},
        {"recordplayer", "jukebox"},
        {"leashknot", "leash_knot"},
        {"lightningbolt", "lightning_bolt"},
        {"lavaslime", "magma_cube"},
        {"minecartrideable", "minecart"},
        {"mobspawner", "mob_spawner"},
        {"mushroomcow", "mooshroom"},
        {"music", "noteblock"},
        {"ozelot", "ocelot"},
        {"polarbear", "polar_bear"},
        {"shulkerbullet", "shulker_bullet"},
        {"smallfireball", "small_fireball"},
        {"spectralarrow", "spectral_arrow"},
        {"thrownpotion", "potion"},
        {"minecartspawner", "spawner_minecart"},
        {"structure", "structure_block"},
        {"primedtnt", "tnt"},
        {"minecarttnt", "tnt_minecart"},
        {"villagergolem", "villager_golem"},
        {"witherboss", "wither"},
        {"witherskull", "wither_skull"},
        {"thrownexpbottle", "xp_bottle"},
        {"xporb", "xp_orb"},
        {"pigzombie", "zombie_pigman"},
    };
	
	protected static final float TOO_SMALL = (float) 1e-9;

	protected World[] serverWorlds;
	protected MCEventHandler eventHandler;
	protected boolean listening = true;
	protected Minecraft mc;
	protected PrintWriter writer = null;
	protected boolean includeNBTWithData = false;
	protected boolean havePlayer;
	protected int playerId = 0;
	protected UUID playerUniqueId;
	protected EntityPlayerMP playerMP;
	protected List<String> usernames = null;
	protected List<String> passwords = null;
	protected boolean authenticated;
	public static final String PASSWORD_DATA = "raspberryjammod_passwords.dat";
	public static final String PERMISSION_DATA = "raspberryjammod_permissions.dat";
	private String salt = null;
	private boolean authenticationSetup;
	private List<HitDescription> hits = new LinkedList<HitDescription>();
	protected List<ChatDescription> chats = new LinkedList<ChatDescription>();
	private boolean restrictToSword = true;
	private boolean detectLeftClick;
	private static final int MAX_CHATS = 512;
	private static final int MAX_HITS = 512;
	public Permission permission = null;
	protected boolean handledPermission = false;
	private String authenticatedUsername = null;
	private boolean stopChanges = false;
	private boolean verifiedUser = false;
	private Map<Integer,UUID> idToUUID = new HashMap<Integer,UUID>();

	public APIHandler(MCEventHandler eventHandler, PrintWriter writer) throws IOException {
		this(eventHandler, writer, true);
	}
	
	public void close() {
		eventHandler.unregisterAPIHandler(this);
	}
	
	public APIHandler(MCEventHandler eventHandler, PrintWriter writer, Boolean needAuthentication) throws IOException {
		this.eventHandler = eventHandler;
		this.writer = writer;
		this.havePlayer = false;
		this.playerMP = null;
		this.handledPermission = false;
        this.detectLeftClick = RaspberryJamMod.leftClickToo;

        eventHandler.registerAPIHandler(this);

		if (needAuthentication) {
			File pass = new File(PASSWORD_DATA); 
			if (pass.exists()) {
				passwords = new ArrayList<String>();
				usernames = new ArrayList<String>();
				BufferedReader r = new BufferedReader(new FileReader(pass));
				String l;
				while (null != (l=r.readLine())) {
					l = l.trim();
					String[] data = l.split("\\s+");
					if (data.length >= 2) {
						usernames.add(data[0]);
						passwords.add(data[1]);
					}
				}
				r.close();
                
                authenticated = false;
				salt = null;
				try {
					MessageDigest md = MessageDigest.getInstance("MD5");
					md.reset();
					
					byte[] b = ("RaspberryJamMod"+System.currentTimeMillis()).getBytes("UTF-8"); 
					
					md.update(b);
					
					salt = tohex(md.digest());
				} catch (Exception e) {
				}

			}
            else {
                this.authenticated = true;
            }
		}
		else {
			this.authenticated = true;
		}
	}
    
    synchronized public void died(int entityId) {
        if (entityId == playerId) {
            playerMP = null;
        }
    }
    
    synchronized public void joined(int entityId) {
        if (entityId == playerId) {
            playerMP = null;
        }
    }
    
    synchronized private void updatePlayerMP() {
        if (playerMP != null)
            return;

		playerMP = RaspberryJamMod.minecraftServer.getPlayerList().getPlayerByUUID(playerUniqueId);
    }
	
	public static String tohex(byte[] array) {
		StringBuilder s = new StringBuilder();
		for (byte b : array) {
			s.append(String.format("%02x", b));
		}
		return s.toString();
	}
	
	protected boolean setup() {
		serverWorlds = RaspberryJamMod.minecraftServer.worldServers;

		if (serverWorlds == null) {
			fail("Worlds not available");
			return false;
		}
		
		if (! havePlayer) {
			if (RaspberryJamMod.integrated) {
				mc = Minecraft.getMinecraft();
				
				if (mc == null) {
					fail("Minecraft client not yet available");
				}
				
				if (mc.thePlayer == null) {
					fail("Client player not available");
					return false;
				}
				playerUniqueId = mc.thePlayer.getUniqueID();
				playerMP = RaspberryJamMod.minecraftServer.getPlayerList().getPlayerByUUID(playerUniqueId);
				playerId = playerMP.getEntityId();
			}
			else {
				playerMP = null;
				
				if (authenticatedUsername != null) 
					playerMP = (EntityPlayerMP)getPlayerByNameOrUUID(authenticatedUsername);
				
				if (playerMP != null) {
					verifiedUser = true;
				}
				else {
					int firstId = 0;
					
					for (EntityPlayer p : RaspberryJamMod.minecraftServer.getPlayerList().getPlayerList()) {
						int id = p.getEntityId();
						if (playerMP == null || id < firstId) {
							firstId = id;
							playerMP = (EntityPlayerMP)p;
						}
					}
				}
				
				if (playerMP != null) {
					playerId = playerMP.getEntityId();
					playerUniqueId = playerMP.getUniqueID();
				}
			}
			
			if (playerMP == null) {
				// This check could be removed, but a connection to a server while there is no
				// player on the server is more likely to be a hacking attempt, and so we'll
				// wait for a player.
				fail("Player not found (in setup)");
				return false;
			}
			else {
				havePlayer = true;
			}
		}
		else {
			updatePlayerMP();
		}

		return true;
	}
	
	void handleAuthentication(String input) throws IOException {
		if (salt == null)
			throw new IOException("salt generation error");

		if (input.startsWith("security.authenticate(")) {
			input = input.substring(22).trim();
			if (input.length()<2) 
				throw new IOException("authentication error");
			input = input.substring(0,input.length()-1);
			int count = usernames.size();
			for (int i = 0 ; i < count ; i++) {
				String data = salt + ":" + usernames.get(i) + ":" + passwords.get(i);
				MessageDigest md;
				try {
					md = MessageDigest.getInstance("MD5");
				} catch (NoSuchAlgorithmException e) {
					throw new IOException("md5 error");
				}
				md.reset();
				
				byte[] b = data.getBytes("UTF-8"); 
				
				md.update(b);
				
				String dataDigest = tohex(md.digest());
				
				if (input.equals(dataDigest)) {
                    System.out.println("Authenticated "+usernames.get(i));
                    authenticatedUsername = usernames.get(i);
					authenticated = true;
					return;
				}
			}
			throw new IOException("authentication error");
		}
		sendLine("security.challenge "+salt);
	}

	void process(String clientSentence) throws IOException {
		if (!authenticated) {
			handleAuthentication(clientSentence);
			return;
		}
		
		if (!setup())
			return;
		
		if (!handledPermission) {
			handlePermission();
			handledPermission = true;            
		}
		
		Scanner scan = null;

		try {	
			int paren;
			String cmd;
			if (clientSentence.startsWith("+")) {
				paren = 0;
				cmd = "world.setBlock";
			}
			else {
				paren = clientSentence.indexOf('(');
				if (paren < 0) {
					if (! clientSentence.matches("^[\\s\r\n]*$")) {
						unknownCommand();
					}
					return;
				}
				cmd = clientSentence.substring(0, paren);
			}
			String args = clientSentence.substring(paren + 1).replaceAll("[\\s\r\n]+$", "").replaceAll("\\)$", "");

			scan = new Scanner(args);
			scan.useDelimiter(",");

			synchronized (eventHandler) {
				try {
					runCommand(cmd, args, scan);
				} 
				catch(NoSuchElementException e) {
					fail("Parsing error?");
				}
			}

			scan.close();
			scan = null;
		}
		catch(Exception e) {
			System.out.println(""+e);
			e.printStackTrace();
		}
		finally {
			if (scan != null)
				scan.close();
		}
	}


	private void handlePermission() {
		File perm = new File(PERMISSION_DATA); 
		if (perm.exists()) {
			String permissionString = "";
			
			try {
				permission = new Permission(serverWorlds);
				BufferedReader r = new BufferedReader(new FileReader(perm));
				String l;
				String toMatch;
				if (authenticatedUsername != null) {
					toMatch = authenticatedUsername + " ";
				}
				else {
					toMatch = null;
				}
				while (null != (l=r.readLine())) {
					l = l.trim();
					if (l.startsWith("*")) {
						permission.add(l.substring(1));
					}
					else if (toMatch != null && l.startsWith(toMatch)) {
						permission.add(l.substring(toMatch.length()));
					}
				}
				r.close();
				if (permission.permitsEverything())
					permission = null;
			}
			catch (Exception e) {
				System.err.println("Error in reading permissions file");
				permission = new Permission(serverWorlds);
				permission.add(null, Permission.ALL, Permission.ALL, Permission.ALL, Permission.ALL, false);
			}
		}
	}

	protected void runCommand(String cmd, String args, Scanner scan) 
			throws InputMismatchException, NoSuchElementException, IndexOutOfBoundsException {

		if (cmd.equals(SETBLOCK)) {
			Location pos = getBlockLocation(scan);
			
			if (permission != null && permission.isPermitted(pos.world, pos.getX(), pos.getZ()))
				return;
			
			short id = scan.nextShort();
			short meta = scan.hasNextShort() ? scan.nextShort() : 0;
			String tagString = getRest(scan);

			SetBlockState setState;

			if (tagString.contains("{")) {
				try {
					setState = new SetBlockNBT(pos, id, meta, 
							JsonToNBT.getTagFromJson(tagString));
				} catch (NBTException e) {
					System.err.println("Cannot parse NBT");
					setState = new SetBlockState(pos, id, meta);
				}
			}
			else {
				setState = new SetBlockState(pos, id, meta);
			}

			eventHandler.queueServerAction(setState);
		}
		else if (cmd.equals(GETBLOCK)) {
			Location pos = getBlockLocation(scan);
			int id = eventHandler.getBlockId(pos);

			sendLine(id);
		}
		else if (cmd.equals(GETBLOCKWITHDATA)) {
			if (includeNBTWithData) {
				sendLine(eventHandler.describeBlockState(getBlockLocation(scan)));
			}
			else {
				BlockState state = eventHandler.getBlockState(getBlockLocation(scan));
				sendLine(""+state.id+","+state.meta);
			}
		}
		else if (cmd.equals(GETBLOCKS)) {
			Location pos1 = getBlockLocation(scan);
			Location pos2 = getBlockLocation(scan);

			StringBuilder out = new StringBuilder();
			int x1 = Math.min(pos1.getX(), pos2.getX());
			int x2 = Math.max(pos1.getX(), pos2.getX());
			int y1 = Math.min(pos1.getY(), pos2.getY());
			int y2 = Math.max(pos1.getY(), pos2.getY());
			int z1 = Math.min(pos1.getZ(), pos2.getZ());
			int z2 = Math.max(pos1.getZ(), pos2.getZ());
			for (int y = y1 ; y <= y2 ; y++)
				for (int x = x1 ; x <= x2; x++)
					for (int z = z1 ; z <= z2; z++) {
						if (out.length() != 0)
							out.append(",");
						out.append(eventHandler.getBlockId(new Location(pos1.world, x, y, z)));
					}
			sendLine(out.toString());
		}
		else if (cmd.equals(GETBLOCKSWITHDATA)) {
			Location pos1 = getBlockLocation(scan);
			Location pos2 = getBlockLocation(scan);
			StringBuilder out = new StringBuilder();
			int x1 = Math.min(pos1.getX(), pos2.getX());
			int x2 = Math.max(pos1.getX(), pos2.getX());
			int y1 = Math.min(pos1.getY(), pos2.getY());
			int y2 = Math.max(pos1.getY(), pos2.getY());
			int z1 = Math.min(pos1.getZ(), pos2.getZ());
			int z2 = Math.max(pos1.getZ(), pos2.getZ());
			for (int y = y1 ; y <= y2 ; y++)
				for (int x = x1 ; x <= x2; x++)
					for (int z = z1 ; z <= z2; z++) {
						if (out.length() != 0)
							out.append("|");
						Location pos = new Location(pos1.world, x, y, z);
						if (includeNBTWithData) {
							out.append(eventHandler.describeBlockState(pos).replace("&","&amp;").replace("|","&#124;"));
						}
						else {
							BlockState state = eventHandler.getBlockState(pos);
							out.append(""+state.id+","+state.meta);
						}
					}
			sendLine(out.toString());
		}
		else if (cmd.equals(GETHEIGHT)) {
			int x0 = scan.nextInt();
			int z0 = scan.nextInt();
			Location pos = Location.decodeLocation(serverWorlds, x0, 0, z0);
			Chunk chunk = serverWorlds[0].getChunkFromBlockCoords(pos);
			int h = chunk.getHeight(pos);
			int x = pos.getX();
			int z = pos.getZ();
			for (int y = serverWorlds[0].getHeight() ; y >= h ; y--) {
				Block b = chunk.getBlockState(x,y,z).getBlock();
				if (b != Blocks.air) {
					h = y;
					break;
				}
			}

			h -= Location.getOrigin(serverWorlds[0]).getY();

			sendLine(h);
		}
// TODO: light level
//		else if (cmd.equals(GETLIGHTLEVEL)) {
//			sendLine(Block.getBlockById(scan.nextInt()).getLightValue()/15.);
//		}
//		else if (cmd.equals(SETLIGHTLEVEL)) {
//			int id = scan.nextInt();
//			float value = scan.nextFloat();
//			Block.getBlockById(id).setLightLevel(value);
//		}
		else if (cmd.equals(SETBLOCKS)) {
			Location pos1 = getBlockLocation(scan);
			Location pos2 = getBlockLocation(scan);

			/* TODO? do partial drawing in case of partial overlap with forbidden area.
			 */
			if (permission != null && permission.isPermitted(pos1.world, pos1.getX(), pos1.getZ(),
					pos2.getX(), pos2.getZ()))
				return;
			
			short id = scan.nextShort();
			short meta = scan.hasNextShort() ? scan.nextShort() : 0;

			String tagString = getRest(scan);

			SetBlocksState setState;

			if (tagString.contains("{")) {
				try {
					setState = new SetBlocksNBT(pos1, pos2, id, meta, JsonToNBT.getTagFromJson(tagString));
				} catch (NBTException e) {
					setState = new SetBlocksState(pos1, pos2, id, meta);
				}
			}
			else {
				setState = new SetBlocksState(pos1, pos2, id, meta);
			}

			eventHandler.queueServerAction(setState);
		}
		else if (cmd.startsWith("player.")) {
			String subcommand = cmd.substring(7);
			if (tooManyPlayerCommandArguments(subcommand, args)) {
				String name = scan.next();
				if (!name.equals("None") && name.length()>0) {
					EntityPlayer player = getPlayerByNameOrUUID(name);
					if (player != null) 
						entityCommand(player.getEntityId(), subcommand, scan);
					else
						fail("Player not found (in player.*)");
					return;
				}
			}
			
			if (havePlayer) {
				entityCommand(playerId, subcommand, scan);
			}
			else {
				fail("Do not seem to have a player");
			}
		}
		else if (cmd.startsWith("entity.")) {
			entityCommand(scan.nextInt(), cmd.substring(7), scan);
		}
		else if (cmd.equals(CHATGLOBAL)) {
			chat(args);
		}
		else if (cmd.equals(WORLDGETPLAYERIDS)) {
			List<Integer> players = new ArrayList<Integer>();
			for (World w : serverWorlds) {
				for (EntityPlayer p : (List<EntityPlayer>)w.playerEntities) {
					players.add(p.getEntityId());
				}
			}
			Collections.sort(players);
			
			String ids = "";
			for (Integer id : players) {
				if (ids.length() > 0)
					ids += "|";
				ids += id;
			}
			sendLine(ids);
		}
		else if (cmd.equals(WORLDGETPLAYERID)) {
			if (scan.hasNext()) {
				String name = scan.next();
				
				EntityPlayer player = getPlayerByNameOrUUID(name);
				
				if (player != null)
					sendLine(player.getEntityId());
				else
					fail("Unknown player");
			}
			else {
				// unofficial API to get current player ID
				if (havePlayer)
					sendLine(playerId);
				else
					fail("Have not yet found a player.");
			}
		}
		else if (cmd.equals(WORLDDELETEENTITY)) {
			removeEntity(scan.nextInt());
		}
		else if (cmd.equals(WORLDSPAWNENTITY)) {
			spawnEntity(scan);
		}
		else if (cmd.equals(WORLDSPAWNPARTICLE)) {
			spawnParticle(scan);
		}
		else if (cmd.equals(EVENTSCLEAR)) {
			clearAllEvents();
		}
		else if (cmd.equals(EVENTSBLOCKHITS)) {
			sendLine(getHitsAndClear());
		}
		else if (cmd.equals(EVENTSCHATPOSTS)) {
			sendLine(getChatsAndClear());
		}
		else if (cmd.equals(WORLDSETTING)) {
			String setting = scan.next();
			if (setting.equals(WORLDSETTING_WORLD_IMMUTABLE)) // across connections
				stopChanges = (scan.nextInt() != 0);
			else if (setting.equals(WORLDSETTING_INCLUDE_NBT)) // connection-specific
				includeNBTWithData = (scan.nextInt() != 0);
			else if (setting.equals(WORLDSETTING_NAMETAGS_VISIBLE)) // across connections, standalone only
				RaspberryJamMod.noNameTags = (scan.nextInt() == 0);
//			else if (setting.equals(WORLDSETTING_PAUSE_DRAWING)) // across connections
//				eventHandler.setPause(scan.nextInt() != 0);
			// name_tags not supported
		}
		else if (cmd.equals(EVENTSSETTING)) {
			String setting = scan.next();
			if (setting.equals(EVENTSSETTING_RESTRICT_TO_SWORD)) // connection-specific 
				restrictToSword = (scan.nextInt() != 0);
			else if (setting.equals(EVENTSSETTING_DETECT_LEFT_CLICK)) // connection-specific
				detectLeftClick =  (scan.nextInt() != 0);
		}
		else if (cmd.startsWith("camera.")) {
			cameraCommand(cmd.substring(7), scan);
		}
		else if(cmd.equals(APISUPPORTS)) {
			String arg = scan.next();
			if (arg == null) {
				fail("invalid argument");
				return;
			}
			apiSupports(arg);
		}
		else if (cmd.equals(APIVERSION)) {
			sendLine(RaspberryJamMod.MODID+","+RaspberryJamMod.VERSION+","+"java"+","+mcVersion());
		}
		else {
			unknownCommand();
		}
	}
	
	private boolean tooManyPlayerCommandArguments(String subcommand, String args) {
		// check if there are more arguments than are needed; this detects if the
		// script slipped in a username, for compatibility with RaspberryJuice
		int count = args.length() > 0 ? 1 : 0;
		for (int i = args.length()-1; i >= 0 ; i--)
			if (args.charAt(i) == ',')
				count++;
		if (subcommand.startsWith("get"))
			return count > 0;
		else if (subcommand.equals(SETDIRECTION) ||
				subcommand.equals(SETTILE) || 
				subcommand.equals(SETPOS))
			return count > 3;
		else if (subcommand.equals(CHAT)) {
			// the player.chat command ALWAYS takes a player name, but perhaps blank
			return true;
		}
		else
			return count > 1;
	}

	private void apiSupports(String arg) {
		String[] list = fullCommands;
		if (arg.startsWith("camera.")) {
			arg = arg.substring(7);
			list = cameraCommands;
		}
		else if (arg.startsWith("entity.") || arg.startsWith("player.")) {
			arg = arg.substring(7);
			list = entityOrPlayerCommands;
		}
		else if (arg.startsWith(WORLDSETTING+".")) {
			arg = arg.substring(WORLDSETTING.length()+1);
			list = worldSettings;
		}
		else if (arg.startsWith(EVENTSSETTING+".")) {
			arg = arg.substring(EVENTSSETTING.length()+1);
			list = eventsSettings;
		}
		for (String c : list) 
			if (c.equals(arg)) {
				sendLine(1);
				return;
			}
		sendLine(0);
	}

	protected EntityPlayer getPlayerByNameOrUUID(String name) {
		for (EntityPlayer p : RaspberryJamMod.minecraftServer.getPlayerList().getPlayerList()) {
			if (p.getName().equals(name)) {
				return p;
			}
		}
		for (EntityPlayer p : RaspberryJamMod.minecraftServer.getPlayerList().getPlayerList()) {
			if (p.getUniqueID().toString().equals(name)) {
				return p;
			}
		}		
		return null;
	}
	
	protected String mcVersion() {
		return RaspberryJamMod.minecraftServer.getMinecraftVersion();
	}
	
	protected void unknownCommand() {
		fail("unknown command");
	}
	
	protected void removeEntity(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null)
			e.getEntityWorld().removeEntity(e);
	}
    
    protected String rename111(String entityId) {
        if (entityId.startsWith("minecraft:"))
            return entityId;
        System.out.println("Searching for "+entityId);
        String e = entityId.toLowerCase();
        for (String[] data: ENTITY_RENAME_111) {
            if (data[0].equals(e)) {
                System.out.println("found minecraft:"+data[1]);
                return "minecraft:" + data[1];
            }
        }
        return "minecraft:" + entityId;
    }

	protected void spawnEntity(Scanner scan) {
		String entityId = scan.next();
        
        System.out.println("Helo");
        if (RaspberryJamMod.NOMINAL_VERSION >= 1011000) {
            System.out.println("ren");
            entityId = rename111(entityId);
        }
        
		double x0 = scan.nextDouble();
		double y0 = scan.nextDouble();
		double z0 = scan.nextDouble();
		Vec3w pos = Location.decodeVec3w(serverWorlds, x0, y0, z0);
		
		// TODO? Could do damage by spawning dragons close to a forbidden zone; perhaps forbid that?
		if (permission != null && ! permission.isPermitted(pos.world, 
				(int)Math.floor(pos.xCoord),(int)Math.floor(pos.zCoord)))
			return;
		
		String tagString = getRest(scan);
        if (tagString.length() == 0)
            tagString = "{}";
		Entity entity;
		boolean fixGravity = false;
		
		try {
            NBTTagCompound tags;
            try {
                tags = JsonToNBT.getTagFromJson(tagString);
                if (tags.hasKey("NoAI")) {
                    fixGravity = tags.getBoolean("NoAI");
                }
            } catch (NBTException e) {
                fail("Cannot parse tags");
                return;
            }
            tags.setString("id", entityId);
            entity = EntityList.createEntityFromNBT(tags, pos.world);
            if (fixGravity && entity instanceof EntityLiving) {
                System.out.println("fixGravity "+fixGravity);
                ((EntityLiving)entity).addPotionEffect(new PotionEffect(MobEffects.levitation, 
                        Integer.MAX_VALUE, -1));
            }
			
			if (entity == null) {
				throw new Exception();
			}
		} catch(Exception e) {
			fail("Cannot create entity");
			return;
		}

		entity.setPositionAndUpdate(pos.xCoord, pos.yCoord, pos.zCoord);
		pos.world.spawnEntityInWorld(entity);
		sendLine(entity.getEntityId());
		
		//TODO: antigravity for NoAI:1
	}

	protected void chat(int id, String msg) {
		Entity e = getServerEntityByID(id);
		if (e == null || ! (e instanceof EntityPlayer)) {
			fail("cannot find player");
			return;
		}
		
		e.addChatMessage(new TextComponentString(msg));
	}
	

	protected void chat(String msg) {
		if (RaspberryJamMod.globalChatMessages) {
			globalMessage(msg);
		}
		else if (! RaspberryJamMod.integrated) {
			if (verifiedUser)
				chat(playerId, msg);
			else
				globalMessage(msg);
		}
		else {
			mc.thePlayer.addChatComponentMessage(new TextComponentString(msg));
		}
	}
	
	protected void spawnParticle(Scanner scan) {
		String particleName = scan.next();
		double x0 = scan.nextDouble();
		double y0 = scan.nextDouble();
		double z0 = scan.nextDouble();
		Vec3w pos = Location.decodeVec3w(serverWorlds, x0, y0, z0);
		double dx = scan.nextDouble();
		double dy = scan.nextDouble();
		double dz = scan.nextDouble();
		double speed = scan.nextDouble();
		int count = scan.nextInt();

		int[] extras = null;
		EnumParticleTypes particle = null;
		for (EnumParticleTypes e : EnumParticleTypes.values()) {
			if (e.getParticleName().equals(particleName)) {
				particle = e;
				extras = new int[e.getArgumentCount()];
				try {
					for (int i = 0 ; i < extras.length; i++)
						extras[i] = scan.nextInt();
				}
				catch (Exception exc) {}
				break;
			}
		}
		if (particle == null) {
			fail("Cannot find particle type");
		}
		else {
			((WorldServer)pos.world).spawnParticle(particle, false, pos.xCoord, pos.yCoord, pos.zCoord, count, 
					dx, dy, dz, speed, extras);
		}
	}
	
	protected void cameraCommand(String cmd, Scanner scan) {
		if (! havePlayer)
			fail("Do not have a player (yet?)");
        //updatePlayerMP();
        if (playerMP == null)
            fail("Player not found (in camera.*)");
		if (cmd.equals(GETENTITYID)) {
			sendLine(playerMP.getSpectatingEntity().getEntityId());
		}
		else if (cmd.equals(SETFOLLOW) || cmd.equals(SETNORMAL)) {
			if (! RaspberryJamMod.integrated)
				return;
			
			mc.gameSettings.debugCamEnable = false;
			boolean follow = cmd.equals(SETFOLLOW);

			if (playerMP != null) {
				if (! scan.hasNext()) {
					playerMP.setSpectatingEntity(null);
				}
				else {
					Entity entity = getServerEntityByID(scan.nextInt());
					if (entity != null) {
						playerMP.setSpectatingEntity(entity);
					}
				}
			}

			if (follow) {
				mc.gameSettings.thirdPersonView = 1;
				mc.entityRenderer.loadEntityShader((Entity)null);
			}
			else {
				mc.gameSettings.thirdPersonView = 0;
				mc.entityRenderer.loadEntityShader(mc.getRenderViewEntity());
			}
		}
		else if (cmd.equals(SETDEBUG)) {
			if (! RaspberryJamMod.integrated)
				return;
			
			mc.gameSettings.debugCamEnable = true;
		}
		else if (cmd.equals(SETDISTANCE)) {
			Float d = scan.nextFloat();
			Class c = net.minecraft.client.renderer.EntityRenderer.class;
			try {
				Field f = c.getDeclaredField("thirdPersonDistance");
				f.setAccessible(true);
				f.set(mc.entityRenderer,d);
			}
			catch (Exception e) {
				System.out.println(""+e);
			}
			try {
				Field f = c.getDeclaredField("thirdPersonDistanceTemp");
				f.setAccessible(true);
				f.set(mc.entityRenderer,d);
			}
			catch (Exception e) {
				System.out.println(""+e);
			}
		}
		else {
			unknownCommand();
		}
	}

	protected void entityCommand(int id, String cmd, Scanner scan) {
		Entity e = getServerEntityByID(id);
		if (e == null) {
			fail("cannot find entity");
			return;
		}
		if (cmd.equals(GETPOS)) {
			entityGetPos(id);
		}
		else if (cmd.equals(GETTILE)) {
			entityGetTile(id);
		}
		else if (cmd.equals(GETROTATION)) {
			entityGetRotation(id);
		}
		else if (cmd.equals(SETROTATION)) {
			entitySetRotation(id, scan.nextFloat());
		}
		else if (cmd.equals(GETPITCH)) {
			entityGetPitch(id);
		}
		else if (cmd.equals(SETPITCH)) {
			entitySetPitch(id, scan.nextFloat());
		}
		else if (cmd.equals(GETDIRECTION)) {
			entityGetDirection(id);
		}
		else if (cmd.equals(SETDIRECTION)) {
			entitySetDirection(id, scan);
		}
		else if (cmd.equals(SETTILE)) {
			entitySetTile(id, scan);
		}
		else if (cmd.equals(SETPOS)) {
			entitySetPos(id, scan);
		}
		else if (cmd.equals(SETDIMENSION)) {			
			entitySetDimension(id, scan.nextInt());
		}
		else if (cmd.equals(GETNAME)) {
			entityGetNameAndUUID(id, false);
		}
		else if (cmd.equals(GETNAMEUUID)) {
			entityGetNameAndUUID(id, true);
		}
        else if (cmd.equals(CHAT)) {
            chat(id, scan.next());
        }
		else {
			unknownCommand();
		}
	}
	
	protected void entityGetNameAndUUID(int id, boolean includeUUID) {
		Entity e = getServerEntityByID(id);
        if (e == null) {
            fail("Cannot find entity");
        }
        if (includeUUID)
            sendLine(e.getName()+","+e.getUniqueID());
        else
            sendLine(e.getName());
	}

	protected void entitySetDirection(int id, Scanner scan) {
		double x  = scan.nextDouble();
		double y = scan.nextDouble();
		double z = scan.nextDouble();
		Entity e = getServerEntityByID(id);
		if (e != null)
			entitySetDirection(e, x, y, z);
		
		if (!RaspberryJamMod.integrated)
			return;
		
		e = mc.theWorld.getEntityByID(id);
		if (e != null)
			entitySetDirection(e, x, y, z);
	}

	static protected String getRest(Scanner scan) {
		StringBuilder out = new StringBuilder();

		while (scan.hasNext()) {
			if (out.length() > 0)
				out.append(",");
			out.append(scan.next());
		}
		return out.toString();
	}
	
	protected void entitySetDimension(int id, int dimension) {
		Entity e = getServerEntityByID(id);
		if (e != null) 
			eventHandler.queueServerAction(new SetDimension(e, dimension));
        else
            fail("Cannot find entity");
	}

	protected void entitySetDirection(Entity e, double x, double y, double z) {
		double xz = Math.sqrt(x * x + z * z);

		if (xz >= TOO_SMALL) {
			float yaw = (float) (Math.atan2(-x, z) * 180 / Math.PI);
			e.setRotationYawHead(yaw);
			e.rotationYaw = yaw;
		}

		if (x * x + y * y + z * z >= TOO_SMALL * TOO_SMALL)
			e.rotationPitch = (float) (Math.atan2(-y, xz) * 180 / Math.PI);
	}

	protected void fail(String string) {
		System.err.println("Error: "+string);
		sendLine("Fail");
	}
	
	protected void entitySetPitch(int id, float angle) {
		Entity e = getServerEntityByID(id);
		if (e != null)
			e.rotationPitch = angle;
		
		if (!RaspberryJamMod.integrated)
			return;
		
		e = mc.theWorld.getEntityByID(id);
		if (e != null)
			e.rotationPitch = angle;
	}

	protected void entitySetRotation(int id, float angle) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			e.rotationYaw = angle;
			e.setRotationYawHead(angle);
		}

		if (!RaspberryJamMod.integrated)
			return;
		
		e = mc.theWorld.getEntityByID(id);
		if (e != null) {
			e.rotationYaw = angle;
			e.setRotationYawHead(angle);
		}
	}
	
	protected void entityGetRotation(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) 
			sendLine(normalizeAngle(e.rotationYaw));
        else
            fail("Cannot find entity");
	}

	protected float normalizeAngle(float angle) {
		angle = angle % 360;
		if (angle <= -180)
			angle += 360;
		if (angle > 180)
			angle -= 360;
		return angle;
	}

	protected void entityGetPitch(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) 
			sendLine(normalizeAngle(e.rotationPitch));
        else
            fail("Cannot find entity");
	}

	protected void entityGetDirection(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			//sendLine(e.getLookVec());
			double pitch = e.rotationPitch * Math.PI / 180.;
			double yaw = e.rotationYaw * Math.PI / 180.;
			double x = Math.cos(-pitch) * Math.sin(-yaw);
			double z = Math.cos(-pitch) * Math.cos(-yaw);
			double y = Math.sin(-pitch);
			sendLine(new Vec3d(x,y,z));
		}
        else
            fail("Cannot find entity");
	}

	protected void entitySetPos(int id, Scanner scan) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			float serverYaw = 0f;
			serverYaw = e.rotationYaw;
	
			double x = scan.nextDouble();
			double y = scan.nextDouble();
			double z = scan.nextDouble();
			Vec3w pos = Location.decodeVec3w(serverWorlds, x, y, z);
			if (pos.world != e.getEntityWorld()) {
//				e.setWorld(pos.world);
				System.out.println("World change unsupported");
				// TODO: implement moving between worlds
				return;
			}
			e.setPositionAndUpdate(pos.xCoord,pos.yCoord,pos.zCoord);
			e.setRotationYawHead(serverYaw);
	
			if (!RaspberryJamMod.integrated)
				return;
			
			e = mc.theWorld.getEntityByID(id);
			if (e != null) {
				e.rotationYaw = serverYaw;
				e.setRotationYawHead(serverYaw);
			}
		}
        else
            fail("Cannot find entity");
	}

	protected void entitySetTile(int id, Scanner scan) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			float serverYaw = 0f;
			if (e != null) {
				serverYaw = e.rotationYaw;
				Location pos = getBlockLocation(scan);
				if (pos.world != e.getEntityWorld()) {
					// TODO: implement moving between worlds
					return;
				}
				e.setPositionAndUpdate(pos.getX()+0.5, pos.getY(), (double)pos.getZ()+0.5);
				e.setRotationYawHead(serverYaw);
			}

			if (!RaspberryJamMod.integrated)
				return;
			
			e = mc.theWorld.getEntityByID(id);
			if (e != null) {
				e.rotationYaw = serverYaw;
				e.setRotationYawHead(serverYaw);
			}
		}
        else
            fail("Cannot find entity");
	}

	protected static int trunc(double x) {
		return (int)Math.floor(x);
	}

	protected void entityGetTile(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			World w = e.getEntityWorld();
			Vec3d pos0 = e.getPositionVector();

			while (w != e.getEntityWorld()) {
				// Rare concurrency issue: entity switched worlds between getting w and pos0.
				// To be somewhat safe, let's sleep for approximately a server tick and get
				// everything again. 
				try { Thread.sleep(50); } catch(Exception exc) {}
				w = e.getEntityWorld();
				pos0 = e.getPositionVector();
			}
			
			Vec3d pos = Location.encodeVec3(serverWorlds, w, e.getPositionVector());
			sendLine(""+trunc(pos.xCoord)+","+trunc(pos.yCoord)+","+trunc(pos.zCoord));
		}
        else
            fail("Cannot find entity");
	}

	protected void sendLine(BlockPos pos) {
		sendLine(""+pos.getX()+","+pos.getY()+","+pos.getZ());
	}

	protected void entityGetPos(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			World w = e.getEntityWorld();
			Vec3d pos0 = e.getPositionVector();
			while (w != e.getEntityWorld()) {
				// Rare concurrency issue: entity switched worlds between getting w and pos0.
				// To be somewhat safe, let's sleep for approximately a server tick and get
				// everything again. 
				try { Thread.sleep(50); } catch(Exception exc) {}
				w = e.getEntityWorld();
				pos0 = e.getPositionVector();
			}
			
			Vec3d pos = Location.encodeVec3(serverWorlds, w, pos0);
			sendLine(pos);
		}
        else
            fail("Cannot find entity");
	}

	protected void sendLine(double x) {
		sendLine(Double.toString(x));
	}

	protected void sendLine(int x) {
		sendLine(Integer.toString(x));
	}

	protected void sendLine(Vec3d v) {
		sendLine(""+v.xCoord+","+v.yCoord+","+v.zCoord);
	}

	protected void sendLine(String string) {
		try {
			writer.print(string+"\n");
			writer.flush();
		}
		catch(Exception e) {					
		}
	}

	protected Location getBlockLocation(Scanner scan) {
		int x = scan.nextInt();
		int y = scan.nextInt();
		int z = scan.nextInt();
		return Location.decodeLocation(serverWorlds, x, y, z);
	}

	protected Entity getServerEntityByID(int id) {
		if (id == playerId) {
			return playerMP;
        }

		UUID uuid = idToUUID.get(id);

		if (uuid != null) {
			return RaspberryJamMod.minecraftServer.getPlayerList().getPlayerByUUID(uuid);
		}

		for (EntityPlayerMP player : RaspberryJamMod.minecraftServer.getPlayerList().getPlayerList()) 
			if (player.getEntityId() == id) {
				idToUUID.put(id, player.getUniqueID());
				return player;
			}

		for (World w : serverWorlds) {
			Entity e = w.getEntityByID(id);
			if (e != null)
				return e;
		}

		return null;
	}

	static void globalMessage(String message) {
		for (EntityPlayerMP player : RaspberryJamMod.minecraftServer.getPlayerList().getPlayerList())  {
			player.addChatComponentMessage(new TextComponentString(message));
		}
	}

	public void click(PlayerInteractEvent event, boolean right) {
		EntityPlayer player = event.getEntityPlayer();
		
		if (player == null || player.getEntityWorld().isRemote != RaspberryJamMod.clientOnlyAPI )
			return;
		
		if (right || detectLeftClick) {
			if (! restrictToSword || holdingSword(player)) {
				synchronized(hits) {
					if (hits.size() >= MAX_HITS)
						hits.remove(0);
					hits.add(new HitDescription(eventHandler.getWorlds(),event));
				}
			}
		}
		if (stopChanges && (RaspberryJamMod.globalImmutable || 
								(havePlayer && playerId == player.getEntityId()))) {
			event.setCanceled(true);
		}
	}

	private boolean holdingSword(EntityPlayer player) {
		ItemStack item = player.getHeldItemMainhand();
		if (item != null) {
			return item.getItem() instanceof ItemSword;
		}
		return false;
	}
	
	public void setRestrictToSword(boolean value) {
		restrictToSword = value;
	}

	public String getHitsAndClear() {
		String out = "";

		synchronized(hits) {
			int count = hits.size();
			for (HitDescription e : hits) {
				if (out.length() > 0)
					out += "|";
				out += e.getDescription();
			}
			hits.clear();
		}

		return out;
	}

	public String getChatsAndClear() {
		StringBuilder out = new StringBuilder();

		synchronized(chats) {
			int count = hits.size();
			for (ChatDescription c : chats) {
				if (out.length() > 0)
					out.append("|");
				out.append(c.id);
				out.append(",");
				out.append(c.message.replace("&","&amp;").replace("|", "&#124;"));
			}
			chats.clear();
		}

		return out.toString();
	}

	public int eventCount() {
		synchronized(hits) {
			return hits.size();
		}
	}

	public void clearHits() {
		synchronized(hits) {
			hits.clear();
		}
	}

	public void clearChats() {
		synchronized(chats) {
			chats.clear();
		}
	}
	
	public void clearAllEvents() {
		hits.clear();
		chats.clear();
	}
	
	public void addChatDescription(ChatDescription cd) {
		synchronized(chats) {
			if (chats.size() >= MAX_CHATS)
				chats.remove(0);
			chats.add(cd);
		}
	}

	static class ChatDescription {
		int id;
		String message;
		public ChatDescription(int entityId, String message) {
			this.id = entityId;
			this.message = message;
		}
	}
	

	static class HitDescription {
		private String description;
		
		public HitDescription(World[] worlds, PlayerInteractEvent event) {
			Vec3i pos = Location.encodeVec3i(worlds, 
					event.getEntityPlayer().getEntityWorld(),
					event.getPos().getX(), event.getPos().getY(), event.getPos().getZ());
			description = ""+pos.getX()+","+pos.getY()+","+pos.getZ()+","+
					numericFace(event.getFace())+","+event.getEntity().getEntityId();
		}

		private int numericFace(EnumFacing face) {
            if (face == null)
                return 7;
			switch(face) {
			case DOWN:
				return 0;
			case UP:
				return 1;
			case NORTH:
				return 2;
			case SOUTH:
				return 3;
			case WEST:
				return 4;
			case EAST:
				return 5;
			default:
				return 7;
			}
		}

		public String getDescription() {
			return description;
		}
	}
}

package mobi.omegacentauri.raspberryjammod;

// TODO: getHeight() should check block queue

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.InputMismatchException;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Scanner;

import javax.swing.text.html.HTMLDocument.HTMLReader.IsindexAction;

import mobi.omegacentauri.raspberryjammod.APIHandler.ChatDescription;
import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityList;
import net.minecraft.entity.EntityLiving;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.init.Blocks;
import net.minecraft.item.ItemStack;
import net.minecraft.item.ItemSword;
import net.minecraft.nbt.JsonToNBT;
import net.minecraft.nbt.NBTException;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.network.play.server.S43PacketCamera;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.BlockPos;
import net.minecraft.util.ChatComponentText;
import net.minecraft.util.EnumFacing;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.util.IChatComponent;
import net.minecraft.util.Vec3;
import net.minecraft.util.Vec3i;
import net.minecraft.world.World;
import net.minecraft.world.WorldServer;
import net.minecraft.world.WorldSettings;
import net.minecraft.world.chunk.Chunk;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;

public class APIHandler {
	// world.checkpoint.save/restore, player.setting, world.setting(nametags_visible,*),
	// camera.setFixed() unsupported
	// camera.setNormal(id) and camera.setFollow(id) uses spectating, and so it moves the
	// player along with the entity that was set as camera
	protected static final String CHAT = "chat.post";
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

	protected static final String GETLIGHTLEVEL = "block.getLightLevel"; // EXPERIMENTAL AND UNSUPPORTED
	protected static final String SETLIGHTLEVEL = "block.setLightLevel"; // EXPERIMENTAL AND UNSUPPORTED


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
	protected static final String GETDIRECTION = "getDirection";
	protected static final String GETPITCH = "getPitch";
	protected static final String GETPOS = "getPos";
	protected static final String GETROTATION = "getRotation";
	protected static final String GETTILE = "getTile";
	protected static final String SETDIMENSION = "setDimension"; // EXPERIMENTAL AND UNSUPPORTED
	protected static final String SETDIRECTION = "setDirection";
	protected static final String SETPITCH = "setPitch";
	protected static final String SETPOS = "setPos";
	protected static final String SETROTATION = "setRotation";
	protected static final String SETTILE = "setTile";
	protected static final String GETNAME = "getNameAndUUID";

	protected static final float TOO_SMALL = (float) 1e-9;

	protected World[] serverWorlds;
	protected MCEventHandler eventHandler;
	protected boolean listening = true;
	protected Minecraft mc;
	protected PrintWriter writer = null;
	protected boolean includeNBTWithData = false;
	protected boolean havePlayer;
	protected int playerId;
	protected EntityPlayerMP playerMP;
	private List<HitDescription> hits = new LinkedList<HitDescription>();
	protected List<ChatDescription> chats = new LinkedList<ChatDescription>();
	protected static final int MAX_CHATS = 512;
	private static final int MAX_HITS = 512;
	private volatile boolean restrictToSword = true;
	private volatile boolean detectLeftClick = RaspberryJamMod.leftClickToo;

	public APIHandler(MCEventHandler eventHandler, PrintWriter writer) throws IOException {
		this.eventHandler = eventHandler;
		this.writer = writer;
		this.havePlayer = false;
		this.playerMP = null;
		detectLeftClick = RaspberryJamMod.leftClickToo;
		eventHandler.registerAPIHandler(this);
	}
	
	protected boolean setup() {
		serverWorlds = MinecraftServer.getServer().worldServers;
		
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
				playerId = mc.thePlayer.getEntityId();
				for (World w : serverWorlds) {
					Entity e = w.getEntityByID(playerId);
					if (e != null)
						playerMP = (EntityPlayerMP)e;
				}
			}
			else {
				playerMP = null;
				int firstId = 0;
				
				for (World w : serverWorlds) {
					for (EntityPlayerMP p : (List<EntityPlayerMP>)w.playerEntities) {
						int id = p.getEntityId();
						if (playerMP == null || id < firstId) {
							firstId = id;
							playerMP = p;
						}
					}
				}
			}
			if (playerMP == null) {
				fail("Player not found");
				return false;
			}
			havePlayer = true;
		}
		return true;
	}

	void process(String clientSentence) {
		if (!setup())
			return;
	
		Scanner scan = null;

		try {	
			int paren = clientSentence.indexOf('(');
			if (paren < 0)
				return;
			
			String cmd = clientSentence.substring(0, paren);
			String args = clientSentence.substring(paren + 1).replaceAll("[\\s\r\n]+$", "").replaceAll("\\)$", "");
		
			if (cmd.startsWith("player.")) {
				// Compatibility with the mcpi library included with Juice
				if (args.startsWith("None,")) {
					args = args.substring(5);
				}
				else if (args.equals("None")) {
					args = "";
				}
			}

			scan = new Scanner(args);
			scan.useDelimiter(",");

			synchronized (eventHandler) {
				runCommand(cmd, args, scan);
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


	protected void runCommand(String cmd, String args, Scanner scan) 
			throws InputMismatchException, NoSuchElementException, IndexOutOfBoundsException {

		if (cmd.equals(SETBLOCK)) {
			Location pos = getBlockLocation(scan);
			short id = scan.nextShort();
			short meta = scan.hasNextShort() ? scan.nextShort() : 0;
			String tagString = getRest(scan);

			SetBlockState setState;

			if (tagString.contains("{")) {
				try {
					setState = new SetBlockNBT(pos, id, meta, JsonToNBT.func_180713_a(tagString));
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
				Block b = chunk.getBlock(x,y,z);
				if (b != Blocks.air) {
					h = y;
					break;
				}
			}

			h -= serverWorlds[0].getSpawnPoint().getY();

			sendLine(h);
		}
		else if (cmd.equals(GETLIGHTLEVEL)) {
			sendLine(Block.getBlockById(scan.nextInt()).getLightValue()/15.);
		}
		else if (cmd.equals(SETLIGHTLEVEL)) {
			int id = scan.nextInt();
			float value = scan.nextFloat();
			Block.getBlockById(id).setLightLevel(value);
		}
		else if (cmd.equals(SETBLOCKS)) {
			Location pos1 = getBlockLocation(scan);
			Location pos2 = getBlockLocation(scan);

			short id = scan.nextShort();
			short meta = scan.hasNextShort() ? scan.nextShort() : 0;

			String tagString = getRest(scan);

			SetBlocksState setState;

			if (tagString.contains("{")) {
				try {
					setState = new SetBlocksNBT(pos1, pos2, id, meta, JsonToNBT.func_180713_a(tagString));
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
			entityCommand(playerId, cmd.substring(7), scan);
		}
		else if (cmd.startsWith("entity.")) {
			entityCommand(scan.nextInt(), cmd.substring(7), scan);
		}
		else if (cmd.equals(CHAT)) {
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
				for (World w : serverWorlds) {
					for (EntityPlayer p : (List<EntityPlayer>)w.playerEntities) {
						if (p.getName().equals(name)) {
							sendLine(p.getEntityId());
							return;
						}
					}
				}
				fail("Unknown player");
			}
			else {
				// unofficial API to get current player ID
				sendLine(playerId);
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
			if (setting.equals("world_immutable")) // across connections
				eventHandler.setStopChanges(scan.nextInt() != 0);
			else if (setting.equals("include_nbt_with_data")) // connection-specific
				includeNBTWithData = (scan.nextInt() != 0);
			else if (setting.equals("pause_drawing")) // across connections
				eventHandler.setPause(scan.nextInt() != 0);
			// name_tags not supported
		}
		else if (cmd.equals(EVENTSSETTING)) {
			String setting = scan.next();
			if (setting.equals("restrict_to_sword")) // connection-specific
				restrictToSword = (scan.nextInt() != 0);
			else if (setting.equals("detect_left_click")) // connection-specific
				detectLeftClick = (scan.nextInt() != 0);
		}
		else if (cmd.startsWith("camera.")) {
			cameraCommand(cmd.substring(7), scan);
		}
        else {
            unknownCommand();
        }
	}
	
	protected void removeEntity(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null)
			e.getEntityWorld().removeEntity(e);
	}

	protected void spawnEntity(Scanner scan) {
		String entityId = scan.next();
		double x0 = scan.nextDouble();
		double y0 = scan.nextDouble();
		double z0 = scan.nextDouble();
		Vec3w pos = Location.decodeVec3w(serverWorlds, x0, y0, z0);
		String tagString = getRest(scan);
		Entity entity;
		if (tagString.length() > 0) {
			NBTTagCompound tags;
			try {
				tags = JsonToNBT.func_180713_a(tagString);
			} catch (NBTException e) {
				fail("Cannot parse tags");
				return;
			}
			tags.setString("id", entityId);
			entity = EntityList.createEntityFromNBT(tags, pos.world);
		}
		else {
			entity = EntityList.createEntityByName(entityId, pos.world);
		}

		if (entity == null) {
			fail("Cannot create entity");
		}
		else {
			entity.setPositionAndUpdate(pos.xCoord, pos.yCoord, pos.zCoord);
			pos.world.spawnEntityInWorld(entity);
			sendLine(entity.getEntityId());
		}
	}

	protected void chat(String msg) {
		if (! RaspberryJamMod.integrated || RaspberryJamMod.globalChatMessages) {
			globalMessage(msg);
		}
		else {
			mc.thePlayer.addChatComponentMessage(new ChatComponentText(msg));
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
    
    protected void unknownCommand() {
        fail("unknown command");
    }

	protected void entityCommand(int id, String cmd, Scanner scan) {
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
			entityGetNameAndUUID(id);
		}
        else {
            unknownCommand();
        }
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
	}

	protected void entityGetNameAndUUID(int id) {
		Entity e = getServerEntityByID(id);
        if (e == null)
            fail("Unknown entity");
        else
            sendLine(e.getName()+","+e.getUniqueID());
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
			sendLine(new Vec3(x,y,z));
		}
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
	}

	protected static int trunc(double x) {
		return (int)Math.floor(x);
	}

	protected void entityGetTile(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			World w = e.getEntityWorld();
			Vec3 pos0 = e.getPositionVector();

			while (w != e.getEntityWorld()) {
				// Rare concurrency issue: entity switched worlds between getting w and pos0.
				// To be somewhat safe, let's sleep for approximately a server tick and get
				// everything again. 
				try { Thread.sleep(50); } catch(Exception exc) {}
				w = e.getEntityWorld();
				pos0 = e.getPositionVector();
			}
			
			Vec3 pos = Location.encodeVec3(serverWorlds, w, e.getPositionVector());
			sendLine(""+trunc(pos.xCoord)+","+trunc(pos.yCoord)+","+trunc(pos.zCoord));
		}
	}

	protected void sendLine(BlockPos pos) {
		sendLine(""+pos.getX()+","+pos.getY()+","+pos.getZ());
	}

	protected void entityGetPos(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) {
			World w = e.getEntityWorld();
			Vec3 pos0 = e.getPositionVector();
			while (w != e.getEntityWorld()) {
				// Rare concurrency issue: entity switched worlds between getting w and pos0.
				// To be somewhat safe, let's sleep for approximately a server tick and get
				// everything again. 
				try { Thread.sleep(50); } catch(Exception exc) {}
				w = e.getEntityWorld();
				pos0 = e.getPositionVector();
			}
			
			Vec3 pos = Location.encodeVec3(serverWorlds, w, pos0);
			sendLine(pos);
		}
	}

	protected void sendLine(double x) {
		sendLine(Double.toString(x));
	}

	protected void sendLine(int x) {
		sendLine(Integer.toString(x));
	}

	protected void sendLine(Vec3 v) {
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
		if (id == playerId)
			return playerMP;
		for (World w : serverWorlds) {
			Entity e = w.getEntityByID(id);
			if (e != null)
				return e;
		}
		fail("Cannot find entity "+id);
		return null;
	}

	static void globalMessage(String message) {
		for (World w : MinecraftServer.getServer().worldServers) {
			for (EntityPlayer p : (List<EntityPlayer>)w.playerEntities ) {
				p.addChatComponentMessage(new ChatComponentText(message));
			}
		}
	}

	public void close() {
		eventHandler.unregisterAPIHandler(this);
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
					event.entityPlayer.getEntityWorld(),
					event.pos.getX(), event.pos.getY(), event.pos.getZ());
			description = ""+pos.getX()+","+pos.getY()+","+pos.getZ()+","+numericFace(event.face)+","+event.entity.getEntityId();
		}

		private int numericFace(EnumFacing face) {
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


	public void onClick(PlayerInteractEvent event) {
		if (event.action == PlayerInteractEvent.Action.RIGHT_CLICK_BLOCK ||
				(detectLeftClick && event.action == PlayerInteractEvent.Action.LEFT_CLICK_BLOCK)) {
			if (! restrictToSword || holdingSword(event.entityPlayer)) {
				synchronized(hits) {
					if (hits.size() >= MAX_HITS)
						hits.remove(0);
					hits.add(new HitDescription(eventHandler.getWorlds(),event));
				}
			}
		}
		if (eventHandler.stopChanges) {
			event.setCanceled(true);
		}
	}


	private boolean holdingSword(EntityPlayer player) {
		ItemStack item = player.getHeldItem();
		if (item != null) {
			return item.getItem() instanceof ItemSword;
		}
		return false;
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
	
}

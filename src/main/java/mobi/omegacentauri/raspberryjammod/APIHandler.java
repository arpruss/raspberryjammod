package mobi.omegacentauri.raspberryjammod;

// TODO: getHeight() should check block queue

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.InputMismatchException;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Scanner;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
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

public class APIHandler {
	// world.checkpoint.save/restore, player.setting, world.setting(nametags_visible,*),
	// camera.setFixed() unsupported
	// camera.setNormal(id) and camera.setFollow(id) uses spectating, and so it moves the
	// player along with the entity that was set as camera
	private static final String CHAT = "chat.post";
	private static final String SETBLOCK = "world.setBlock";
	private static final String SETBLOCKS = "world.setBlocks"; 
	private static final String GETBLOCK = "world.getBlock";
	private static final String GETBLOCKWITHDATA = "world.getBlockWithData";
	private static final String GETHEIGHT = "world.getHeight"; 

	private static final String GETLIGHTLEVEL = "block.getLightLevel";
	private static final String SETLIGHTLEVEL = "block.setLightLevel";

	private static final String WORLDSPAWNENTITY = "world.spawnEntity";
	private static final String WORLDDELETEENTITY = "world.removeEntity";
	private static final String WORLDGETPLAYERIDS = "world.getPlayerIds"; 	
	private static final String WORLDGETPLAYERID = "world.getPlayerId"; 
	private static final String WORLDSETTING = "world.setting";

	private static final String EVENTSBLOCKHITS = "events.block.hits";
	private static final String EVENTSCHATPOSTS = "events.chat.posts";
	private static final String EVENTSCLEAR = "events.clear";
	private static final String EVENTSSETTING = "events.setting";

	private static final String CAMERASETFOLLOW = "camera.setFollow";
	private static final String CAMERASETNORMAL = "camera.setNormal";
	private static final String CAMERAGETENTITYID = "camera.getEntityId";
	private static final String CAMERASETDEBUG = "camera.setDebug";

	// player.* or entity.*
	private static final String GETDIRECTION = "getDirection";
	private static final String GETPITCH = "getPitch";
	private static final String GETPOS = "getPos";
	private static final String GETROTATION = "getRotation";
	private static final String GETTILE = "getTile";
	private static final String SETDIMENSION = "setDimension";
	private static final String SETDIRECTION = "setDirection";
	private static final String SETPITCH = "setPitch";
	private static final String SETPOS = "setPos";
	private static final String SETROTATION = "setRotation";
	private static final String SETTILE = "setTile";

	private static final float TOO_SMALL = (float) 1e-9;

	private World[] serverWorlds;
	private MCEventHandler eventHandler;
	private boolean listening = true;
	private Minecraft mc;
	private int connectionsActive = 0;
	DataOutputStream writer = null;
	private boolean includeNBTWithData = false;
	private boolean havePlayer;
	private int playerId;
	private EntityPlayerMP playerMP;

	public APIHandler(MCEventHandler eventHandler, DataOutputStream writer) throws IOException {
		this.eventHandler = eventHandler;
		this.writer = writer;
		this.havePlayer = false;
		this.playerMP = null;
	}

	void process(String clientSentence) {
		Scanner scan = null;
		
		serverWorlds = MinecraftServer.getServer().worldServers;
		
		if (serverWorlds == null) {
			fail("Worlds not available");
			return;
		}

		if (! havePlayer) {
			if (RaspberryJamMod.integrated) {
				mc = Minecraft.getMinecraft();
				
				if (mc == null) {
					fail("Minecraft client not yet available");
				}
				
				if (mc.thePlayer == null) {
					fail("Client player not available");
					return;
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
				return;
			}
			havePlayer = true;
		}

		try {	
			int paren = clientSentence.indexOf('(');
			if (paren < 0)
				return;
			String cmd = clientSentence.substring(0, paren);
			String args = clientSentence.substring(paren + 1).replaceAll("[\\s\r\n]+$", "").replaceAll("\\)$", "");

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
			e.printStackTrace(System.out);
		}
		finally {
			if (scan != null)
				scan.close();
		}
	}


	private void runCommand(String cmd, String args, Scanner scan) 
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
			if (RaspberryJamMod.globalChatMessages) {
				globalMessage(args);
			}
			else {
				Minecraft.getMinecraft().thePlayer.addChatComponentMessage(new ChatComponentText(args));
			}
		}
		else if (cmd.equals(WORLDGETPLAYERIDS)) {
			// TODO : ensure local player is first (lowest number?!)
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
							break;
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
			Entity e = getServerEntityByID(scan.nextInt());
			if (e != null)
				e.getEntityWorld().removeEntity(e);
		}
		else if (cmd.equals(WORLDSPAWNENTITY)) {
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
		else if (cmd.equals(EVENTSCLEAR)) {
			eventHandler.clearAll();
		}
		else if (cmd.equals(EVENTSBLOCKHITS)) {
			sendLine(eventHandler.getHitsAndClear());
		}
		else if (cmd.equals(EVENTSCHATPOSTS)) {
			sendLine(eventHandler.getChatsAndClear());
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
			if (scan.next().equals("restrict_to_sword")) // across connections
				eventHandler.setRestrictToSword(scan.nextInt() != 0);
		}
		else if (cmd.equals(CAMERAGETENTITYID)) {
			sendLine(playerMP.getSpectatingEntity().getEntityId());
		}
		else if (cmd.equals(CAMERASETFOLLOW) || cmd.equals(CAMERASETNORMAL)) {
			if (! RaspberryJamMod.integrated)
				return;
			
			mc.gameSettings.debugCamEnable = false;
			boolean follow = cmd.equals(CAMERASETFOLLOW);

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
		else if (cmd.equals(CAMERASETDEBUG)) {
			if (! RaspberryJamMod.integrated)
				return;
			
			mc.gameSettings.debugCamEnable = true;
		}
	}

	private void entityCommand(int id, String cmd, Scanner scan) {
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
	}

	private void entitySetDirection(int id, Scanner scan) {
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

	static private String getRest(Scanner scan) {
		StringBuilder out = new StringBuilder();

		while (scan.hasNext()) {
			if (out.length() > 0)
				out.append(",");
			out.append(scan.next());
		}
		return out.toString();
	}
	
	private void entitySetDimension(int id, int dimension) {
		Entity e = getServerEntityByID(id);
		if (e != null) 
			eventHandler.queueServerAction(new SetDimension(e, dimension));
	}

	private void entitySetDirection(Entity e, double x, double y, double z) {
		double xz = Math.sqrt(x * x + z * z);

		if (xz >= TOO_SMALL) {
			float yaw = (float) (Math.atan2(-x, z) * 180 / Math.PI);
			e.setRotationYawHead(yaw);
			e.rotationYaw = yaw;
		}

		if (x * x + y * y + z * z >= TOO_SMALL * TOO_SMALL)
			e.rotationPitch = (float) (Math.atan2(-y, xz) * 180 / Math.PI);
	}

	private void fail(String string) {
		System.err.println("Error: "+string);
		sendLine("Fail");
	}
	
	private void entitySetPitch(int id, float angle) {
		Entity e = getServerEntityByID(id);
		if (e != null)
			e.rotationPitch = angle;
		
		if (!RaspberryJamMod.integrated)
			return;
		
		e = mc.theWorld.getEntityByID(id);
		if (e != null)
			e.rotationPitch = angle;
	}

	private void entitySetRotation(int id, float angle) {
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
	
	private void entityGetRotation(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) 
			sendLine(normalizeAngle(e.rotationYaw));
	}

	private float normalizeAngle(float angle) {
		angle = angle % 360;
		if (angle <= -180)
			angle += 360;
		if (angle > 180)
			angle -= 360;
		return angle;
	}

	private void entityGetPitch(int id) {
		Entity e = getServerEntityByID(id);
		if (e != null) 
			sendLine(normalizeAngle(e.rotationPitch));
	}

	private void entityGetDirection(int id) {
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

	private void entitySetPos(int id, Scanner scan) {
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

	private void entitySetTile(int id, Scanner scan) {
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

	private static int trunc(double x) {
		return (int)Math.floor(x);
	}

	private void entityGetTile(int id) {
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

	private void sendLine(BlockPos pos) {
		sendLine(""+pos.getX()+","+pos.getY()+","+pos.getZ());
	}

	private void entityGetPos(int id) {
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

	private void sendLine(double x) {
		sendLine(Double.toString(x));
	}

	private void sendLine(int x) {
		sendLine(Integer.toString(x));
	}

	private void sendLine(Vec3 v) {
		sendLine(""+v.xCoord+","+v.yCoord+","+v.zCoord);
	}

	private void sendLine(String string) {
		try {
			writer.writeBytes(string+"\n");
			writer.flush();
		}
		catch(Exception e) {					
		}
	}

	private Location getBlockLocation(Scanner scan) {
		int x = scan.nextInt();
		int y = scan.nextInt();
		int z = scan.nextInt();
		return Location.decodeLocation(serverWorlds, x, y, z);
	}
	

	Entity getServerEntityByID(int id) {
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


//	static EntityPlayerMP getServerPlayer() {
//		EntityPlayerSP playerSP = Minecraft.getMinecraft().thePlayer;
//		if (playerSP == null)
//			return null;
//		return (EntityPlayerMP)MinecraftServer.getServer().getEntityWorld().getEntityByID(playerSP.getEntityId());
//	}
}

package mobi.omegacentauri.raspberryjammod;

// TODO: getHeight() should check block queue

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Method;
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

public class APIHandler {
	// world.checkpoint.save/restore, player.setting, world.setting(nametags_visible,*),
	// camera.setFixed() unsupported
	// camera.setNormal(id) and camera.setFollow(id) uses spectating, and so it moves the
	// player along with the entity that was set as camera
	private static final String CHAT = "chat.post";
	public static final String SETBLOCK = "world.setBlock";
	public static final String SETBLOCKS = "world.setBlocks"; 
	private static final String GETBLOCK = "world.getBlock";
	private static final String GETBLOCKWITHDATA = "world.getBlockWithData";
	private static final String GETHEIGHT = "world.getHeight"; 
	
	private static final String WORLDSPAWNENTITY = "world.spawnEntity";
	private static final String WORLDDELETEENTITY = "world.removeEntity";
	private static final String WORLDGETPLAYERIDS = "world.getPlayerIds"; 	
	private static final String WORLDGETPLAYERID = "world.getPlayerId"; 
	private static final String WORLDSETTING = "world.setting";
	
	private static final String PLAYERSETTILE = "player.setTile"; 
	private static final String PLAYERSETPOS = "player.setPos"; 
	private static final String PLAYERSETROTATION = "player.setRotation";   	
	private static final Object PLAYERSETPITCH = "player.setPitch"; 
	private static final Object PLAYERSETDIRECTION = "player.setDirection"; 
	private static final String PLAYERGETDIRECTION = "player.getDirection"; 
	private static final String PLAYERGETROTATION = "player.getRotation"; 
	private static final String PLAYERGETPITCH = "player.getPitch";
	private static final String PLAYERGETPOS = "player.getPos";
	private static final String PLAYERGETTILE = "player.getTile";
	private static final String ENTITYGETDIRECTION = "entity.getDirection"; 
	private static final String ENTITYGETROTATION = "entity.getRotation"; 
	private static final String ENTITYGETPITCH = "entity.getPitch"; 
	private static final String ENTITYSETDIRECTION = "entity.setDirection"; 
	private static final String ENTITYSETROTATION = "entity.setRotation"; 
	private static final String ENTITYSETPITCH = "entity.setPitch"; 
	private static final String ENTITYGETPOS = "entity.getPos"; 
	private static final String ENTITYGETTILE = "entity.getTile"; 
	private static final String ENTITYSETTILE = "entity.setTile"; 
	private static final String ENTITYSETPOS = "entity.setPos";

	private static final String EVENTSBLOCKHITS = "events.block.hits";
	private static final String EVENTSCHATPOSTS = "events.chat.posts";
	private static final String EVENTSCLEAR = "events.clear";
	private static final String EVENTSSETTING = "events.setting";
	
	private static final String CAMERASETFOLLOW = "camera.setFollow";
	private static final String CAMERASETNORMAL = "camera.setNormal";
	private static final String CAMERAGETENTITYID = "camera.getEntityId";

	private static final Block UNKNOWN_BLOCK = Blocks.beacon;

	private static final float TOO_SMALL = (float) 1e-9;

	Block[] typeMap;

	private World serverWorld;
	private MCEventHandler eventHandler;
	private boolean listening = true;
 	private Minecraft mc;
 	private int connectionsActive = 0;
	DataOutputStream writer = null;

	public APIHandler(MCEventHandler eventHandler, DataOutputStream writer) throws IOException {
		this.eventHandler = eventHandler;
		this.writer = writer;
	}

	void process(String clientSentence) {
		Scanner scan = null;
		mc = Minecraft.getMinecraft();
		if (mc == null) {
			fail("Minecraft not available");
			return;
		}
		serverWorld = MinecraftServer.getServer().getEntityWorld();
		if (serverWorld == null) {
			fail("World not available");
			return;
		}
		EntityPlayerSP clientPlayer = mc.thePlayer;
		if (clientPlayer == null) {
			fail("Player not available");
			return;
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
				runCommand(clientPlayer, cmd, args, scan);
			}
	
			scan.close();
			scan = null;
		}
		catch(Exception e) {
			System.out.println(""+e);
		}
		finally {
			if (scan != null)
				scan.close();
		}
	}


	private void runCommand(EntityPlayerSP clientPlayer,
			String cmd, String args, Scanner scan) throws InputMismatchException, NoSuchElementException, 
			IndexOutOfBoundsException {
		
		if (cmd.equals(GETBLOCK)) {
			int id = eventHandler.getBlockId(serverWorld, getBlockPosition(scan));

			sendLine(id);
		}
		else if (cmd.equals(GETBLOCKWITHDATA)) {
			MCEventHandler.BlockState state = eventHandler.getBlockState(serverWorld, getBlockPosition(scan));
			
			sendLine(""+state.id+","+state.meta);
		}
		else if (cmd.equals(GETHEIGHT)) {
			BlockPos pos = getBlockPosition(scan.nextInt(), 0, scan.nextInt());
			Chunk chunk = serverWorld.getChunkFromBlockCoords(pos);
			int h = chunk.getHeight(pos);
			int x = pos.getX();
			int z = pos.getZ();
			for (int y = serverWorld.getHeight() ; y >= h ; y--) {
				Block b = chunk.getBlock(x,y,z);
				if (b != Blocks.air) {
					h = y;
					break;
				}
			}

			h -= serverWorld.getSpawnPoint().getY();

			sendLine(h);
		}
		else if (cmd.equals(SETBLOCK)) {
			BlockPos pos = getBlockPosition(scan);
			short id = scan.nextShort();
			short meta = scan.hasNextShort() ? scan.nextShort() : 0;
			eventHandler.queueSetBlockState(pos, id, meta);
		}
		else if (cmd.equals(SETBLOCKS)) {
			BlockPos pos1 = getBlockPosition(scan);
			BlockPos pos2 = getBlockPosition(scan);

			short id = scan.nextShort();
			short meta = scan.hasNextShort() ? scan.nextShort() : 0;

			int x1 = pos1.getX();
			int x2 = pos2.getX();
			if (x2 < x1) {
				int t = x2;
				x2 = x1;
				x1 = t;
			}
			int y1 = pos1.getY();
			int y2 = pos2.getY();
			if (y2 < y1) {
				int t = y2;
				y2 = y1;
				y1 = t;
			}
			int z1 = pos1.getZ();
			int z2 = pos2.getZ();
			if (z2 < z1) {
				int t = z2;
				z2 = z1;
				z1 = t;
			}
			for (int x = x1; x <= x2; x++)
				for (int y = y1; y <= y2; y++)
					for (int z = z1 ; z <= z2; z++) {
						eventHandler.queueSetBlockState(new BlockPos(x,y,z), id, meta);
					}
		}
		else if (cmd.equals(PLAYERGETPOS)) {
			entityGetPos(clientPlayer);
		}
		else if (cmd.equals(PLAYERGETTILE)) {
			entityGetTile(clientPlayer);
		}
		else if (cmd.equals(CHAT)) {
			Minecraft.getMinecraft().thePlayer.addChatComponentMessage(new ChatComponentText(args));
//			clientPlayer.sendChatMessage(args);
		}
		else if (cmd.equals(WORLDGETPLAYERIDS)) {
			List<EntityPlayer> players = serverWorld.playerEntities;
			String ids = "";
			for (EntityPlayer p : players) {
				if (ids.length() > 0)
					ids += "|";
				ids += p.getEntityId();
			}
			sendLine(ids);
		}
		else if (cmd.equals(WORLDGETPLAYERID)) {
			if (scan.hasNext()) {
				String name = scan.next();
				List<EntityPlayer> players = serverWorld.playerEntities;
				for (EntityPlayer p : players) {
					if (p.getName().equals(name)) {
						sendLine(p.getEntityId());
						break;
					}
				}
				fail("Unknown player");
			}
			else {
				sendLine(clientPlayer.getEntityId());
			}
		}
		else if (cmd.equals(PLAYERSETTILE)) {
			entitySetTile(clientPlayer, scan);
		}
		else if (cmd.equals(PLAYERSETPOS)) {
			entitySetPos(clientPlayer, scan);
		}
		else if (cmd.equals(PLAYERGETDIRECTION)) {
			entityGetDirection(clientPlayer);
		}
		else if (cmd.equals(PLAYERGETROTATION)) {
			entityGetRotation(clientPlayer);
		}
		else if (cmd.equals(PLAYERSETROTATION)) {
			clientPlayer.rotationYaw = scan.nextFloat();
		}
		else if (cmd.equals(PLAYERSETPITCH)) {
			clientPlayer.rotationPitch = scan.nextFloat();
		}
		else if (cmd.equals(WORLDDELETEENTITY)) {
			serverWorld.removeEntity(serverWorld.getEntityByID(scan.nextInt()));
		}
		else if (cmd.equals(WORLDSPAWNENTITY)) {
			String entityId = scan.next();
			BlockPos spawnPos = serverWorld.getSpawnPoint();
			double x = scan.nextDouble() + spawnPos.getX();
			double y = scan.nextDouble() + spawnPos.getY();
			double z = scan.nextDouble() + spawnPos.getZ();
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
				entity = EntityList.createEntityFromNBT(tags, serverWorld);
			}
			else {
				entity = EntityList.createEntityByName(entityId, serverWorld);
			}
			
			if (entity == null) {
				fail("Cannot create entity");
			}
			else {
				entity.setPositionAndUpdate(x, y, z);
				serverWorld.spawnEntityInWorld(entity);
				sendLine(entity.getEntityId());
			}
		}
		else if (cmd.equals(PLAYERSETDIRECTION)) {
			double x = scan.nextDouble();
			double y = scan.nextDouble();
			double z = scan.nextDouble();
			entitySetDirection(clientPlayer, x, y, z);
		}
		else if (cmd.equals(PLAYERGETPITCH)) {
			entityGetPitch(clientPlayer);
		}
		else if (cmd.equals(ENTITYGETPOS)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetPos(e);
			else
				fail("No such entity");
		}
		else if (cmd.equals(ENTITYGETTILE)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetTile(e);
			else
				fail("No such entity");
		}
		else if (cmd.equals(ENTITYGETROTATION)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetRotation(e);
			else
				fail("No such entity");
		}
		else if (cmd.equals(ENTITYSETROTATION)) {
			int id = scan.nextInt();
			float angle = scan.nextFloat();
			Entity e = serverWorld.getEntityByID(id);
			if (e != null) {
				e.rotationYaw = angle;
				e.setRotationYawHead(angle);
			}
			else
				fail("No such entity");
			e = mc.theWorld.getEntityByID(id);
			if (e != null) {
				e.rotationYaw = angle;
				e.setRotationYawHead(angle);
			}
		}
		else if (cmd.equals(ENTITYGETPITCH)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetPitch(e);
			else
				fail("No such entity");
		}
		else if (cmd.equals(ENTITYSETPITCH)) {
			int id = scan.nextInt();
			float angle = scan.nextFloat();
			Entity e = serverWorld.getEntityByID(id);
			if (e != null)
				e.rotationPitch = angle;
			else
				fail("No such entity");
			e = mc.theWorld.getEntityByID(id);
			if (e != null)
				e.rotationPitch = angle;
		}
		else if (cmd.equals(ENTITYGETDIRECTION)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetDirection(e);
			else
				fail("No such entity");
		}
		else if (cmd.equals(ENTITYSETDIRECTION)) {
			int id = scan.nextInt();
			double x  = scan.nextDouble();
			double y = scan.nextDouble();
			double z = scan.nextDouble();
			Entity e = serverWorld.getEntityByID(id);
			if (e != null)
				entitySetDirection(e, x, y, z);
			else
				fail("No such entity");
			e = mc.theWorld.getEntityByID(id);
			if (e != null)
				entitySetDirection(e, x, y, z);
		}
		else if (cmd.equals(ENTITYSETTILE)) {
			int id = scan.nextInt();
			Entity e = serverWorld.getEntityByID(id);
			float serverYaw = 0f;
			if (e != null) {
				serverYaw = e.rotationYaw;
				entitySetTile(e, scan);
				e.setRotationYawHead(serverYaw);
			}
			e = mc.theWorld.getEntityByID(id);
			if (e != null) {
				e.rotationYaw = serverYaw;
				e.setRotationYawHead(serverYaw);
			}
		}
		else if (cmd.equals(ENTITYSETPOS)) {
			int id = scan.nextInt();
			Entity e = serverWorld.getEntityByID(id);
			float serverYaw = 0f;
			if (e != null) {
				serverYaw = e.rotationYaw;
				entitySetPos(e, scan);
				e.setRotationYawHead(serverYaw);
			}
			e = mc.theWorld.getEntityByID(id);
			if (e != null) {
				e.rotationYaw = serverYaw;
				e.setRotationYawHead(serverYaw);
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
			if (setting.equals("world_immutable"))
				eventHandler.setStopChanges(scan.nextInt() != 0);
			// name_tags not supported
		}
		else if (cmd.equals(EVENTSSETTING)) {
			if (scan.next().equals("restrict_to_sword"))
				eventHandler.setRestrictToSword(scan.nextInt() != 0);
		}
		else if (cmd.equals(CAMERAGETENTITYID)) {
			EntityPlayerMP playerMP = getServerPlayer(clientPlayer);
			if (playerMP == null) {
				fail("Cannot find player");
			}
			else {
				sendLine(playerMP.getSpectatingEntity().getEntityId());
			}
		}
		else if (cmd.equals(CAMERASETFOLLOW) || cmd.equals(CAMERASETNORMAL)) {
			EntityPlayerMP playerMP = getServerPlayer(clientPlayer);
			boolean follow = cmd.equals(CAMERASETFOLLOW);

			if (playerMP != null) {
				if (! scan.hasNext()) {
					playerMP.setSpectatingEntity(null);
				}
				else {
					Entity entity = serverWorld.getEntityByID(scan.nextInt());
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

	private void entityGetRotation(Entity e) {
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

	private void entityGetPitch(Entity e) {
		sendLine(normalizeAngle(e.rotationPitch));
	}

	private void entityGetDirection(Entity e) {
		//sendLine(e.getLookVec());
		double pitch = e.rotationPitch * Math.PI / 180.;
		double yaw = e.rotationYaw * Math.PI / 180.;
		double x = Math.cos(-pitch) * Math.sin(-yaw);
		double z = Math.cos(-pitch) * Math.cos(-yaw);
		double y = Math.sin(-pitch);
		sendLine(new Vec3(x,y,z));
	}

	private void entitySetPos(Entity e, Scanner scan) {
		double x = scan.nextDouble();
		double y = scan.nextDouble();
		double z = scan.nextDouble();
		BlockPos spawnPos = serverWorld.getSpawnPoint();
		e.setPositionAndUpdate(x + spawnPos.getX(), 
				y + spawnPos.getY(),
				z + spawnPos.getZ());
	}

	private void entitySetTile(Entity e, Scanner scan) {
		BlockPos pos = getBlockPosition(scan);
		e.setPositionAndUpdate(pos.getX()+0.5, pos.getY(), (double)pos.getZ()+0.5);
	}
	
	private static int trunc(double x) {
		return (int)Math.floor(x);
	}

	private void entityGetTile(Entity e) {
		BlockPos spawn = serverWorld.getSpawnPoint();
		Vec3 spawnPoint = new Vec3(spawn.getX(), spawn.getY(), spawn.getZ());
		Vec3 pos = e.getPositionVector().subtract(spawnPoint);
		sendLine(""+trunc(pos.xCoord)+","+trunc(pos.yCoord)+","+trunc(pos.zCoord));
	}

	private void sendLine(BlockPos pos) {
		sendLine(""+pos.getX()+","+pos.getY()+","+pos.getZ());
	}

	private void entityGetPos(Entity e) {
		BlockPos spawn = serverWorld.getSpawnPoint();
		Vec3 spawnPoint = new Vec3(spawn.getX(), spawn.getY(), spawn.getZ());
		Vec3 pos = e.getPositionVector().subtract(spawnPoint);
		sendLine(pos);
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

	private BlockPos getBlockPosition(Scanner scan) {
		int x = scan.nextInt();
		int y = scan.nextInt();
		int z = scan.nextInt();
		return getBlockPosition(x, y, z);
	}

	private BlockPos getBlockPosition(int x, int y, int z) {
		BlockPos spawnPos = serverWorld.getSpawnPoint();
		return new BlockPos(x+spawnPos.getX(), y+spawnPos.getY(), z+spawnPos.getZ());
//		return serverWorld.getSpawnPoint().add(x,y,z);
	}

	EntityPlayerMP getServerPlayer(EntityPlayerSP playerSP) {
		return (EntityPlayerMP)serverWorld.getEntityByID(playerSP.getEntityId());
	}
}

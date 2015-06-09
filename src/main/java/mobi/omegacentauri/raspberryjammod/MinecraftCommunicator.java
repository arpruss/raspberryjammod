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

public class MinecraftCommunicator {
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

	final private ServerSocket socket;
	private World serverWorld;
	private MCEventHandler eventHandler;
	private boolean listening = true;
	private boolean translateBlockId = false; // default: do not translate blocks between Pi and Desktop
 	private Minecraft mc;
 	private int connectionsActive = 0;

	public MinecraftCommunicator(MCEventHandler eventHandler) throws IOException {
		this.eventHandler = eventHandler;
		socket = new ServerSocket(RaspberryJamMod.portNumber);
		initTypeMap();
	}

	void communicate() throws IOException {
		while(listening) {
			Socket connectionSocket = null;
			if (RaspberryJamMod.concurrentConnections == 1) {
				socketCommunicate(socket);
			}
			else if (connectionsActive < RaspberryJamMod.concurrentConnections) {
				new Thread(new Runnable(){

					@Override
					public void run() {
						socketCommunicate(socket);
					}}).start();
			}
			else {
				// Too many connections: sleep until one or more go away
				try {
					Thread.sleep(1000);
				}
				catch (Exception e) {}
			}
		}
	}

	private void socketCommunicate(ServerSocket serverSocket) {
		connectionsActive++;
		
		Socket connectionSocket = null;
		DataOutputStream writer = null;
		BufferedReader reader = null;
		
		try {
			connectionSocket = serverSocket.accept();
			
			String clientSentence;
			
			reader = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
			writer = new DataOutputStream(connectionSocket.getOutputStream());
	
			while(null != (clientSentence = reader.readLine())) {
				process(clientSentence, writer);
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
			connectionsActive--;
		}
	}

	synchronized private void process(String clientSentence, DataOutputStream writer) {
		Scanner scan = null;
		mc = Minecraft.getMinecraft();
		if (mc == null) {
			fail(writer, "Minecraft not available");
			return;
		}
		serverWorld = MinecraftServer.getServer().getEntityWorld();
		if (serverWorld == null) {
			fail(writer, "World not available");
			return;
		}
		EntityPlayerSP clientPlayer = mc.thePlayer;
		if (clientPlayer == null) {
			fail(writer, "Player not available");
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

			runCommand(writer, clientPlayer, cmd, args, scan);

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


	private void runCommand(DataOutputStream writer,
			EntityPlayerSP clientPlayer,
			String cmd, String args, Scanner scan) throws InputMismatchException, NoSuchElementException, 
			IndexOutOfBoundsException {
		
		if (cmd.equals(GETBLOCK)) {
			DesktopBlock b = new DesktopBlock(eventHandler.getBlockState(serverWorld, getPosition(scan)));

			sendLine(writer, b.toAPIBlock().id);
		}
		else if (cmd.equals(GETBLOCKWITHDATA)) {
			APIBlock b = new DesktopBlock(eventHandler.getBlockState(serverWorld, getPosition(scan))).toAPIBlock();
			sendLine(writer, ""+b.id+","+b.meta);
		}
		else if (cmd.equals(GETHEIGHT)) {
			BlockPos pos = getPosition(scan.nextInt(), 0, scan.nextInt());
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

			sendLine(writer, h);
		}
		else if (cmd.equals(SETBLOCK)) {
			BlockPos pos = getPosition(scan);
			int id = scan.nextInt();
			int meta = scan.hasNextInt() ? scan.nextInt() : 0;
			IBlockState state = new DesktopBlock(new APIBlock(id, meta)).getBlockState();
			eventHandler.queueSetBlockState(new BlockPos(pos), state);
		}
		else if (cmd.equals(SETBLOCKS)) {
			BlockPos pos1 = getPosition(scan);
			BlockPos pos2 = getPosition(scan);

			int id = scan.nextInt();
			int meta = scan.hasNextInt() ? scan.nextInt() : 0;
			IBlockState state = new DesktopBlock(new APIBlock(id, meta)).getBlockState();

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
						eventHandler.queueSetBlockState(new BlockPos(x,y,z), state);
					}
		}
		else if (cmd.equals(PLAYERGETPOS)) {
			entityGetPos(writer, clientPlayer);
		}
		else if (cmd.equals(PLAYERGETTILE)) {
			entityGetTile(writer, clientPlayer);
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
			sendLine(writer, ids);
		}
		else if (cmd.equals(WORLDGETPLAYERID)) {
			if (scan.hasNext()) {
				String name = scan.next();
				List<EntityPlayer> players = serverWorld.playerEntities;
				for (EntityPlayer p : players) {
					if (p.getName().equals(name)) {
						sendLine(writer, p.getEntityId());
						break;
					}
				}
				fail(writer, "Unknown player");
			}
			else {
				sendLine(writer, clientPlayer.getEntityId());
			}
		}
		else if (cmd.equals(PLAYERSETTILE)) {
			entitySetTile(clientPlayer, scan);
		}
		else if (cmd.equals(PLAYERSETPOS)) {
			entitySetPos(clientPlayer, scan);
		}
		else if (cmd.equals(PLAYERGETDIRECTION)) {
			entityGetDirection(writer, clientPlayer);
		}
		else if (cmd.equals(PLAYERGETROTATION)) {
			entityGetRotation(writer, clientPlayer);
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
					fail(writer, "Cannot parse tags");
					return;
				}
				tags.setString("id", entityId);
				entity = EntityList.createEntityFromNBT(tags, serverWorld);
			}
			else {
				entity = EntityList.createEntityByName(entityId, serverWorld);
			}
			
			if (entity == null) {
				fail(writer, "Cannot create entity");
			}
			else {
				entity.setPositionAndUpdate(x, y, z);
				serverWorld.spawnEntityInWorld(entity);
				sendLine(writer, entity.getEntityId());
			}
		}
		else if (cmd.equals(PLAYERSETDIRECTION)) {
			double x = scan.nextDouble();
			double y = scan.nextDouble();
			double z = scan.nextDouble();
			entitySetDirection(clientPlayer, x, y, z);
		}
		else if (cmd.equals(PLAYERGETPITCH)) {
			entityGetPitch(writer, clientPlayer);
		}
		else if (cmd.equals(ENTITYGETPOS)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetPos(writer, e);
			else
				fail(writer, "No such entity");
		}
		else if (cmd.equals(ENTITYGETTILE)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetTile(writer, e);
			else
				fail(writer, "No such entity");
		}
		else if (cmd.equals(ENTITYGETROTATION)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetRotation(writer, e);
			else
				fail(writer, "No such entity");
		}
		else if (cmd.equals(ENTITYSETROTATION)) {
			int id = scan.nextInt();
			float angle = scan.nextFloat();
			Entity e = serverWorld.getEntityByID(id);
			if (e != null) {
//				System.out.println("server "+e.rotationYaw);
				e.rotationYaw = angle;
				e.setRotationYawHead(angle);
//				e.setLocationAndAngles(e.getPosition().getX(), e.getPosition().getY(), e.getPosition().getZ(), angle, e.rotationPitch);
			}
			else
				fail(writer, "No such entity");
			e = mc.theWorld.getEntityByID(id);
			if (e != null) {
//				System.out.println("client "+e.rotationYaw);
				e.rotationYaw = angle;
				e.setRotationYawHead(angle);
//				e.setLocationAndAngles(e.getPosition().getX(), e.getPosition().getY(), e.getPosition().getZ(), angle, e.rotationPitch);
			}
		}
		else if (cmd.equals(ENTITYGETPITCH)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetPitch(writer, e);
			else
				fail(writer, "No such entity");
		}
		else if (cmd.equals(ENTITYSETPITCH)) {
			int id = scan.nextInt();
			float angle = scan.nextFloat();
			Entity e = serverWorld.getEntityByID(id);
			if (e != null)
				e.rotationPitch = angle;
			else
				fail(writer, "No such entity");
			e = mc.theWorld.getEntityByID(id);
			if (e != null)
				e.rotationPitch = angle;
		}
		else if (cmd.equals(ENTITYGETDIRECTION)) {
			Entity e = serverWorld.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetDirection(writer, e);
			else
				fail(writer, "No such entity");
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
				fail(writer, "No such entity");
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
			sendLine(writer, eventHandler.getHitsAndClear());
		}
		else if (cmd.equals(EVENTSCHATPOSTS)) {
			sendLine(writer, eventHandler.getChatsAndClear());
		}
		else if (cmd.equals(WORLDSETTING)) {
			String setting = scan.next();
			if (setting.equals("world_immutable"))
				eventHandler.setStopChanges(scan.nextInt() != 0);
			else if (setting.equals("translate_blocks"))
				translateBlockId = scan.nextInt() != 0;
			// name_tags not supported
		}
		else if (cmd.equals(EVENTSSETTING)) {
			if (scan.next().equals("restrict_to_sword"))
				eventHandler.setRestrictToSword(scan.nextInt() != 0);
		}
		else if (cmd.equals(CAMERAGETENTITYID)) {
			EntityPlayerMP playerMP = getServerPlayer(clientPlayer);
			if (playerMP == null) {
				fail(writer, "Cannot find player");
			}
			else {
				sendLine(writer, playerMP.getSpectatingEntity().getEntityId());
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

	private void fail(DataOutputStream writer, String string) {
		System.err.println("Error: "+string);
		sendLine(writer, "Fail");
	}

	private void entityGetRotation(DataOutputStream writer, Entity e) {
		sendLine(writer, normalizeAngle(e.rotationYaw));
	}

	private float normalizeAngle(float angle) {
		angle = angle % 360;
		if (angle <= -180)
			angle += 360;
		if (angle > 180)
			angle -= 360;
		return angle;
	}

	private void entityGetPitch(DataOutputStream writer, Entity e) {
		sendLine(writer, normalizeAngle(e.rotationPitch));
	}

	private void entityGetDirection(DataOutputStream writer, Entity e) {
		//sendLine(e.getLookVec());
		double pitch = e.rotationPitch * Math.PI / 180.;
		double yaw = e.rotationYaw * Math.PI / 180.;
		double x = Math.cos(-pitch) * Math.sin(-yaw);
		double z = Math.cos(-pitch) * Math.cos(-yaw);
		double y = Math.sin(-pitch);
		sendLine(writer, new Vec3(x,y,z));
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
		BlockPos pos = getPosition(scan);
		e.setPositionAndUpdate((double)pos.getX(), (double)pos.getY(), (double)pos.getZ());
	}

	private void entityGetTile(DataOutputStream writer, Entity e) {
		BlockPos spawn = serverWorld.getSpawnPoint();
		Vec3i spawnPoint = new Vec3i(spawn.getX(), spawn.getY(), spawn.getZ());
		BlockPos pos = e.getPosition().subtract(spawnPoint);

		sendLine(writer, pos);
	}

	private void sendLine(DataOutputStream writer, BlockPos pos) {
		sendLine(writer, ""+pos.getX()+","+pos.getY()+","+pos.getZ());
	}

	private void entityGetPos(DataOutputStream writer, Entity e) {
		BlockPos spawn = serverWorld.getSpawnPoint();
		Vec3 spawnPoint = new Vec3(spawn.getX(), spawn.getY(), spawn.getZ());
		Vec3 pos = e.getPositionVector().subtract(spawnPoint);
		sendLine(writer, pos);
	}

	private void sendLine(DataOutputStream writer, double x) {
		sendLine(writer, Double.toString(x));
	}

	private void sendLine(DataOutputStream writer, int x) {
		sendLine(writer, Integer.toString(x));
	}

	private void sendLine(DataOutputStream writer, Vec3 v) {
		sendLine(writer, ""+v.xCoord+","+v.yCoord+","+v.zCoord);
	}

	private void sendLine(DataOutputStream writer, String string) {
		try {
			writer.writeBytes(string+"\n");
			writer.flush();
		}
		catch(Exception e) {					
		}
	}

	private BlockPos getPosition(Scanner scan) {
		int x = scan.nextInt();
		int y = scan.nextInt();
		int z = scan.nextInt();
		return getPosition(x, y, z);
	}

	private BlockPos getPosition(int x, int y, int z) {
		return serverWorld.getSpawnPoint().add(x,y,z);
	}

	public void close() {
		
		listening = false;
		try {
			if (socket != null)
				socket.close();
		} catch (IOException e) {
		}
	}

	private void initTypeMap() {
		typeMap = new Block[256];
		typeMap[0] = Blocks.air;
		typeMap[1] = Blocks.stone;
		typeMap[2] = Blocks.grass;
		typeMap[3] = Blocks.dirt;
		typeMap[4] = Blocks.cobblestone;
		typeMap[5] = Blocks.planks; // wooden plank
		typeMap[6] = Blocks.sapling;
		typeMap[7] = Blocks.bedrock;
		typeMap[8] = Blocks.flowing_water;
		typeMap[9] = Blocks.water;
		typeMap[10] = Blocks.flowing_lava;
		typeMap[11] = Blocks.lava;
		typeMap[12] = Blocks.sand;
		typeMap[13] = Blocks.gravel;
		typeMap[14] = Blocks.gold_ore;
		typeMap[15] = Blocks.iron_ore;
		typeMap[16] = Blocks.coal_ore;
		typeMap[17] = Blocks.log; // wood
		typeMap[18] = Blocks.leaves;
		typeMap[19] = Blocks.sponge;
		typeMap[20] = Blocks.glass;
		typeMap[21] = Blocks.lapis_ore;
		typeMap[22] = Blocks.lapis_block;
		typeMap[24] = Blocks.sandstone;
		typeMap[26] = Blocks.bed;
		typeMap[27] = Blocks.golden_rail;
		typeMap[30] = Blocks.web;
		typeMap[31] = Blocks.tallgrass;
		typeMap[32] = Blocks.deadbush;
		typeMap[35] = Blocks.wool;
		typeMap[37] = Blocks.yellow_flower; 
		typeMap[38] = Blocks.red_flower;
		typeMap[39] = Blocks.brown_mushroom;
		typeMap[40] = Blocks.red_mushroom;
		typeMap[41] = Blocks.gold_block;
		typeMap[42] = Blocks.iron_block;
		typeMap[43] = Blocks.stone_slab2;
		typeMap[44] = Blocks.stone_slab;
		typeMap[45] = Blocks.brick_block;
		typeMap[46] = Blocks.tnt;
		typeMap[47] = Blocks.bookshelf;
		typeMap[48] = Blocks.mossy_cobblestone;
		typeMap[49] = Blocks.obsidian;
		typeMap[50] = Blocks.torch;
		typeMap[51] = Blocks.fire;
		typeMap[52] = Blocks.mob_spawner;
		typeMap[53] = Blocks.oak_stairs;
		typeMap[54] = Blocks.chest;
		typeMap[56] = Blocks.diamond_ore;
		typeMap[57] = Blocks.diamond_block;
		typeMap[58] = Blocks.crafting_table;
		typeMap[59] = Blocks.wheat; // seeds
		typeMap[60] = Blocks.farmland;
		typeMap[61] = Blocks.furnace;
		typeMap[62] = Blocks.lit_furnace; 
		typeMap[63] = Blocks.standing_sign; 
		typeMap[64] = Blocks.oak_door;
		typeMap[65] = Blocks.ladder;
		typeMap[66] = Blocks.rail;
		typeMap[67] = Blocks.stone_stairs; // cobblestone stairs
		typeMap[68] = Blocks.wall_sign;
		typeMap[71] = Blocks.iron_door;
		typeMap[73] = Blocks.redstone_ore;
		typeMap[74] = Blocks.lit_redstone_ore; // glowing redstone ore
		typeMap[78] = Blocks.snow_layer;
		typeMap[79] = Blocks.ice;
		typeMap[80] = Blocks.snow;
		typeMap[81] = Blocks.cactus;
		typeMap[82] = Blocks.clay;
		typeMap[83] = Blocks.reeds; // sugar cane
		typeMap[85] = Blocks.oak_fence;
		typeMap[86] = Blocks.pumpkin;
		typeMap[87] = Blocks.netherrack;
		typeMap[89] = Blocks.glowstone;
		typeMap[91] = Blocks.lit_pumpkin;
		typeMap[92] = Blocks.cake;
		typeMap[95] = UNKNOWN_BLOCK; // invisible bedrock
		typeMap[96] = Blocks.trapdoor;
		typeMap[98] = Blocks.stonebrick;
		typeMap[99] = Blocks.brown_mushroom; // huge brown mushroom
		typeMap[100] = Blocks.red_mushroom; // huge red mushroom
		typeMap[101] = Blocks.iron_bars;
		typeMap[102] = Blocks.glass_pane;
		typeMap[103] = Blocks.melon_block;
		typeMap[104] = Blocks.pumpkin_stem;
		typeMap[105] = Blocks.melon_stem;
		typeMap[106] = Blocks.vine;
		typeMap[107] = Blocks.oak_fence_gate;
		typeMap[108] = Blocks.brick_stairs;
		typeMap[109] = Blocks.stone_brick_stairs;
		typeMap[110] = Blocks.mycelium;
		typeMap[111] = Blocks.waterlily;
		typeMap[112] = Blocks.nether_brick;
		typeMap[114] = Blocks.nether_brick_stairs;
		typeMap[120] = Blocks.end_portal_frame;
		typeMap[121] = Blocks.end_stone;
		typeMap[127] = Blocks.cocoa;
		typeMap[128] = Blocks.sandstone_stairs;
		typeMap[129] = Blocks.emerald_ore;
		typeMap[133] = Blocks.emerald_block;
		typeMap[134] = Blocks.spruce_stairs;
		typeMap[135] = Blocks.birch_stairs;
		typeMap[136] = Blocks.jungle_stairs;
		typeMap[139] = Blocks.cobblestone_wall;
		typeMap[141] = Blocks.carrots;
		typeMap[142] = Blocks.potatoes;
		typeMap[155] = Blocks.quartz_block;
		typeMap[156] = Blocks.quartz_stairs;
		typeMap[157] = Blocks.double_wooden_slab; 
		typeMap[158] = Blocks.wooden_slab;
		typeMap[159] = Blocks.stained_hardened_clay;
		typeMap[163] = Blocks.acacia_stairs;
		typeMap[164] = Blocks.dark_oak_stairs;
		typeMap[170] = Blocks.hay_block;
		typeMap[171] = Blocks.carpet;
		typeMap[172] = Blocks.hardened_clay;
		typeMap[173] = Blocks.coal_block;
		typeMap[174] = Blocks.packed_ice;
		typeMap[243] = UNKNOWN_BLOCK; // podzol
		typeMap[244] = UNKNOWN_BLOCK; // beet root
		typeMap[245] = UNKNOWN_BLOCK; // stone cutter
		typeMap[246] = Blocks.obsidian; // glowing obsidian
		typeMap[247] = UNKNOWN_BLOCK; // nether reactor core
		typeMap[248] = UNKNOWN_BLOCK; // update game block
		typeMap[249] = UNKNOWN_BLOCK; // update game block		
	}

	/*
	public Block getBlockByRaspberryId(int id) {
		if (! translateBlockId)
			return Block.getBlockById(id);
		Block b = null;
		if (id < typeMap.length)
			b = typeMap[id];

		if (b == null)
			return UNKNOWN_BLOCK;
		else
			return b;
	}

	public int getRaspberryBlockId(Block b) {
		if (! translateBlockId)
			return Block.getIdFromBlock(b);
		for (int i=0; i<typeMap.length; i++) 
			if (typeMap[i] == b)
				return i;
		return 95; // UNKNOWN : invisible bedrock ?!
	} */

	class APIBlock
	{
		private int id;
		private int meta;

		public APIBlock(int id, int meta) {
			this.id = id;
			this.meta = meta;
		}
	}

	class DesktopBlock
	{
		private Block block;
		private int meta;

		public DesktopBlock(Block block, int meta) {
			this.block = block;
			this.meta = meta;
		}

		public IBlockState getBlockState() {
			return block.getStateFromMeta(meta);
		}

		public DesktopBlock(APIBlock apiBlock) {
			if (!MinecraftCommunicator.this.translateBlockId) {
				this.block = Block.getBlockById(apiBlock.id);
				if (this.block == null)
					this.block = UNKNOWN_BLOCK;
				this.meta = apiBlock.meta; 
				return;
			}

			this.block = null;
			if (apiBlock.id < typeMap.length)
				this.block = typeMap[apiBlock.id];

			if (this.block == null)
				this.block = UNKNOWN_BLOCK;

			this.meta = apiBlock.meta; // todo: translate meta
		}

		public DesktopBlock(IBlockState blockState) {
			this.block = blockState.getBlock();
			this.meta = this.block.getMetaFromState(blockState);
		}

		public APIBlock toAPIBlock() {
			if (!MinecraftCommunicator.this.translateBlockId)
				return new APIBlock(Block.getIdFromBlock(block), meta);

			for (int i=0; i<typeMap.length; i++) 
				if (typeMap[i] == block)
					return new APIBlock(i, meta); // todo: translate meta

			return new APIBlock(95, meta);
		}
	}

	EntityPlayerMP getServerPlayer(EntityPlayerSP playerSP) {
		return (EntityPlayerMP)serverWorld.getEntityByID(playerSP.getEntityId());
	}
}

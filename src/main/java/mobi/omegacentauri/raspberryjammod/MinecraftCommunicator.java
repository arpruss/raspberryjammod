package mobi.omegacentauri.raspberryjammod;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
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
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.Blocks;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.BlockPos;
import net.minecraft.util.IChatComponent;
import net.minecraft.util.Vec3;
import net.minecraft.util.Vec3i;
import net.minecraft.world.World;
import net.minecraft.world.chunk.Chunk;

public class MinecraftCommunicator {
	// world.checkpoint.save/restore, player.setting, world.setting(nametags_visible,*),
	// camera.* unsupported
	private static final String CHAT = "chat.post";
	public static final String SETBLOCK = "world.setBlock";
	public static final String SETBLOCKS = "world.setBlocks"; 
	private static final String GETBLOCK = "world.getBlock";
	private static final String GETBLOCKWITHDATA = "world.getBlockWithData";
	private static final String GETHEIGHT = "world.getHeight"; 
	private static final String GETPLAYERIDS = "world.getPlayerIds"; 
	private static final String GETPLAYERENTITYID = "world.getPlayerEntityId"; 
	private static final String PLAYERSETTILE = "player.setTile"; 
	private static final String PLAYERSETPOS = "player.setPos"; 
	private static final String PLAYERGETDIRECTION = "player.getDirection"; 
	private static final String PLAYERGETROTATION = "player.getRotation"; 
	private static final String PLAYERGETPITCH = "player.getPitch";
	private static final String PLAYERGETPOS = "player.getPos";
	private static final String PLAYERGETTILE = "player.getTile";	
	private static final String ENTITYGETDIRECTION = "entity.getDirection"; 
	private static final String ENTITYGETROTATION = "entity.getRotation"; 
	private static final String ENTITYGETPITCH = "entity.getPitch"; 
	private static final String ENTITYGETPOS = "entity.getPos"; 
	private static final String ENTITYGETTILE = "entity.getTile"; 
	private static final String ENTITYSETTILE = "entity.setTile"; 
	private static final String ENTITYSETPOS = "entity.setPos"; 
	private static final String WORLDSETTING = "world.setting";

	private static final String EVENTSBLOCKHITS = "events.block.hits";
	private static final String EVENTSCLEAR = "events.clear";
	private static final String EVENTSSETTING = "events.setting";
	
	private static final Block UNKNOWN_BLOCK = Blocks.beacon;
	Block[] typeMap;

	private ServerSocket socket;
	private DataOutputStream writer;
	private World world;
	private MCEventHandler eventHandler;
	private boolean listening = true;
	private boolean translateBlockId = true;

	public MinecraftCommunicator(MCEventHandler eventHandler) throws IOException {
		this.eventHandler = eventHandler;
		socket = new ServerSocket(4711);
		initTypeMap();
	}

	void communicate() throws IOException {
		String clientSentence;

		while(listening) {
			Socket connectionSocket = null;

			try {
				connectionSocket = socket.accept();
				BufferedReader reader =
						new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
				writer = new DataOutputStream(connectionSocket.getOutputStream());

				while(null != (clientSentence = reader.readLine())) {
					Scanner scan = null;
					Minecraft mc = Minecraft.getMinecraft();
					if (mc == null) {
						sendLine("Error: minecraft not available");
						continue;
					}
					world = MinecraftServer.getServer().getEntityWorld();
					if (world == null) {
						sendLine("Error: world not available");
						continue;
					}
					EntityPlayerSP player = mc.thePlayer;
					if (player == null) {
						sendLine("Error: player not available");
						continue;
					}
					process(mc, player, clientSentence);
				}
			}
			catch (Exception e) {
				System.out.println(""+e);
				try {
					Thread.sleep(1000);
				}
				catch(Exception e2) {					
				}
			}
			finally {
				if (connectionSocket != null)
					connectionSocket.close();
			}
		}
	}

	private void process(Minecraft mc, EntityPlayerSP player,
			String clientSentence) {
		Scanner scan = null;

		try {	
			int paren = clientSentence.indexOf('(');
			if (paren < 0)
				return;
			String cmd = clientSentence.substring(0, paren);
			String args = clientSentence.substring(paren + 1).replaceAll("[\r\n)]+$", "");

			scan = new Scanner(args);
			scan.useDelimiter(",");
			
			runCommand(mc, player, cmd, args, scan);
			
			scan.close();
			scan = null;
		}
		catch(InputMismatchException e) {
			System.out.println(""+e);
		}
		catch (NoSuchElementException e) {
			System.out.println(""+e);
		}
		finally {
			if (scan != null)
				scan.close();
		}
	}


	private void runCommand(Minecraft mc, EntityPlayerSP player,
			String cmd, String args, Scanner scan) throws InputMismatchException, NoSuchElementException, 
			IndexOutOfBoundsException {
		if (cmd.equals(GETBLOCK)) {
			Block block = world.getBlockState(getPosition(scan)).getBlock();
			int id = getRaspberryBlockId(block);
			sendLine(id);
		}
		else if (cmd.equals(GETBLOCKWITHDATA)) {
			IBlockState state = world.getBlockState(getPosition(scan));
			Block block = state.getBlock();
			int id = getRaspberryBlockId(block);
			sendLine(""+id+","+block.getMetaFromState(state));
		}
		else if (cmd.equals(GETHEIGHT)) {
			BlockPos pos = getPosition(scan.nextInt(), 0, scan.nextInt());
			Chunk chunk = world.getChunkFromBlockCoords(pos);
			int h = chunk.getHeight(pos);
			int x = pos.getX();
			int z = pos.getZ();
			for (int y = world.getHeight() ; y >= h ; y--) {
				Block b = chunk.getBlock(x,y,z);
				if (b != Blocks.air) {
					h = y;
					break;
				}
			}

			h -= world.getSpawnPoint().getY();
			
			sendLine(h);
		}
		else if (cmd.equals(SETBLOCK)) {
			BlockPos pos = getPosition(scan);
			int type = scan.nextInt();

			Block b = getBlockByRaspberryId(type);
			IBlockState s = scan.hasNextInt() ? b.getStateFromMeta(scan.nextInt()) : b.getDefaultState();
			eventHandler.queueSetBlockState(pos, s);
//			world.setBlockState(pos, s, 2); 
			//			mc.theWorld.markBlocksDirtyVertical(pos.getX(), pos.getZ(), pos.getX(), pos.getZ());
		
			//world.checkLight(pos);

			//		        if (!world.isRemote)
			//		        {
			//		            world.markBlockForUpdate(pos);
			//		        }
		}
		else if (cmd.equals(SETBLOCKS)) {
			BlockPos pos1 = getPosition(scan);
			BlockPos pos2 = getPosition(scan);
			int type = scan.nextInt();

			Block b = getBlockByRaspberryId(type);
			IBlockState state;
			
			if (scan.hasNextInt()) {
				state = b.getStateFromMeta(scan.nextInt());
			}
			else {
				state = b.getDefaultState();
			}
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
			entityGetPos(player);
		}
		else if (cmd.equals(PLAYERGETTILE)) {
			entityGetTile(player);
		}
		else if (cmd.equals(CHAT)) {
			player.sendChatMessage(args);
		}
		else if (cmd.equals(GETPLAYERIDS)) {
			List<EntityPlayer> players = world.playerEntities;
			String ids = "";
			for (EntityPlayer p : players) {
				if (ids.length() > 0)
					ids += "|";
				ids += p.getEntityId();
			}
			sendLine(ids);
		}
		else if (cmd.equals(GETPLAYERENTITYID)) {
			sendLine(player.getEntityId());
		}
		else if (cmd.equals(PLAYERSETTILE)) {
			entitySetTile(player, scan);
		}
		else if (cmd.equals(PLAYERSETPOS)) {
			entitySetPos(player, scan);
		}
		else if (cmd.equals(PLAYERGETDIRECTION)) {
			entityGetDirection(player);
		}
		else if (cmd.equals(PLAYERGETROTATION)) {
			entityGetRotation(player);
		}
		else if (cmd.equals(PLAYERGETPITCH)) {
			entityGetPitch(player);
		}
		else if (cmd.equals(ENTITYGETPOS)) {
			Entity e = world.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetPos(e);
			else
				sendLine("Error: No such entity");
		}
		else if (cmd.equals(ENTITYGETTILE)) {
			Entity e = world.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetTile(e);
			else
				sendLine("Error: No such entity");
		}
		else if (cmd.equals(ENTITYGETROTATION)) {
			Entity e = world.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetRotation(e);
			else
				sendLine("Error: No such entity");
		}
		else if (cmd.equals(ENTITYGETPITCH)) {
			Entity e = world.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetPitch(e);
			else
				sendLine("Error: No such entity");
		}
		else if (cmd.equals(ENTITYGETDIRECTION)) {
			Entity e = world.getEntityByID(scan.nextInt());
			if (e != null)
				entityGetDirection(e);
			else
				sendLine("Error: No such entity");
		}
		else if (cmd.equals(ENTITYSETTILE)) {
			Entity e = world.getEntityByID(scan.nextInt());
			if (e != null)
				entitySetTile(e, scan);
			
		}
		else if (cmd.equals(ENTITYSETPOS)) {
			Entity e = world.getEntityByID(scan.nextInt());
			if (e != null)
				entitySetPos(e, scan);
		}
		else if (cmd.equals(EVENTSCLEAR)) {
			eventHandler.clearHits();
		}
		else if (cmd.equals(EVENTSBLOCKHITS)) {
			sendLine(eventHandler.getHitsAndClear());
		}
		else if (cmd.equals(WORLDSETTING)) {
			if (scan.next().equals("world_immutable"))
				eventHandler.setStopChanges(scan.nextInt() != 0);
			else if (scan.next().equals("translate_blocks"))
				translateBlockId = scan.nextInt() != 0;
			// name_tags not supported
		}
		else if (cmd.equals(EVENTSSETTING)) {
			if (scan.next().equals("restrict_to_sword"))
				eventHandler.setRestrictToSword(scan.nextInt() != 0);
		}
	}

	private void entityGetPitch(Entity e) {
		Vec3 look = e.getLookVec();
		Double xz = Math.sqrt(look.xCoord * look.xCoord + look.zCoord * look.zCoord);
		sendLine(Math.atan2(look.yCoord, xz) * 180. / Math.PI);
	}

	private void entityGetRotation(Entity e) {
		Vec3 look = e.getLookVec();
		if (Math.abs(look.xCoord) < 1e-10 && Math.abs(look.yCoord) < 1e-10) {
			sendLine(0);
		}
		else {
			Double angle = (Math.atan2(look.zCoord, look.xCoord) + Math.PI) * 180. / Math.PI;
			sendLine(angle);
		}
	}

	private void entityGetDirection(Entity e) {
		sendLine(e.getLookVec());
	}

	private void entitySetPos(Entity e, Scanner scan) {
		double x = scan.nextDouble();
		double y = scan.nextDouble();
		double z = scan.nextDouble();
		BlockPos spawnPos = world.getSpawnPoint();
		e.setPositionAndUpdate(x + spawnPos.getX(), 
				y + spawnPos.getY(),
				z + spawnPos.getZ());
	}

	private void entitySetTile(Entity e, Scanner scan) {
		BlockPos pos = getPosition(scan);
		e.setPositionAndUpdate((double)pos.getX(), (double)pos.getY(), (double)pos.getZ());
	}

	private void entityGetTile(Entity e) {
		BlockPos spawn = world.getSpawnPoint();
		Vec3i spawnPoint = new Vec3i(spawn.getX(), spawn.getY(), spawn.getZ());
		BlockPos pos = e.getPosition().subtract(spawnPoint);

		sendLine(pos);
	}

	private void sendLine(BlockPos pos) {
		sendLine(""+pos.getX()+","+pos.getY()+","+pos.getZ());
	}

	private void entityGetPos(Entity e) {
		BlockPos spawn = world.getSpawnPoint();
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

	private BlockPos getPosition(Scanner scan) {
		int x = scan.nextInt();
		int y = scan.nextInt();
		int z = scan.nextInt();
		return getPosition(x, y, z);
	}

	private BlockPos getPosition(int x, int y, int z) {
		return world.getSpawnPoint().add(x,y,z);
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
		return 83; // UNKNOWN : sugar cane ?!
	}
}

package mobi.omegacentauri.raspberryjammod;

import java.beans.EventSetDescriptor;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.UUID;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.gui.GuiChat;
import net.minecraft.client.gui.GuiScreen;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
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
import net.minecraft.util.Vec3i;
import net.minecraft.world.EnumDifficulty;
import net.minecraft.world.World;
import net.minecraftforge.client.event.MouseEvent;
import net.minecraftforge.event.CommandEvent;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.event.terraingen.InitMapGenEvent;
import net.minecraftforge.fml.common.FMLCommonHandler;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.InputEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.relauncher.Side;

abstract public class MCEventHandler {
	protected List<ServerAction> serverActionQueue = new ArrayList<ServerAction>();		
	private List<HitDescription> hits = new LinkedList<HitDescription>();
	protected List<ChatDescription> chats = new LinkedList<ChatDescription>();
	private static final int MAX_HITS = 512;
	private volatile boolean stopChanges = false;
	private volatile boolean restrictToSword = true;
	protected volatile boolean pause = false;
	private ServerChatEvent chatEvents;
	protected static final int MAX_CHATS = 512;
	protected boolean doRemote;

	public void setStopChanges(boolean stopChanges) {
		this.stopChanges = stopChanges;
	}
	
//	@SubscribeEvent
//	public void onInitMapGenEvent(InitMapGenEvent event) {
//		System.out.println("Init map gen");
//		MinecraftServer.getServer().setDifficultyForAllWorlds(EnumDifficulty.PEACEFUL);
//	}
	
//	@SubscribeEvent
//    public void onKeyInput(InputEvent.KeyInputEvent event) {
//        if(KeyBindings.superchat.isPressed()) {
//            System.out.println("superchat");
//            Minecraft.getMinecraft().displayGuiScreen(new MyChat());
//        }
//    }
	
	@SubscribeEvent
	public void onPlayerInteractEvent(PlayerInteractEvent event) {
		if (event.entityPlayer == null || event.entityPlayer.getEntityWorld().isRemote != RaspberryJamMod.clientOnlyAPI )
			return;
		
		if (event.action == PlayerInteractEvent.Action.RIGHT_CLICK_BLOCK ||
			(RaspberryJamMod.leftClickToo && event.action == PlayerInteractEvent.Action.LEFT_CLICK_BLOCK)) {
			if (! restrictToSword || holdingSword(event.entityPlayer)) {
				synchronized(hits) {
					if (hits.size() >= MAX_HITS)
						hits.remove(0);
					hits.add(new HitDescription(getWorlds(),event));
				}
			}
		}
		if (stopChanges) {
			event.setCanceled(true);
		}
	}
	
	abstract protected World[] getWorlds();

	private boolean holdingSword(EntityPlayer player) {
		ItemStack item = player.getHeldItem();
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
				out.append(c.message.replace("|", "&#124;"));
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
	
	public void clearAll() {
		hits.clear();
		chats.clear();
	}
	
	public void queueServerAction(ServerAction s) {
		synchronized(serverActionQueue) {
			serverActionQueue.add(s);
		}
	}
	
	public void runQueue() {
		if (!pause) {
			synchronized(serverActionQueue) {
				for (ServerAction entry: serverActionQueue) {
					if (! RaspberryJamMod.serverActive)
						break;
					entry.execute();
				}
				serverActionQueue.clear();
			}
		}
		else if (! RaspberryJamMod.serverActive) {
			synchronized(serverActionQueue) {
				serverActionQueue.clear();
			}
		}
	}

	public BlockState getBlockState(Location pos) {
		int x = pos.getX();
		int y = pos.getY();
		int z = pos.getZ();
	
		synchronized(serverActionQueue) {
			for (int i = serverActionQueue.size() - 1 ; i >= 0 ; i--) {
				ServerAction entry = serverActionQueue.get(i);
				if (entry.contains(pos.world,x,y,z)) {
					return entry.getBlockState();
				}
			}
		}
		
		return new BlockState(pos.world.getBlockState(pos));
	}

	public String describeBlockState(Location pos) {
		int x = pos.getX();
		int y = pos.getY();
		int z = pos.getZ();
	
		synchronized(serverActionQueue) {
			for (int i = serverActionQueue.size() - 1 ; i >= 0 ; i--) {
				ServerAction entry = serverActionQueue.get(i);
				if (entry.contains(pos.world,x,y,z)) {
					return entry.describe();
				}
			}
		}

		IBlockState state = pos.world.getBlockState(pos);
		Block block = state.getBlock();
		int meta = block.getMetaFromState(state);
		String describe = ""+block.getIdFromBlock(block)+","+meta+",";

		TileEntity tileEntity = pos.world.getTileEntity(pos);
		if (tileEntity == null)
			return describe;
		NBTTagCompound tag = new NBTTagCompound();
		tileEntity.writeToNBT(tag);
		SetBlockNBT.scrubNBT(tag);
		return describe+tag.toString();
	}

	public int getBlockId(Location pos) {
		int x = pos.getX();
		int y = pos.getY();
		int z = pos.getZ();
	
		synchronized(serverActionQueue) {
			for (int i = serverActionQueue.size() - 1 ; i >= 0 ; i--) {
				ServerAction entry = serverActionQueue.get(i);
				if (entry.contains(pos.world, x,y,z)) {
					return (int)entry.getBlockId();
				}
			}
		}
		
		return Block.getIdFromBlock(pos.world.getBlockState(pos).getBlock());
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


	public void setPause(boolean b) {
		pause = b;
	}
}

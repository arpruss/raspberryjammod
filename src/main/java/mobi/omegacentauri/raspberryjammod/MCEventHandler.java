package mobi.omegacentauri.raspberryjammod;

import java.beans.EventSetDescriptor;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.gui.GuiChat;
import net.minecraft.client.gui.GuiScreen;
import net.minecraft.event.ClickEvent;
import net.minecraft.item.ItemStack;
import net.minecraft.item.ItemSword;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.BlockPos;
import net.minecraft.util.EnumFacing;
import net.minecraft.util.IChatComponent;
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

public class MCEventHandler {
	List<SetBlockState> setBlockStateQueue = new ArrayList<SetBlockState>();		
	List<HitDescription> hits = new LinkedList<HitDescription>();
	List<ChatDescription> chats = new LinkedList<ChatDescription>();
	static final int MAX_HITS = 512;
	private boolean stopChanges = false;
	private boolean restrictToSword = true;
	ServerChatEvent chatEvents;
	static final int MAX_CHATS = 512;

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
	public void onChatEvent(ServerChatEvent event) {
		ChatDescription cd = new ChatDescription(event.player.getEntityId(), event.message);
		synchronized(chats) {
			if (chats.size() >= MAX_CHATS)
				chats.remove(0);
			chats.add(cd);
		}
	}

	@SubscribeEvent
	public void onPlayerInteractEvent(PlayerInteractEvent event) {
		if (event.action == PlayerInteractEvent.Action.RIGHT_CLICK_BLOCK ||
			(RaspberryJamMod.leftClickToo && event.action == PlayerInteractEvent.Action.LEFT_CLICK_BLOCK)) {
			if (! restrictToSword || holdingSword()) {
				synchronized(hits) {
					if (hits.size() >= MAX_HITS)
						hits.remove(0);
					hits.add(new HitDescription(event));
				}
			}
		}
		if (stopChanges) {
			event.setCanceled(true);
		}
	}

	private boolean holdingSword() {
		ItemStack item = Minecraft.getMinecraft().thePlayer.getHeldItem();
		if (item != null) {
			return item.getItem() instanceof ItemSword;
//			String name = item.getUnlocalizedName();
//			if (name != null)
//				return name.contains("item.sword");
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

	@SubscribeEvent
	public void onServerTick(TickEvent.ServerTickEvent event) {
		World world = MinecraftServer.getServer().getEntityWorld();
		synchronized(setBlockStateQueue) {
			for (SetBlockState entry: setBlockStateQueue) {
				if (world.getTileEntity(entry.pos) != null) {
				}
				world.setBlockState(entry.pos, entry.state, 2);
				world.markBlockForUpdate(entry.pos);
			}
			setBlockStateQueue.clear();
		}
	}

	public void queueSetBlockState(BlockPos pos, IBlockState s) {
		synchronized(setBlockStateQueue) {
			setBlockStateQueue.add(new SetBlockState(pos, s));
		}
	}

	class SetBlockState {
		BlockPos pos;
		IBlockState state;

		public SetBlockState(BlockPos pos, IBlockState s) {
			this.pos = pos;
			this.state = s;
		}
	}

	class HitDescription {
		private String description;
		
		public HitDescription(PlayerInteractEvent event) {
			BlockPos pos = event.pos.subtract(MinecraftServer.getServer().getEntityWorld().getSpawnPoint());
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

	public IBlockState getBlockState(World world, BlockPos pos) {
		int x = pos.getX();
		int y = pos.getY();
		int z = pos.getZ();
	
		synchronized(setBlockStateQueue) {
			for (int i = setBlockStateQueue.size() - 1 ; i >= 0 ; i--) {
				SetBlockState entry = setBlockStateQueue.get(i);
				BlockPos qPos = entry.pos;
				if (qPos.getX() == x && qPos.getZ() == z && qPos.getY() == y) {
					return entry.state;
				}
			}
		}
		
		return world.getBlockState(pos);
	}

	class ChatDescription {
		int id;
		String message;
		public ChatDescription(int entityId, String message) {
			this.id = entityId;
			this.message = message;
		}
	}
	
//	class MyChat extends GuiChat {
//		public MyChat() {
//			super();
//		}
//		
//		@Override
//	    public void onGuiClosed() {
//			super.onGuiClosed();
//			System.out.println("closed");
//		}
//
//		@Override
//	    protected boolean func_175276_a(IChatComponent p_175276_1_) {
//			System.out.println("175276");
//			return super.func_175276_a(p_175276_1_);
//		}
//
//
//		@Override
//	    public void sendChatMessage(String msg, boolean addToChat) {
//			System.out.println("scm "+msg);
//			super.sendChatMessage(msg, addToChat);
//		}
//	}
}

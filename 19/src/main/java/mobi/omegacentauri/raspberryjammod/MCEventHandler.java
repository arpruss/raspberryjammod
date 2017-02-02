package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

abstract public class MCEventHandler {
	protected List<ServerAction> serverActionQueue = new ArrayList<ServerAction>();
	protected volatile boolean pause = false;
	protected boolean doRemote;
	protected List<APIHandler> apiHandlers = new ArrayList<APIHandler>();
	
	public MCEventHandler() {

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
	public void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
		click(event, true);
	}
	
	@SubscribeEvent 
	public void onRightClickEmpty(PlayerInteractEvent.RightClickEmpty event) {
		click(event, true);
	}
	
	@SubscribeEvent 
	public void onRightClickItem(PlayerInteractEvent.RightClickItem event) {
		click(event, true);
	}
	
	@SubscribeEvent 
	public void onLeftClickBlock(PlayerInteractEvent.LeftClickBlock event) {
		click(event, false);
	}
	
	private void click(PlayerInteractEvent event, boolean right) {
		for (APIHandler apiHandler : apiHandlers) {
			apiHandler.click(event, right);
		}
	}
	
	abstract protected World[] getWorlds();

	public void queueServerAction(ServerAction s) {
		synchronized(serverActionQueue) {
			serverActionQueue.add(s);
		}
	}
	
	public void runQueue() {
		if (!pause) {
			synchronized(serverActionQueue) {
				for (ServerAction entry: serverActionQueue) {
					if (! RaspberryJamMod.apiActive)
						break;
					entry.execute();
				}
				serverActionQueue.clear();
			}
		}
		else if (! RaspberryJamMod.apiActive) {
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
		String describe = ""+Block.getIdFromBlock(block)+","+meta+",";

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

	public void setPause(boolean b) {
		pause = b;
	}

	public void registerAPIHandler(APIHandler apiHandler) {
		apiHandlers.add(apiHandler);
	}

	public void unregisterAPIHandler(APIHandler apiHandler) {
		apiHandlers.remove(apiHandler);
	}
}

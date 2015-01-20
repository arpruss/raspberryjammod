package mobi.omegacentauri.raspberryjammod;

import java.beans.EventSetDescriptor;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import net.minecraft.block.state.IBlockState;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.client.event.MouseEvent;
import net.minecraftforge.event.CommandEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.fml.common.FMLCommonHandler;
import net.minecraftforge.fml.common.eventhandler.Event;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.relauncher.Side;

public class MCEventHandler {
	List<SetBlockState> setBlockStateQueue = new ArrayList<SetBlockState>();		
	List<HitDescription> hits = new LinkedList<HitDescription>();
	static final int MAX_HITS = 512;
	private boolean stopChanges = false;
	
	public void setStopChanges(boolean stopChanges) {
		this.stopChanges = stopChanges;
	}
	
	@SubscribeEvent
	public void onPlayerInteractEvent(PlayerInteractEvent event) {
		if (event.action == PlayerInteractEvent.Action.LEFT_CLICK_BLOCK) {
			// TODO: check for sword?
			synchronized(hits) {
				if (hits.size() >= MAX_HITS)
					hits.remove(0);
				hits.add(new HitDescription(event));
			}
		}
		if (stopChanges) {
			event.setCanceled(true);
		}
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

	@SubscribeEvent
	public void onServerTick(TickEvent.ServerTickEvent event) {
		World world = MinecraftServer.getServer().getEntityWorld();
		synchronized(setBlockStateQueue) {
			for (SetBlockState entry: setBlockStateQueue) {
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
			description = ""+pos.getX()+","+pos.getY()+","+pos.getZ()+","+event.face+","+event.entity.getEntityId();
		}
		
		public String getDescription() {
			return description;
		}
	}
}

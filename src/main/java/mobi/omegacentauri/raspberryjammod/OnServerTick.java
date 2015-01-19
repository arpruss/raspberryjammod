package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import net.minecraft.block.state.IBlockState;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent;

public class OnServerTick {
	List<SetBlockState> setBlockStateQueue = new ArrayList<SetBlockState>();	
	
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
}

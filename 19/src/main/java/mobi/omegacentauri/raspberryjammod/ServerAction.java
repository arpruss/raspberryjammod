package mobi.omegacentauri.raspberryjammod;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.world.World;

public abstract class ServerAction {
	abstract public void execute();
	public boolean contains(World w, int x, int y, int z) {
		return false;
	}
	public String describe() {
		return "";
	}
	public int getBlockId() {
		return 0;
	}
	public int getBlockMeta() {
		return 0;
	}
	public BlockState getBlockState() {
		return new BlockState((short)0,(short)0);
	}
}

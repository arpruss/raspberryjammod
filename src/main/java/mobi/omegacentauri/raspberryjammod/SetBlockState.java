package mobi.omegacentauri.raspberryjammod;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.util.BlockPos;
import net.minecraft.world.World;

public class SetBlockState {
	BlockPos pos;
	short id;
	short meta;

	public SetBlockState(short id, short meta) {
		this.id = id;
		this.meta = meta;
	}

	public SetBlockState(BlockPos pos, short id, short meta) {
		this.pos = pos;
		this.id = id;
		this.meta = meta;
	}
	
	public void execute(World world) {
		IBlockState oldState = world.getBlockState(pos);
		Block oldBlock = oldState.getBlock();
		
		if (null != world.getTileEntity(pos))
			world.removeTileEntity(pos);

		if (Block.getIdFromBlock(oldBlock) != (int)id ||
				oldBlock.getMetaFromState(oldState) != (int)meta )
			 world.setBlockState(pos, Block.getBlockById(id).getStateFromMeta(meta), 3);
		// Maybe the update code should be 2? I don't really know.
	}
	
	public boolean contains(int x, int y, int z) {
		return x == pos.getX() && y == pos.getY() && z == pos.getZ();
	}
	
	public String describe() {
		return ""+id+","+meta+",";
	}
}

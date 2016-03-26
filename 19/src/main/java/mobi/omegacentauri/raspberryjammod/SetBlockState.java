package mobi.omegacentauri.raspberryjammod;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.world.World;

public class SetBlockState extends ServerAction {
	Location pos;
	short id;
	short meta;

	public SetBlockState(short id, short meta) {
		this.id = id;
		this.meta = meta;
	}

	public SetBlockState(Location pos, short id, short meta) {
		this.pos = pos;
		this.id = id;
		this.meta = meta;
	}
	
	@Override
	public int getBlockId() {
		return (int)id;
	}

	@Override
	public int getBlockMeta() {
		return (int)meta;
	}
	
	@Override
	public BlockState getBlockState() {
		return new BlockState(id, meta);
	}

	@Override
	public void execute() {
		IBlockState oldState = pos.world.getBlockState(pos);
		Block oldBlock = oldState.getBlock();
		
		if (null != pos.world.getTileEntity(pos))
			pos.world.removeTileEntity(pos);

		if (Block.getIdFromBlock(oldBlock) != (int)id ||
				oldBlock.getMetaFromState(oldState) != (int)meta )
			pos.world.setBlockState(pos, Block.getBlockById(id).getStateFromMeta(meta), 3);
		// Maybe the update code should be 2? I don't really know.
	}
	
	@Override
	public boolean contains(World w, int x, int y, int z) {
		return pos.world == w && x == pos.getX() && y == pos.getY() && z == pos.getZ();
	}
	
	@Override
	public String describe() {
		return ""+id+","+meta+",";
	}
}

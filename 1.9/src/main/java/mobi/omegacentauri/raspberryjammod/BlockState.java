package mobi.omegacentauri.raspberryjammod;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;

class BlockState {
	short id;
	short meta;
	
	public BlockState(short id, short meta) {
		this.id = id;
		this.meta = meta;
	}

	public BlockState(IBlockState blockState) {
		Block block = blockState.getBlock();
		this.id = (short)Block.getIdFromBlock(block);
		this.meta = (short)block.getMetaFromState(blockState);
	}
}


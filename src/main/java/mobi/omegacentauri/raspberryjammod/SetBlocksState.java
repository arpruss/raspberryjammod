package mobi.omegacentauri.raspberryjammod;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.util.BlockPos;
import net.minecraft.world.World;

public class SetBlocksState extends SetBlockState {
	int x2;
	int y2;
	int z2;
	
	public SetBlocksState(BlockPos corner1, BlockPos corner2, short id, short meta) {
		super(id, meta);
		
		int x1 = corner1.getX();
		int y1 = corner1.getY();
		int z1 = corner1.getZ();
		int x2 = corner2.getX();
		int y2 = corner2.getY();
		int z2 = corner2.getZ();
		
		pos = new BlockPos(Math.min(x1, x2), Math.min(y1, y2), Math.min(z1, z2));
		this.x2 = Math.max(x1,x2);
		this.y2 = Math.max(y1,y2);
		this.z2 = Math.max(z1,z2);
	}
	
	@Override
	public void execute(World world) {
		int y1 = pos.getY();
		int z1 = pos.getZ();
		int intId = (int)id;
		int intMeta = (int)meta;
		IBlockState state = Block.getBlockById(intId).getStateFromMeta(intMeta);
		
		for (int x = pos.getX() ; x <= x2 ; x++)
			for (int y = y1 ; y <= y2 ; y++)
				for (int z = z1 ; z <= z2 ; z++) {
					if (! RaspberryJamMod.active)
						break;

					BlockPos here = new BlockPos(x,y,z);
					IBlockState oldState = world.getBlockState(here);
					Block oldBlock = oldState.getBlock();

					if (world.getTileEntity(here) != null) {
						world.removeTileEntity(here);
					}

					if (Block.getIdFromBlock(oldBlock) != intId ||
							oldBlock.getMetaFromState(oldState) != intMeta) {
						world.setBlockState(here, state, 3);
					}
				}
		
	}
	
	@Override
	public boolean contains(int x, int y, int z) {
		return x <= x2 && y <= y2 && z <= z2 && pos.getX() <= x && pos.getY() <= y && pos.getZ() <= z;
	}
}

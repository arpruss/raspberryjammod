package mobi.omegacentauri.raspberryjammod;

import java.util.Iterator;

import net.minecraft.block.Block;
import net.minecraft.block.state.IBlockState;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.nbt.NBTUtil;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.tileentity.TileEntitySign;
import net.minecraft.util.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.registry.FMLControlledNamespacedRegistry;

public class SetBlockNBT extends SetBlockState {
	NBTTagCompound nbt;
	
	// Note: This modifies the nbt tag compound
	public SetBlockNBT(BlockPos pos, short id, short meta, NBTTagCompound nbt) {
		super(pos,id,meta);
		this.nbt = nbt;
	}
	
	@Override
	public void execute(World world) {
		world.setBlockState(pos, Block.getBlockById((int)id).getStateFromMeta((int)meta), 2);
		TileEntity tileEntity = world.getTileEntity(pos);
		if (tileEntity != null) {
			nbt.setInteger("x", pos.getX());
			nbt.setInteger("y", pos.getY());
			nbt.setInteger("z", pos.getZ());
			try {
				tileEntity.readFromNBT(nbt);
			}
			catch(Exception e){}
			tileEntity.markDirty();
		}
	}	

	static public void scrubNBT(NBTTagCompound tag) {
		tag.removeTag("x");
		tag.removeTag("y");
		tag.removeTag("z");
	}
	
	@Override
	public String describe() {
		scrubNBT(nbt);
		return super.describe()+nbt.toString();
	}
}

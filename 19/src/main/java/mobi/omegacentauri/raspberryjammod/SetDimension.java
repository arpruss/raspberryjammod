package mobi.omegacentauri.raspberryjammod;

import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayerMP;

public class SetDimension extends ServerAction {
	Entity entity;
	int dimension;
	
	public SetDimension(Entity e, int dim) {
		this.entity = e;
		this.dimension = dim;
	}
	
	@Override
	public void execute() {
		if (null != RaspberryJamMod.minecraftServer && 
				null != RaspberryJamMod.minecraftServer.worldServerForDimension(dimension))
			return;
		
		if (entity instanceof EntityPlayerMP) {
			RaspberryJamMod.minecraftServer.getPlayerList()
				.changePlayerDimension((EntityPlayerMP)entity, dimension);
		}
		else {
		    // TODO? : move non-players
		}
	}
}

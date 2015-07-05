package mobi.omegacentauri.raspberryjammod;

import net.minecraft.entity.Entity;
import net.minecraft.server.MinecraftServer;

public class SetDimension extends ServerAction {
	Entity entity;
	int dimension;
	
	public SetDimension(Entity e, int dim) {
		this.entity = e;
		this.dimension = dim;
	}
	
	@Override
	public void execute() {
		if (null == MinecraftServer.getServer().worldServerForDimension(dimension))
			return;
		entity.travelToDimension(dimension);
	}
}

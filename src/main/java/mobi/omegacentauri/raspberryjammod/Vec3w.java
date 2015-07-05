package mobi.omegacentauri.raspberryjammod;

import net.minecraft.util.Vec3;
import net.minecraft.world.World;

public class Vec3w extends Vec3 {
	World world;
	
	public Vec3w(World w, double x, double y, double z) {
		super(x,y,z);
		world = w;
	}
}

package mobi.omegacentauri.raspberryjammod;

import net.minecraft.util.math.Vec3d;
import net.minecraft.world.World;

public class Vec3w extends Vec3d {
	World world;
	
	public Vec3w(World w, double x, double y, double z) {
		super(x,y,z);
		world = w;
	}
}

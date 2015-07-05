package mobi.omegacentauri.raspberryjammod;

import net.minecraft.util.BlockPos;
import net.minecraft.util.Vec3;
import net.minecraft.world.World;

public class Location extends BlockPos {
	World world;
	
	// > -2000: world 0, center at 0
	// > -4000: world 1, center at -3000
	// > -6000: world 2, center at -5000
	
	static public World getWorldByEncodedAltitude(World[] serverWorlds, double y) {
		int i = (int)Math.floor(-y / 2000);
		if (i < 0)
			i = 0;
		if (i >= serverWorlds.length)
			i = 0;
		return serverWorlds[i];
	}
	
	static public double decodeAltitude(double y) {
		if (y > -2000)
			return y;
		double i = Math.floor(-y / 2000);
		return y + 2000 * i + 1000;
	}
	
	static public double encodeAltitude(int worldIndex, double y) {
		if (worldIndex == 0) {
			if (y > -2000)
				return y;
			else
				return -1999;
		}
		return y - 1000 - 2000 * worldIndex;
	}

	Location(World world, int x, int y, int z) {
		super(x,y,z);
		this.world = world;
	}

	Location(World world, double x, double y, double z) {
		super(x,y,z);
		this.world = world;
	}

	static Location decodeLocation(World[] serverWorlds, int x, int y, int z) {
		World w = getWorldByEncodedAltitude(serverWorlds, y);
		BlockPos spawnPos = w.getSpawnPoint();
		return new Location(w, x+spawnPos.getX(), (int)decodeAltitude(y)+spawnPos.getY(), z+spawnPos.getZ());
	}

	static Vec3w decodeVec3w(World[] serverWorlds, double x, double y, double z) {
		World w = getWorldByEncodedAltitude(serverWorlds, y);
		BlockPos spawnPos = w.getSpawnPoint();
		return new Vec3w(w, x+spawnPos.getX(), (int)decodeAltitude(y)+spawnPos.getY(), z+spawnPos.getZ());
	}

	public static Vec3 encode(World[] serverWorlds, World w, Vec3 pos) {
		for (int i = 0 ; i < serverWorlds.length ; i++) {
			if (serverWorlds[i] == w) {
				return new Vec3(pos.xCoord, encodeAltitude(i, pos.yCoord), pos.zCoord);
			}
		}
		return pos;
	}
}

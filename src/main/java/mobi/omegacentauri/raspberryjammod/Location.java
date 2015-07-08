package mobi.omegacentauri.raspberryjammod;

import net.minecraft.util.BlockPos;
import net.minecraft.util.Vec3;
import net.minecraft.util.Vec3i;
import net.minecraft.world.World;

public class Location extends BlockPos {
	World world;
	static final int WORLD_SPACING = 2000;
	static final int WORLD_SPACING_HALF = WORLD_SPACING/2;
	
	// Altitudes for world number i are >-WORLD_SPACING_HALF-WORLD_SPACING*i and
	// <= WORLD_SPACING_HALF-WORLD_SPACING*i, with altitude 0 being at -WORLD_SPACING*i.
	// For instance, world 0 (the overworld in the stock setup) is from -WORLD_SPACING_HALF (not
	// inclusive) to WORLD_SPACING_HALF (inclusive), with world 1 right below that, and so on.
	// This allows most old scripts to work fine in multiworld settings.
	
	static public World getWorldByEncodedAltitude(World[] serverWorlds, double y) {
		int i = (int)Math.floor((WORLD_SPACING_HALF-y) / WORLD_SPACING);
		if (i < 0)
			i = 0;
		if (i >= serverWorlds.length)
			i = 0;
		return serverWorlds[i];
	}
	
	static public double decodeAltitude(double y) {
		if (y > -WORLD_SPACING_HALF)
			return y;
		double i = Math.floor((WORLD_SPACING_HALF-y) / WORLD_SPACING);
		return y + WORLD_SPACING * i;
	}
	
	static public double encodeAltitude(int worldIndex, double y) {
		if (worldIndex == 0) {
			if (y > -WORLD_SPACING_HALF)
				return y;
			else
				return 1-WORLD_SPACING_HALF;
		}
		if (y >= WORLD_SPACING_HALF)
			y = WORLD_SPACING_HALF - 1;
		return y - WORLD_SPACING * worldIndex;
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

	public static Vec3 encodeVec3(World[] serverWorlds, World w, Vec3 pos) {
		for (int i = 0 ; i < serverWorlds.length ; i++) {
			if (serverWorlds[i] == w) {
				BlockPos spawnPos = w.getSpawnPoint();
				return new Vec3(pos.xCoord-spawnPos.getX(), encodeAltitude(i, pos.yCoord-spawnPos.getY()), 
						pos.zCoord-spawnPos.getZ());
			}
		}
		return pos;
	}

	public static Vec3i encodeVec3i(World[] serverWorlds, World w, int x, int y, int z) {
		for (int i = 0 ; i < serverWorlds.length ; i++) {
			if (serverWorlds[i] == w) {
				BlockPos spawnPos = w.getSpawnPoint();
				return new Vec3i(x-spawnPos.getX(), encodeAltitude(i, y-spawnPos.getY()), z-spawnPos.getZ());
			}
		}
		return new Vec3i(x,y,z);
	}
}

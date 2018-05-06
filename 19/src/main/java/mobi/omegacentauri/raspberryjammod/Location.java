package mobi.omegacentauri.raspberryjammod;

import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Vec3d;
import net.minecraft.util.math.Vec3i;
import net.minecraft.world.World;

public class Location extends BlockPos {
	World world;
	static final int WORLD_SPACING = 2000;
	static final int WORLD_SPACING_HALF = WORLD_SPACING/2;
    static BlockPos zeroPoint = new BlockPos(0,0,0);
	
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
    
    public static BlockPos getOrigin(World w) {
        if (RaspberryJamMod.absoluteCoordinates)
            return zeroPoint;
        else
            return w.getSpawnPoint();
    }

	static Location decodeLocation(World[] serverWorlds, int x, int y, int z) {
		World w = getWorldByEncodedAltitude(serverWorlds, y);
		BlockPos originPos = getOrigin(w);
		return new Location(w, x+originPos.getX(), (int)decodeAltitude(y)+originPos.getY(), z+originPos.getZ());
	}

	static Vec3w decodeVec3w(World[] serverWorlds, double x, double y, double z) {
		World w = getWorldByEncodedAltitude(serverWorlds, y);
		BlockPos originPos = getOrigin(w);
		return new Vec3w(w, x+originPos.getX(), (int)decodeAltitude(y)+originPos.getY(), z+originPos.getZ());
	}

	public static Vec3d encodeVec3(World[] serverWorlds, World w, Vec3d pos) {
		for (int i = 0 ; i < serverWorlds.length ; i++) {
			if (serverWorlds[i] == w) {
				BlockPos originPos = getOrigin(w);
				return new Vec3d(pos.xCoord-originPos.getX(), encodeAltitude(i, pos.yCoord-originPos.getY()), 
						pos.zCoord-originPos.getZ());
			}
		}
		return pos;
	}

	public static Vec3i encodeVec3i(World[] serverWorlds, World w, int x, int y, int z) {
		for (int i = 0 ; i < serverWorlds.length ; i++) {
			if (serverWorlds[i] == w) {
				BlockPos originPos = getOrigin(w);
				return new Vec3i(x-originPos.getX(), encodeAltitude(i, y-originPos.getY()), z-originPos.getZ());
			}
		}
		return new Vec3i(x,y,z);
	}
}

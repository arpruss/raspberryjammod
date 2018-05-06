package mobi.omegacentauri.raspberryjammod;

import net.minecraft.util.math.BlockPos;
import java.util.ArrayList;
import java.util.List;

import net.minecraft.world.World;

public class Permission {
	List<Rectangle> rectangles;
	static final int ALL = Integer.MIN_VALUE;
	World[] worlds;
	
	public Permission(World[] worlds) {
		this.worlds = worlds;
		rectangles = null;
	}
	
	public boolean permitsEverything() {
		if (rectangles == null)
			return true;
		if (rectangles.size() > 1)
			return false;
		Rectangle r = rectangles.get(0);
		return r.world == null && r.minX == ALL && r.permitted;
	}
	
	private void init() {
		if (rectangles == null)
			rectangles = new ArrayList<Rectangle>();
	}
	
	public void add(World world,int x1,int z1,int x2,int z2,boolean permission) {
		init();
		Rectangle r = new Rectangle(world,x1,z1,x2,z2,permission);
		for (int i = rectangles.size() - 1 ; i >= 0 ; i--) {
			if (r.contains(rectangles.get(i))) {
				rectangles.remove(i);
			}
		}
		rectangles.add(0, r);		
	}
	
	public void add(String s) {
		s = s.toLowerCase().replaceAll("[\\s()]", "");
		String[] items = s.split("(?=(permit|forbid))");
		for (String item : items) {
			boolean permitted = item.startsWith("permit");
			try {
				item = item.substring(6);
				String[] args = item.split(",");
				World world;
				if (args[0].equals("*"))
					world = null;
				else
					world = worlds[Integer.parseInt(args[0])];
				if (args[1].equals("*")) {
					add(world,ALL,ALL,ALL,ALL,permitted);
				}
				else {
					boolean relative = false;
					if (args[1].startsWith("s")) {
						args[1] = args[1].substring(1);
						relative = true;
					}
					int x1 = Integer.parseInt(args[1]);
					int z1 = Integer.parseInt(args[2]);
					int x2 = Integer.parseInt(args[3]);
					int z2 = Integer.parseInt(args[4]);
					
					if (relative) {
						if (world == null) {
							for (World w : worlds) {
                                BlockPos origin = Location.getOrigin(w);
								add(w,x1+origin.getX(),z1+origin.getZ(),
										x2+origin.getX(),z2+origin.getZ(), permitted);
							}
						}
						else {
                            BlockPos origin = Location.getOrigin(world);
							add(world,x1+origin.getX(),z1+origin.getZ(),
									x2+origin.getX(),z2+origin.getZ(), 
									permitted);
						}
					}
					else {
						add(world,x1,z1,x2,z2,permitted);
					}
				}
			}
			catch(Exception e) {
				System.err.println("Cannot parse permission "+item);
				if (! permitted) {
					add(null,ALL,ALL,ALL,ALL,false);
				}
			}
		}
	}
	
	public boolean isPermitted(World w, int x, int z) {
		if (rectangles == null)
			return true; // DEFAULT: permit
		for (Rectangle r : rectangles) {
			if (r.contains(w,x,z)) {
				return r.permitted;
			}
		}
		return true;
	}
	
	public boolean isPermitted(World world, int x1, int z1, int x2, int z2) {
		if (rectangles == null)
			return true; // DEFAULT: permit
		for (Rectangle r : rectangles) {
			if (r.permitted && r.contains(world, x1, z1, x2, z2)) {
				return true;
			}
			else if (! r.permitted && r.overlaps(world, x1, z1, x2, z2)) {
				return false;
			}
		}
		return true;
	}

	static class Rectangle {
		int minX; // Minecraft coordinates
		int minZ;
		int maxX;
		int maxZ;
		World world;
		boolean permitted;
		
		public Rectangle(World world, int x1,int z1,int x2,int z2, boolean permitted) {
			this.permitted = permitted;
			this.world = world;
			if (x1 == ALL) {
				minX = ALL;
				maxX = ALL;
				minZ = ALL;
				maxZ = ALL;
			}
			else {
				if (x1 <= x2) {
					minX = x1;
					maxX = x2;
				}
				else {
					minX = x2;
					maxX = x1;
				}
				if (z1 <= z2) {
					minZ = z1;
					maxZ = z2;
				}
				else {
					minZ = z2;
					maxZ = z1;
				}
			}
		}
		
		public boolean contains(World w, int x, int z) {
			return (world == null || world == w) &&
					(minX == ALL || (minX <= x && x <= maxX && minZ <= z && z <= maxZ));
		}
		
		public boolean contains(Rectangle r) {
			return (world == null || world == r.world) && 
					(minX == ALL || (minX <= r.minX && r.maxX <= maxX && minZ <= r.minZ && r.maxZ <= maxZ));
		}
		
		public boolean contains(World w, int _x1, int _z1, int _x2, int _z2) {
			int x1,z1,x2,z2;
			if (_x1 < _x2) {
				x1 = _x1;
				x2 = _x2;
			}
			else {
				x1 = _x2;
				x2 = _x1;
			}
			if (_z1 < _z2) {
				z1 = _z1;
				z2 = _z2;
			}
			else {
				z1 = _z2;
				z2 = _z1;
			}
			return (world == null || world == w) && 
					(minX == ALL || (minX <= x1 && x2 <= maxX && minZ <= z1 && z2 <= maxZ));
		}
		
		public boolean overlaps(World w, int _x1, int _z1, int _x2, int _z2) {
			int x1,z1,x2,z2;
			if (_x1 < _x2) {
				x1 = _x1;
				x2 = _x2;
			}
			else {
				x1 = _x2;
				x2 = _x1;
			}
			if (_z1 < _z2) {
				z1 = _z1;
				z2 = _z2;
			}
			else {
				z1 = _z2;
				z2 = _z1;
			}
			if (world != null && world != w)
				return false;
			return !(maxX < x1 || x2 < minX || maxZ < z1 || z2 < minZ);
		}
	}
}

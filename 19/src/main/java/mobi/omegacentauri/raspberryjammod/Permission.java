package mobi.omegacentauri.raspberryjammod;

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
		s = s.replaceAll("\\s", "");
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
					add(world,Integer.parseInt(args[1]),Integer.parseInt(args[2]),
							Integer.parseInt(args[3]),Integer.parseInt(args[4]), permitted);
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
//				System.out.println("permission "+x+" "+z+" "+r.permitted);
				return r.permitted;
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
	}
}

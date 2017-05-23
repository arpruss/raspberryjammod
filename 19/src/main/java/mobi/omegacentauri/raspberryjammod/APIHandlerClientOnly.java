package mobi.omegacentauri.raspberryjammod;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.List;

import net.minecraft.client.Minecraft;
import net.minecraft.entity.Entity;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TextComponentString;
import net.minecraft.world.World;
import net.minecraft.world.WorldServer;
import net.minecraft.entity.player.EntityPlayer;

// This class is meant to provide most of the APIHandler facility while one is connected to a
// server. Of course, any block changes won't get written back to the server.

public class APIHandlerClientOnly extends APIHandler {

	public APIHandlerClientOnly(MCEventHandler eventHandler, PrintWriter writer) throws IOException {
		super(eventHandler, writer, false);
		
		handledPermission = true;
	}

	@Override
	protected boolean setup() {
		if (!RaspberryJamMod.integrated) {
			fail("This requires the client");
			return false;
		}
		
		mc = Minecraft.getMinecraft();
		if (mc == null) {
			fail("Minecraft client not yet available");
			return false;
		}		
		
		serverWorlds = new World[] { mc.theWorld };
		
		if (mc.thePlayer == null) {
			fail("Client player not available");
			return false;
		}
		
		playerId = mc.thePlayer.getEntityId();
		playerMP = null;
		havePlayer = true;
		permission = null;
		return true;
	}

	@Override
	protected EntityPlayer getPlayerByNameOrUUID(String name) {
		for (EntityPlayer p : (List<EntityPlayer>)mc.theWorld.playerEntities) {
			if (p.getName().equals(name)) {
				return p;
			}
		}
		for (EntityPlayer p : (List<EntityPlayer>)mc.theWorld.playerEntities) {
			if (p.getUniqueID().toString().equals(name)) {
				return p;
			}
		}
		return null;
	}


	@Override
	protected Entity getServerEntityByID(int id) {
		Entity e = mc.theWorld.getEntityByID(id);
		if (e == null)
			fail("Cannot find entity "+id);
		return e;
	}
	
	@Override
	protected void chat(String msg) {
		mc.thePlayer.addChatComponentMessage(new TextComponentString(msg));
	}

	@Override
	protected void spawnParticle(Scanner scan) {
		String particleName = scan.next();
		double x0 = scan.nextDouble();
		double y0 = scan.nextDouble();
		double z0 = scan.nextDouble();
		Vec3w pos = Location.decodeVec3w(serverWorlds, x0, y0, z0);
		double dx = scan.nextDouble();
		double dy = scan.nextDouble();
		double dz = scan.nextDouble();
		double speed = scan.nextDouble();
		int count = scan.nextInt();

		int[] extras = null;
		EnumParticleTypes particle = null;
		for (EnumParticleTypes e : EnumParticleTypes.values()) {
			if (e.getParticleName().equals(particleName)) {
				particle = e;
				extras = new int[e.getArgumentCount()];
				try {
					for (int i = 0 ; i < extras.length; i++)
						extras[i] = scan.nextInt();
				}
				catch (Exception exc) {}
				break;
			}
		}
		if (particle == null) {
			fail("Cannot find particle type");
		}
		else {
			for (int i = 0 ; i < count ; i++)
				pos.world.spawnParticle(particle, false, pos.xCoord, pos.yCoord, pos.zCoord, dx, dy, dz, extras);
		}
	}

	@Override
	protected void cameraCommand(String cmd, Scanner scan) {
	}
	
	@Override
	protected String mcVersion() {
		return Minecraft.getMinecraft().getVersion();
	}
	
	

}

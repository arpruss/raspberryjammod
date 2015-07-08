package mobi.omegacentauri.raspberryjammod;

import java.io.DataOutputStream;
import java.io.IOException;

import net.minecraft.client.Minecraft;
import net.minecraft.entity.Entity;
import net.minecraft.world.World;

// This class is meant to provide most of the APIHandler facility while one is connected to a
// server. Of course, any block changes won't get written back to the server.

public class APIHandlerClientOnly extends APIHandler {

	public APIHandlerClientOnly(MCEventHandler eventHandler, DataOutputStream writer) throws IOException {
		super(eventHandler, writer);
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
		
		if (! havePlayer) {
			if (mc.thePlayer == null) {
				fail("Client player not available");
				return false;
			}
			playerId = mc.thePlayer.getEntityId();
			havePlayer = true;
		}
		return true;
	}

	@Override
	protected Entity getServerEntityByID(int id) {
		Entity e = mc.theWorld.getEntityByID(id);
		if (e == null)
			fail("Cannot find entity "+id);
		return e;
	}

}

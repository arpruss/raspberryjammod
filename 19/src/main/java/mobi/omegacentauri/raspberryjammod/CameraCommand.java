package mobi.omegacentauri.raspberryjammod;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import net.minecraft.block.Block;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.client.renderer.EntityRenderer;
import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.network.Packet;
import net.minecraft.potion.Potion;
import net.minecraft.potion.PotionEffect;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.TextComponentString;

public class CameraCommand implements ICommand {
	public CameraCommand() {
	}

	@Override
	public List getTabCompletionOptions(MinecraftServer server, 
			ICommandSender sender, String[] args,
			BlockPos pos) {

		if (args.length == 1) {
			List<String> options = new ArrayList<String>();
			if ("distance".startsWith(args[0])) 
				options.add("distance");
			if ("debug".startsWith(args[0]))
				options.add("debug");
			return options;
		}
		else if (args.length == 2 && args[0].equals("debug")) {
			List<String> options = new ArrayList<String>();
			options.add("on");
			options.add("off");
			options.add("toggle");
			return options;
		}
		return null;
	}

	@Override
	public List getCommandAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getCommandName());
		return aliases;
	}

	@Override
	public void execute(MinecraftServer server, ICommandSender sender, String[] args)
			throws CommandException {
		Minecraft mc = Minecraft.getMinecraft();

		if (args.length >= 1 && args[0].equals("debug")) {
			if (args.length == 1 || args[1].equals("toggle")) {
				mc.gameSettings.debugCamEnable = ! mc.gameSettings.debugCamEnable;
			}
			else if (args.length == 2) {
				mc.gameSettings.debugCamEnable = args[1].equals("on") || args[1].equals("1");
			}
			else {
				usage(sender);
			}
		}
		else if (args.length >= 2 && args[0].equals("distance")) {
			try {
				setThirdPersonDistance(Float.parseFloat(args[1]));
			}
			catch (NumberFormatException e) {
			}
		}
		else {
			usage(sender);
		}
	}
	
	public void usage(ICommandSender sender) {
		Minecraft.getMinecraft().thePlayer.addChatComponentMessage(
				new TextComponentString(getCommandUsage(sender)));
	}

	static public void setField(Class c, String field, Object object, Object value) {
		try {
			Field f = c.getDeclaredField(field);
			f.setAccessible(true);
			f.set(object, value);
		}
		catch (Exception e) {
			System.out.println(""+e);
		}
	}

	private void setThirdPersonDistance(float x) {
		Class c = net.minecraft.client.renderer.EntityRenderer.class;
		EntityRenderer r = Minecraft.getMinecraft().entityRenderer;
		setField(c, "thirdPersonDistance",  r, x);
		setField(c, "thirdPersonDistanceTemp", r, x);
		setField(c, "field_78490_B", r, x);
		setField(c, "field_78491_C", r, x);
	}

	@Override
	public String getCommandName() {
		return "camera";
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "camera debug [on|off]\ncamera distance length";
	}

//	@Override
//	public boolean canCommandSenderUse(ICommandSender sender) {
//		return true;
//	}

	@Override
	public boolean isUsernameIndex(String[] args, int index) {
		return false;
	}

	@Override
	public int compareTo(ICommand o) {
		return 0;
	}

	@Override
	public boolean checkPermission(MinecraftServer server, ICommandSender sender) {
		return true;
	}
}

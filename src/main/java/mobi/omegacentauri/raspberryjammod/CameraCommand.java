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

import tv.twitch.chat.IChatAPIListener;

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
import net.minecraft.util.BlockPos;
import net.minecraft.util.ChatComponentText;
import net.minecraft.util.IChatComponent;

public class CameraCommand implements ICommand {
	public CameraCommand() {
	}

	@Override
	public List addTabCompletionOptions(ICommandSender sender, String[] args,
			BlockPos pos) {

		if (args.length == 1) {
			List<String> options = new ArrayList<String>();
			options.add("distance");
			options.add("debug");
			return options;
		}
		else if (args.length == 2 && args[0].equals("debug")) {
			List<String> options = new ArrayList<String>();
			options.add("on");
			options.add("off");
			return options;
		}
		return null;
	}

	@Override
	public List getAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getName());
		return aliases;
	}

	@Override
	public void execute(ICommandSender sender, String[] args)
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
		Minecraft.getMinecraft().thePlayer.addChatComponentMessage(new ChatComponentText(getCommandUsage(sender)));
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
	public int compareTo(Object o) {
		return 0;
	}

	@Override
	public String getName() {
		return "camera";
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "camera debug [on|off]\ncamera distance length";
	}

	@Override
	public boolean canCommandSenderUse(ICommandSender sender) {
		return true;
	}

	@Override
	public boolean isUsernameIndex(String[] args, int index) {
		return false;
	}
}

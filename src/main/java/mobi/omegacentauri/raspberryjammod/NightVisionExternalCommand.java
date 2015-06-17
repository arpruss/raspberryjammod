package mobi.omegacentauri.raspberryjammod;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import tv.twitch.chat.IChatAPIListener;

import net.minecraft.block.Block;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
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

public class NightVisionExternalCommand implements ICommand {
	private MCEventHandler eventHandler;

	public NightVisionExternalCommand(MCEventHandler eventHandler) {
		this.eventHandler = eventHandler;
	}

	@Override
	public List addTabCompletionOptions(ICommandSender sender, String[] args,
			BlockPos pos) {
		
		if (args.length == 1) {
			List<String> options = new ArrayList<String>();
			options.add("off");
			options.add("on");
			return options;
		}
		return null;
	}

	@Override
	public List getAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getName());
		aliases.add("nv");
		return aliases;
	}

	@Override
	public void execute(ICommandSender sender, String[] args)
			throws CommandException {
                boolean nv;

		if (args.length == 0) {
                    nv = ! eventHandler.nightVision;
		}
		else if (args[0].toLowerCase().equals("on")) {
                    nv = true;
                }
                else if (args[0].toLowerCase().equals("off")) {
                    nv = false;
                }
                else {
		    throw new CommandException("Usage: /nightvision [on|off]");
                }

		eventHandler.nightVision = nv;
		EntityPlayerSP player = Minecraft.getMinecraft().thePlayer;
		if (player != null) {
  		if (nv) {
  				player.addPotionEffect(new PotionEffect(Potion.nightVision.id, 4096));
  				player.addChatComponentMessage(new ChatComponentText("Enabled night vision"));
  		}
  		else {
  				player.removePotionEffect(Potion.nightVision.id);
  				player.addChatComponentMessage(new ChatComponentText("Disabled night vision"));
  		}
  	}
	}

	@Override
	public int compareTo(Object o) {
		return 0;
	}

	@Override
	public String getName() {
		return "nightvision";
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "nightvision [on|off]";
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


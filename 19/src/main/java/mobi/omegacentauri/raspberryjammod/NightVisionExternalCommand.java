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

import net.minecraft.block.Block;
import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.init.MobEffects;
import net.minecraft.network.Packet;
import net.minecraft.potion.Potion;
import net.minecraft.potion.PotionEffect;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.TextComponentString;

public class NightVisionExternalCommand implements ICommand {
	private ClientEventHandler eventHandler;

	public NightVisionExternalCommand(ClientEventHandler eventHandler2) {
		this.eventHandler = eventHandler2;
	}

	@Override
	public List getTabCompletionOptions(MinecraftServer server, 
			ICommandSender sender, String[] args,
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
	public List getCommandAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getCommandName());
		aliases.add("nv");
		return aliases;
	}

	@Override
	public void execute(MinecraftServer server, ICommandSender sender, String[] args)
			throws CommandException {
		boolean nv;

		if (args.length == 0) {
			nv = ! eventHandler.getNightVision();
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

		eventHandler.setNightVision(nv);
		EntityPlayerSP player = Minecraft.getMinecraft().thePlayer;
		
		if (player != null) {
			if (nv) {
				player.addPotionEffect(new PotionEffect(MobEffects.nightVision, 4096));
				player.addChatComponentMessage(new TextComponentString("Enabled night vision"));
			}
			else {
				player.removePotionEffect(MobEffects.nightVision);
				player.addChatComponentMessage(new TextComponentString("Disabled night vision"));
			}
		}
	}

	@Override
	public String getCommandName() {
		return "nightvision";
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "nightvision [on|off]";
	}

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

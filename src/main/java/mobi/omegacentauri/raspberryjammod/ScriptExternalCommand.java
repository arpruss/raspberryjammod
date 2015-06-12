package mobi.omegacentauri.raspberryjammod;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.lang.ProcessBuilder.Redirect;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import tv.twitch.chat.IChatAPIListener;

import net.minecraft.client.Minecraft;
import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.network.Packet;
import net.minecraft.util.BlockPos;
import net.minecraft.util.ChatComponentText;
import net.minecraft.util.IChatComponent;

public abstract class ScriptExternalCommand implements ICommand {
	abstract protected String getScriptProcessorCommand();
	abstract protected String getExtension();
	abstract protected String[] getScriptPaths();
	Process runningScript = null;
	final String scriptProcessorPath;
	
	public ScriptExternalCommand() {
		System.out.println("Starting ScriptExternalCommand");
		scriptProcessorPath = getScriptProcessorPath();
	}

	private boolean sandboxedScriptPath(String path) {
		// only allow scripts from the selected directories, and don't allow leaving them
		// by using .., and also don't allow passing options to the script
		// processor.
		return ! path.startsWith(".") &&
				! path.contains("/.") &&
				! ( isWindows() && ( path.contains(":") || path.contains("\\.") ) );
	}

	@Override
	public List addTabCompletionOptions(ICommandSender sender, String[] args,
			BlockPos pos) {

		if (! sandboxedScriptPath(args[0]))
			return null;

		if (args.length == 1) {
			int lastSlash = args[0].lastIndexOf('/');
			String subdir = "";
			if (lastSlash != -1) {
				subdir = args[0].substring(0, lastSlash + 1);
			}
			List<String> scripts = getScripts(subdir);
			for (int i = scripts.size() - 1; i>=0; i--)
				if (! scripts.get(i).toLowerCase().startsWith(args[0].toLowerCase()))
					scripts.remove(i);
			return scripts;
		}
		return null;
	}

	protected List<String> getScripts(String subdir) {
		List<String> scripts = new ArrayList<String>();
		String ext = getExtension();
		
		for (String dir : getScriptPaths()) {
			File[] files = new File(dir+subdir).listFiles();
			if (files != null) 
				for (File f : files) {
					String name = f.getName();
					if (! name.startsWith(".") && f.canRead()) {
						if (name.endsWith(ext) && f.isFile()) 
							scripts.add(subdir + name.substring(0, name.length()-ext.length()));
						else if (f.isDirectory())
							scripts.add(subdir + name + "/");
					}
				}
		}
		
		Collections.sort(scripts);
		for (int i = scripts.size() - 1 ; i > 0 ; i--) 
			if (scripts.get(i).equals(scripts.get(i-1)))
				scripts.remove(i);
		
		return scripts;
	}
	@Override
	public List getAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getName());
		return aliases;
	}
	
	protected String extraPath() {
		return "";
	}

	protected String getScriptProcessorPath() {
		String base = getScriptProcessorCommand();
		
		System.out.println("searching");

		String pathSep = System.getProperty("path.separator");
		String fileSep = System.getProperty("file.separator");
		if (base.contains("/") || base.contains(fileSep)) {
			System.out.println("base");
			return base;
		}
		
		String pathVar = System.getenv("PATH");
		String extra = extraPath();
		if (pathVar == null) {
			if (extra.length()==0)
				return base;
			else
				pathVar = extra;				
		}
		else if (extra.length()>0) {
			pathVar = pathVar + pathSep + extra;
		}
		System.out.println("path " +pathVar);
		
		String exeExt = isWindows() ? ".exe" : "";
		
		String[] paths = pathVar.split(pathSep); 
		
		for (String dir : paths) {
			String p = dir + fileSep + base + exeExt;
			if (new File(p).canExecute())
				return p;
		}
		
		return base;
	}
	
	public static boolean isWindows() {
		return System.getProperty("os.name").startsWith("Windows");
	}
	
	// returns true if there actually was a script to close
	public boolean close() {
		boolean closed = false;
		
		if (runningScript != null) {
			try {
				runningScript.exitValue();
			}
			catch (IllegalThreadStateException e) {
				// script was still running
				closed = true;
				runningScript.destroy();
			}
			runningScript = null;
		}

		return closed;
	}

	@Override
	public void execute(ICommandSender sender, String[] args)
			throws CommandException {
                if (! RaspberryJamMod.allowRemote &&
                        ! sender.getCommandSenderName().equals(Minecraft.getMinecraft().thePlayer.username)) {
			Minecraft.getMinecraft().thePlayer.addChatComponentMessage(new ChatComponentText("Blocked remote script launch by "+sender.getCommandSenderName()));
			return;
                }
		if (runningScript != null) {
			if (close()) {
				Minecraft.getMinecraft().thePlayer.addChatComponentMessage(new ChatComponentText("Stopped previous script."));
//				Minecraft.getMinecraft().thePlayer.sendChatMessage("Stopped previous script.");
			}
		}
		
		if (args.length == 0) {
			return;
		}

		if (! sandboxedScriptPath(args[0])) {
			throw new CommandException("Unacceptable script name");
		}
			
		File script = getScript(args[0]);
		if (script == null) {
			throw new CommandException("Cannot find script");
		}
		
		List<String> cmd = new ArrayList<String>();
		cmd.add(scriptProcessorPath);
		cmd.add(script.getName());
		for (int i = 1 ; i < args.length ; i++)
			cmd.add(args[i]);
		
		ProcessBuilder pb = new ProcessBuilder(cmd);
//		pb.redirectErrorStream(true);
		pb.directory(script.getParentFile());
	        Map<String, String> environment = pb.environment();
	        environment.put("MINECRAFT_PLAYER_NAME", sender.getCommandSenderName());

//		pb.inheritIO();
		pb.command(cmd);
		try {
			System.out.println("Running "+script);
			runningScript = pb.start();
			gobble(runningScript.getInputStream(), "");
			gobble(runningScript.getErrorStream(), "[ERR] ");
		} catch (IOException e) {
			throw new CommandException("Error "+e);
		}
	}
	
	private void gobble(final InputStream stream, final String label) {
		Thread t = new Thread() {
			
			@Override
			public void run() {
				BufferedReader br;
				
				br = new BufferedReader(new InputStreamReader(stream));
			
				String line;
				try {
					while ( null != ( line = br.readLine()) ) {
						line.trim();
						Minecraft.getMinecraft().thePlayer.addChatComponentMessage(new ChatComponentText(label + line));
					}
				} catch (IOException e) {
				}
				
				try {
					br.close();
				} catch (IOException e) {
				}
			}
		};
		t.setDaemon(true);
		t.start();
	}
	
	protected File getScript(String base) {
		String[] paths = getScriptPaths();

		String ext = getExtension();		

		String name = base;
		
		if (! name.endsWith(ext))
			name += getExtension();
		
		for (String path : paths) {
			try {
				File f = new File(path + name);
				if (f.canRead()) 
					return f;
			}
			catch(SecurityException e) {
			}
		}
		return null;
	}
}


package mobi.omegacentauri.raspberryjammod;

import java.io.File;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.util.ArrayList;
import java.util.List;

import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.util.BlockPos;

public abstract class ScriptExternalCommand implements ICommand {
	abstract protected String getScriptProcessorBase();
	abstract protected String[] getExtensions();
	abstract protected String[] getScriptPaths();
	Process runningScript = null;
	final String scriptProcessorPath;
	
	public ScriptExternalCommand() {
		scriptProcessorPath = getScriptProcessorPath();
	}

	@Override
	public List getAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getName());
		return aliases;
	}

	protected String getScriptProcessorPath() {
		String base = getScriptProcessorBase();
		
		String pathVar = System.getenv("PATH");
		System.out.println(pathVar);
		if (pathVar == null)
			return base;
		
		String exeExt = System.getProperty("os.name").startsWith("Windows") ? ".exe" : "";
		
		String[] paths = pathVar.split(System.getProperty("path.separator")); 
		
		for (String dir : paths) {
			String p = dir + System.getProperty("file.separator") + base + exeExt;
			if (new File(p).canExecute())
				return p;
		}
		
		return base;
	}
	
	
	@Override
	public void execute(ICommandSender sender, String[] args)
			throws CommandException {
		if (runningScript != null) {
			runningScript.destroy();
			runningScript = null;
			if (args.length == 0) {
				return;
			}
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
		pb.redirectErrorStream(true);
		pb.directory(script.getParentFile());
		pb.inheritIO();
		pb.command(cmd);
		try {
			System.out.println("Running "+script);
			runningScript = pb.start();
		} catch (IOException e) {
			throw new CommandException("Error "+e);
		}
	}
	
	protected File getScript(String base) {
		String[] paths = getScriptPaths();
		String[] exts = getExtensions();
		
		for (String ext : exts) {
			if (ext.startsWith(".") && base.endsWith(ext)) {
				// already have extension
				exts = new String[]{""};
				break;
			}
		}
		
		for (String path : paths) {
			for (String ext : exts) {
				try {
					File f = new File(path + base + ext);
					if (f.canRead()) 
						return f;
				}
				catch(SecurityException e) {
				}
			}
		}
		return null;
	}
}

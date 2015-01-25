package mobi.omegacentauri.raspberryjammod;

import java.io.File;
import java.io.IOException;
import java.lang.ProcessBuilder.Redirect;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.util.BlockPos;

public abstract class ScriptExternalCommand implements ICommand {
	abstract protected String getScriptProcessorBase();
	abstract protected String getExtension();
	abstract protected String[] getScriptPaths();
	Process runningScript = null;
	final String scriptProcessorPath;
	
	public ScriptExternalCommand() {
		scriptProcessorPath = getScriptProcessorPath();
	}

	@Override
	public List addTabCompletionOptions(ICommandSender sender, String[] args,
			BlockPos pos) {
		if (args.length == 1) {
			List<String> scripts = getScripts();
			for (int i = scripts.size() - 1; i>=0; i--)
				if (! scripts.get(i).toLowerCase().startsWith(args[0].toLowerCase()))
					scripts.remove(i);
			return scripts;
		}
		return null;
	}

	protected List<String> getScripts() {
		List<String> scripts = new ArrayList<String>();
		String ext = getExtension();
		
		for (String dir : getScriptPaths()) {
			File[] files = new File(dir).listFiles();
			if (files != null) 
				for (File f : files) {
					String name = f.getName();
					if (name.endsWith(ext) && f.isFile() && f.canRead()) 
						scripts.add(name.substring(0, name.length()-ext.length()));
				}
		}
		
		Collections.sort(scripts);
		
		return scripts;
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

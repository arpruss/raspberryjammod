package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.server.MinecraftServer;

public class PythonExternalCommand extends ScriptExternalCommand {
	
	public PythonExternalCommand(boolean clientSide) {
		super(clientSide);
	}
	
	@Override
	public String getCommandName() {
		return "python";
	}

	@Override
	public List getCommandAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getCommandName());
		aliases.add("py");
		return aliases;
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "python script [arguments]: run script, stopping old one(s) (omit script to stop previous script(s))";
	}

	@Override
	public boolean isUsernameIndex(String[] args, int index) {
		return false;
	}

	@Override
	protected String extraPath() {
		if (isWindows())
			return "\\python27\\;python27\\";
		else
			return "";
	}

	@Override
	protected String getScriptProcessorCommand() {
		return RaspberryJamMod.pythonInterpreter;
	}

	@Override
	protected String getExtension() {
		return ".py";
	}

	@Override
	protected String[] getScriptPaths() {
		return new String[] { "mcpipy/" , "mcpimods/python/"};
	}

	@Override
	public boolean checkPermission(MinecraftServer server, ICommandSender sender) {
		return true;
	}

	@Override
	public int compareTo(ICommand o) {
		return 0;
	}
}


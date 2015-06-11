package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.util.BlockPos;

public class PythonExternalCommand extends ScriptExternalCommand {

	public PythonExternalCommand() {
		super();
	}
	
	@Override
	public String getName() {
		return "python";
	}

	@Override
	public List getAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getName());
		aliases.add("py");
		return aliases;
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "python script [arguments]: run script (omit script to stop previous script)";
	}

	@Override
	public boolean canCommandSenderUse(ICommandSender sender) {
		return true;
	}


	@Override
	public boolean isUsernameIndex(String[] args, int index) {
		return false;
	}

	@Override
	public int compareTo(Object o) {
		return 0;
	}
	
	@Override
	protected String extraPath() {
		if (isWindows())
			return "\\python27\\";
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
}

package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.command.ICommandSender;

public class LocalPythonExternalCommand extends PythonExternalCommand {

	public LocalPythonExternalCommand(boolean clientSide) {
		super(clientSide);
	}
	
	@Override
	public String getCommandName() {
		return "lpython";
	}
	
	@Override
	public List<String> getCommandAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getCommandName());
		aliases.add("lpy");
		return aliases;
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "lpython script [arguments]: run local script, stopping old one(s) (omit script to stop previous script(s))";
	}
}

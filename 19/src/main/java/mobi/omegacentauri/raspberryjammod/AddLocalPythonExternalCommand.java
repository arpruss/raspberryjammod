package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;

public class AddLocalPythonExternalCommand extends PythonExternalCommand {
	public AddLocalPythonExternalCommand(boolean clientSide) {
		super(clientSide);
	}

	@Override
	public String getCommandName() {
		return "addlpython";
	}

	@Override
	public List getCommandAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getCommandName());
		aliases.add("alpy");
		return aliases;
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "addlpython script arguments: run a new local script without stopping old one(s)";
	}

	@Override
	public boolean addMode() {
		return true;
	}
}


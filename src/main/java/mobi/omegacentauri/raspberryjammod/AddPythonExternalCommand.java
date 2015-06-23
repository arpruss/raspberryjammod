package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.util.BlockPos;

public class AddPythonExternalCommand extends PythonExternalCommand {

	public AddPythonExternalCommand() {
		super();
	}
	
	@Override
	public String getName() {
		return "addpython";
	}

	@Override
	public List getAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getName());
		aliases.add("apy");
		return aliases;
	}

	@Override
	public String getCommandUsage(ICommandSender sender) {
		return "addpython script arguments: run a new script without stopping old one(s)";
	}

	@Override
	public boolean addMode() {
		return true;
	}
}


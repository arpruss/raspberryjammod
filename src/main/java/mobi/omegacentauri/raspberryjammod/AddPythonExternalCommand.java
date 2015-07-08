package mobi.omegacentauri.raspberryjammod;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.command.CommandException;
import net.minecraft.command.ICommand;
import net.minecraft.command.ICommandSender;
import net.minecraft.util.BlockPos;

public class AddPythonExternalCommand extends PythonExternalCommand {

	public AddPythonExternalCommand(boolean clientSide) {
		super(clientSide);
	}
	
	@Override
	public String getName() {
		return clientSide ? "laddpython" : "addpython";
	}

	@Override
	public List getAliases() {
		List<String> aliases = new ArrayList<String>();
		aliases.add(getName());
		aliases.add(clientSide ? "lapy" : "apy");
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


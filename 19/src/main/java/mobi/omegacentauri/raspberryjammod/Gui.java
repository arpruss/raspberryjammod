package mobi.omegacentauri.raspberryjammod;

import net.minecraft.client.gui.GuiScreen;
import net.minecraftforge.common.config.ConfigElement;
import net.minecraftforge.common.config.Configuration;
import net.minecraftforge.fml.client.config.GuiConfig;

public class Gui extends GuiConfig {
	public Gui(GuiScreen parent) {
		super(parent,
		        new ConfigElement(RaspberryJamMod.configFile.getCategory(Configuration.CATEGORY_GENERAL)).getChildElements(),
		        "RaspberryJamMod", false, false, GuiConfig.getAbridgedConfigPath(RaspberryJamMod.configFile.toString()));
	}
}
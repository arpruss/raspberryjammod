# Raspberry Jam Mod
Raspberry Jam Mod is a Minecraft Forge mod for Minecraft version 1.8+ that implements most of Raspberry Juice/Pi API. This mod allows Minecraft players to interact with the Minecraft world using the Raspberry Pi and the Python programming language.

## Target
This mod is ideal for Minecraft players who are interested in using the Raspberry Pi to enhance their Minecraft experience, as well as Raspberry Pi enthusiasts who want to use Minecraft as a platform for learning Python.

## Features
- Interact with the Minecraft world using Python
- Use the Raspberry Pi to control Minecraft
- Write and run scripts in Minecraft using the Raspberry Pi
- Automate tasks and build custom Minecraft creations using Python

## Prerequisites
Before using the Raspberry Jam Mod, you need to have:
- A Minecraft profile of version 1.8 or later
- The latest version of Minecraft Forge for your precise Minecraft version (http://files.minecraftforge.net/)
- Python installed (if not already installed)

## Installation (Single-Player and LAN)
- Set up a Minecraft profile of the correct Minecraft version and run it once.
- Install the latest version of Minecraft Forge for your precise Minecraft version (http://files.minecraftforge.net/).
- Put the contents of the mods.zip file in your .minecraft/mods folder. There will be a number of subfolders like 1.8, 1.8.9, etc. All the subfolders should be placed in the mods folder.
- Put the sample scripts in your .minecraft/mcpipy directory.
- Windows users can automate steps 3-4 by using the .exe installer.

## Installation (Server)
- Download a Forge planner from http://files.minecraftforge.net/
- Run the Forge planner and point it to a directory where you want your server to be located. Select "Server" and it will download and install a Minecraft server.
- Create a mods/ folder in the server directory and put the RaspberryJamMod.jar for your server version there.
- Put some sample scripts in a mcpipy/ subdirectory of the same folder as your Minecraft server. Make sure to include all mcpipy/mcpi.
- If your server is open outside your LAN, make a passwords.dat file and place it in your server directory. Make sure each of your users has a .minecraft/mcpipy/mcpi/security.py file that matches the passwords.dat file. See SECURITY.md for more information.
- Instead of running minecraft_server_X.Y.jar to start the server, run the Forge jar.

## Launching Scripts
On a server, the command /py launches a script in the server's mcpipy/ directory, while /lpy launches a script in the client's .minecraft/mcpipy/ directory. Note that /lpy only works if the client has the mod installed. If the client does not have the mod installed, they can still run scripts manually by making sure the script contains the server IP.

## Passwords.dat
The passwords.dat file is used for security purposes on servers that are open outside the LAN. 

## Examples
Here are some examples of what you can do with Raspberry Jam Mod:

- Automate tasks like harvesting crops and replanting them
- Build custom Minecraft creations using Python, such as a functioning calculator or a weather station
- Create a game within Minecraft using Python, such as a platformer or a puzzle game
- Control Minecraft with the Raspberry Pi, such as using a physical button to start a script
- Monitor the Minecraft world, such as detecting player movement and triggering events

## Usage
Here is an example of how to use Raspberry Jam Mod to automate a task in Minecraft:

```
# import the mcpi.minecraft module
import mcpi.minecraft as minecraft

# connect to the Minecraft game
mc = minecraft.Minecraft.create()

# get the player's position
player_pos = mc.player.getTilePos()

# set the block in front of the player to dirt
mc.setBlock(player_pos.x + 1, player_pos.y, player_pos.z, dirt)
```

You can run this script in Minecraft by using the /py command in the game chat. The script will set the block in front of the player to dirt.

## Support
If you encounter any issues or have questions about Raspberry Jam Mod, you can reach out to the developers of this mod.
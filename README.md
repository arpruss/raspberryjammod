# raspberryjammod
Raspberry Jam Mod - a Mod Forge Minecraft 1.8+ mod implementing most of Raspberry Juice/Pi API

To install for single-player and LAN use (as well as for client-side use with a server):
 1. Set up a Minecraft profile of the correct Minecraft version and run it once.
 2. Install the lastest version of Minecraft Forge for your precise Minecraft version (http://files.minecraftforge.net/)
 3. Put the contents of mods.zip in your .minecraft/mods folder (there will be a number of 
    subfolders like 1.8, 1.8.9, etc.--they should all go there).
 4. Put the sample scripts in in your .minecraft/mcpipy directory.
 5. Install Python if you need to.
On Windows, steps 3-5 can be automated by using the .exe installer.

To install on a server:
 1. Download a Forge installer from http://files.minecraftforge.net/
 2. Run and it point it to a directory where you want your server to be, select "Server", 
    and it will download and install a Minecraft server.
 3. Create a mods/ folder in the server directory and put RaspberryJamMod.jar for your
    server version there.
 4. Put some sample scripts in a mcpipy/ subdirectory of the same folder as your minecraft server.
    Make sure to include all mcpipy/mcpi. 
 5. If your server is open outside your LAN make a passwords.dat file and place it in your server directory, and make sure
    each of your users has a .minecraft/mcpipy/mcpi/security.py file that matches it. See SECURITY.md for more information.
 6. Instead of running minecraft_server_X.Y.jar to start the server, run the forge jar.

On a server, /py launches a script in the server's mcpipy/ directory, while /lpy launches a script in the client's 
.minecraft/mcpipy/ directory. Note that /lpy only works if the client has the mod installed (otherwise, the user has
to submit script for curation and inclusion on the server, or launch them manually outside of Minecraft, making sure
their script contains the server IP; this is automagically handled if the script is launched via /lpy.
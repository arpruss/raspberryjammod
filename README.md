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
 5. If your server is open outside your LAN make a passwords.dat file and place it in your server directory, making sure
    that the permissions allow the server to read it, but no one else. The simplest passwords.dat file has plain ASCII
    text lines of the form `username password`, with neither the username nor the password having spaces. I strongly
    recommend that the passwords be random alphanumeric strings rather than human-memorizable passwords, so that if the server
    is compromised, the users' passwords on other services are not compromised. Each client should then have a security.py
    file in their .minecraft/mcpipy/mcpi directory with the lines `AUTHENTICATION_USERNAME="username"` and 
    `AUTHENTICATION_PASSWORD="password"`. For the username, you can use either the human-readable Minecraft username or,
    better, the user's UUID.
 6. Instead of running minecraft_server_X.Y.jar to start the server, run the forge jar.

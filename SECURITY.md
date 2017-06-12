By default, RaspberryJamMod accepts all incoming port 4711 connections and allows them control over the Minecraft
world. If port 4711 is open to the outside internet, or you have pranksters on your LAN, this is unacceptable. You then
have a choice: either disable remote connections in the RaspberryJamMod options by using the GUI mod configuration for the desktop 
version or else making sure that config/raspberryjammod.cfg exists and contains the line 

    B:"Remote Connections"=false

Otherwise, you should use the password authentication system. The latter will require each client script to authenticate 
itself to the server.

The password authentication system is based on a `raspberryjammod_passwords.dat` file in the .minecraft/ or Minecraft 
server directory. The simplest version raspberryjammod_passwords.dat file has plain ASCII text lines of the form `username password`, 
with neither the username nor the password having spaces. 

It is strongly recommended that the passwords be random alphanumeric strings generated for this purpose rather than 
human-memorizable passwords, so that if the server is compromised, the users' passwords on other services are not 
compromised. Each client should then have a security.py file in their .minecraft/mcpipy/mcpi directory with the lines 

    AUTHENTICATION_USERNAME="username"
    AUTHENTICATION_PASSWORD="password"
    
For the username, you can use either the human-readable Minecraft username or, better, the user's UUID.

There is also a permissions system implemented via a raspberryjammod_permissions.dat file, which allows you to restrict
the regions of the world(s) which a given user's script can modify. This is experimental and may not work at all. The
idea is that the permissions file contains lines like:

    username allow|forbid w,[s]x1,z1,x2,z2
    
where w designates the world number (0=overworld) and x1,z1,x2,z2 designate the coordinates that apply to the allowance or 
forbidding, with an "s" prefixed if the coordinates are relative to the spawn point (as in python scripts). Later lines 
take precedence over lower ones. You can also use "*" as a wildcard for the username, for the world, and for the 
coordinate-quadruple. For instance, it's not a bad idea to start a permissions file with:

    * forbid *,*
    
which should forbid users from modifying anything anywhere unless explicitly allowed later on in the file.


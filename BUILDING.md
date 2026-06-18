The build script system has only been tried on Windows+Cygwin. 

For the full build that generates a Windows .exe installer, you need to make sure that you 
have a 2.7.x Win32 CPython in a py27 subdirectory and a 3.x Win32 CPython in the py3 
subdirectory.

Running the root build.sh should:
 - build versions of the mod for Minecraft 1.8-1.10.2, with output in the build/ directory
 - build an Inno Setup .exe installer for the mod
 - install all the mod versions in the correct subdirectories of %appdata%\.minecraft\mods
 
You can skip the Inno Setup step by adding a "noinstaller" argument to build.sh.
You can skip the mod installation step by adding a "noinstall" argument to build.sh.
You can specify the directory to install the mods to by doing something like:
    APPDATA=/directory/above/my/dotminecraft build.sh

Running fast.sh in a source directory will build the specific version of the mod and install
it in the correct subdirectory of %appdata%\.minecraft\mods 

A "noinstall" argument will skip the mod installation, and you can use APPDATA as above.
 
root directory : version for Minecraft 1.8x
19  : version for Minecraft 1.9
194 : version for Minecraft 1.9.4
110 : version for Minecraft 1.10
111 : version for Minecraft 1.11
112 : version for Minecraft 1.12

The 194 and 110 versions do not contain source code. Instead, running fast.sh in those
directories copies the source tree from the 19 directory, patches it up as needed, and
builds it. Any modifications to 194/src and 110/src will thus be lost. Modifications 
should be made only to the root src directory or the 19/src directory.

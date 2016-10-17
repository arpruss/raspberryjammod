rm build/libs/Raspberr*.jar 2> /dev/null
sh gradlew build
# --offline build
rm build/libs/Raspberry*ources.jar 2> /dev/null
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar 2> /dev/null
mkdir ../build/out 2> /dev/null
mkdir ../build/out/1.9 2> /dev/null
cp build/libs/RaspberryJamMod.jar ../build/out/1.9/ 
if [ "$1" != "noinstall" ]
then
    mkdir $APPDATA/.minecraft/mods 2> /dev/null
    mkdir $APPDATA/.minecraft/mods/1.9 2> /dev/null
    cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.9/
else
    echo Skipping mod installation.
fi

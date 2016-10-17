rm build/libs/Raspberr*.jar  2> /dev/null
./gradlew --offline build
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar
mkdir build/out 2> /dev/null
mkdir build/out/1.8  2> /dev/null
mkdir build/out/1.8.8  2> /dev/null
mkdir build/out/1.8.9  2> /dev/null
cp build/libs/RaspberryJamMod.jar build/out/1.8
cp build/libs/RaspberryJamMod.jar build/out/1.8.8
cp build/libs/RaspberryJamMod.jar build/out/1.8.9
if [ "$1" != "noinstall" ]
then
    mkdir $APPDATA/.minecraft/mods  2> /dev/null
    mkdir $APPDATA/.minecraft/mods/1.8  2> /dev/null
    mkdir $APPDATA/.minecraft/mods/1.8.8  2> /dev/null
    mkdir $APPDATA/.minecraft/mods/1.8.9  2> /dev/null
    cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8
    cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8.8
    cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8.9
else
    echo Skipping mod installation.
fi    

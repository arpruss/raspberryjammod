rm build/libs/Raspberr*.jar
./gradlew.bat --offline build
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar
mkdir $APPDATA/.minecraft/mods/1.8
mkdir $APPDATA/.minecraft/mods/1.8.8
mkdir $APPDATA/.minecraft/mods/1.8.9
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8.8
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8.9

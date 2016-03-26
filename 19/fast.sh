rm build/libs/Raspberr*.jar
./gradlew.bat --offline build
rm build/libs/Raspberry*ources.jar
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.9/


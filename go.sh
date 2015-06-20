./zip.sh
rm build/libs/*
./gradlew.bat --offline build
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/
./makesetup.sh

(cd 19 && sh fast.sh)
(cd 194 && sh fast.sh)
(cd 110 && sh fast.sh)
./zip.sh
rm build/libs/*
./gradlew.bat build
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8/
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8.8/
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.8.9/
mkdir build/out
mkdir build/out/1.8
mkdir build/out/1.8.8
mkdir build/out/1.8.9
mkdir build/out/1.9
mkdir build/out/1.9.4
mkdir build/out/1.10
mkdir build/out/1.10.2
cp build/libs/RaspberryJamMod.jar build/out/1.8/
cp build/libs/RaspberryJamMod.jar build/out/1.8.8/
cp build/libs/RaspberryJamMod.jar build/out/1.8.9/
cp 19/build/libs/RaspberryJamMod.jar build/out/1.9/
cp 194/build/libs/RaspberryJamMod.jar build/out/1.9.4/
cp 110/build/libs/RaspberryJamMod.jar build/out/1.10/
cp 110/build/libs/RaspberryJamMod.jar build/out/1.10.2/
(cd build/out && zip -9r ../mods *)
./makesetup.sh
cp python-scripts.zip build/

if [ -d src ]; then
   rm -rf src
fi
cp -r ../19/src .
for x in src/main/java/mobi/omegacentauri/raspberryjammod/*.java ; do
    sed -i -f fix.sed $x 
done
rm build/libs/Raspberr*.jar
./gradlew.bat build
# --offline build
rm build/libs/Raspberry*ources.jar
mv build/libs/Raspberr* build/libs/RaspberryJamMod.jar
cp build/libs/RaspberryJamMod.jar $APPDATA/.minecraft/mods/1.9.4/


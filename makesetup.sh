version=`sed -n 's/^version *= *//p' build.gradle`
echo Building setup for $version
sed -i "s/#define MyAppVersion .*/#define MyAppVersion $version/" RaspberryJamMod.iss
"C:/Program Files (x86)/Inno Setup 5/compil32" /cc RaspberryJamMod.iss

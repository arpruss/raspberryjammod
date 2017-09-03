sed -i 's/public static final String VERSION [^;]*/public static final String VERSION = "'$1'"/' src/main/java/mobi/omegacentauri/raspberryjammod/RaspberryJamMod.java 19/src/main/java/mobi/omegacentauri/raspberryjammod/RaspberryJamMod.java
sed -i 's/^version = "[^"]*"/version = "'$1'"/' build.gradle 19/build.gradle 194/build.gradle 110/build.gradle 111/build.gradle 112/build.gradle

NOINSTALLER=""
NOINSTALL=""
for arg in "$@"
do
    if [ "$arg" = "noinstaller" ]
    then
        echo "Will not build installer"
        NOINSTALLER=$arg
    fi
    if [ "$arg" = "noinstall" ]
    then
        echo "Will not install mod"
        NOINSTALL=$arg
    fi
done    
(cd 19 && sh fast.sh $NOINSTALL)
(cd 194 && sh fast.sh $NOINSTALL)
(cd 110 && sh fast.sh $NOINSTALL)
(cd 111 && sh fast.sh $NOINSTALL)
(cd 112 && sh fast.sh $NOINSTALL)
sh fast.sh $NOINSTALL
sh zip-scripts.sh
(cd build/out && zip -9r ../mods *)
cp build/mods.zip .
if [ "$NOINSTALLER" != "noinstaller" ]
then
    ./makesetup.sh
fi    
cp python-scripts.zip build/

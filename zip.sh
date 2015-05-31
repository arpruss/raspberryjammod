rm python2-scripts.zip
rm python3-scripts.zip
rm -rf python3-scripts
mkdir python3-scripts
rm -f python2-scripts/mcpipy/*.{bak,pyc} python2-scripts/mcpipy/*/*.{bak,pyc}
cp -rf python2-scripts/* python3-scripts
chmod -R u+rw python[23]-scripts
cd python3-scripts/mcpipy
for x in *.py */*.py ; do
  2to3 -w $x
done
rm -f *.{bak,pyc} */*.{bak,pyc}
cd ..
zip -9r ../python3-scripts.zip mcpipy
cd ../python2-scripts
zip -9r ../python2-scripts.zip mcpipy
cd ..

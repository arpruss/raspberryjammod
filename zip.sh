cd src/mcpipy
for x in *.py ; do
  cp $x ../../python2-scripts/mcpipy/
  cp $x ../../python3-scripts/mcpipy/
  2to3 -w ../../python3-scripts/mcpipy/$x
done
cd ../..

cd python2-scripts
zip -9r ../python2-scripts.zip mcpipy
cd ..
cd python3-scripts
rm *.bak
zip -9r ../python3-scripts.zip mcpipy
rm python2-scripts.zip
rm python3-scripts.zip
chmod -R u+rw python[23]-scripts
#cd python3-scripts/mcpipy
#for x in *.py ; do
#  2to3 -w $x
#done
#rm -f *.{bak,pyc} */*.{bak,pyc}
#cd ..
cd python3-scripts/mcpipy
rm -rf *.{bak,pyc} */*.{bak,pyc} __pycache__ */__pycache__ */*/__pycache__
cd ..
zip -9r ../python3-scripts.zip mcpipy
cd ../python2-scripts
zip -9r ../python2-scripts.zip mcpipy
cd ..

mkdir packager/assets
cp raspberryjampe.js packager/assets/
rm -rf p2
mkdir p2
rm -rf p3
mkdir p3
cp -r `grep -l Pruss ../python2-scripts/mcpipy/*.py` ../python2-scripts/mcpipy/mcpi p2
rm p2/neurosky.py
cp -r `grep -l Pruss ../python3-scripts/mcpipy/*.py` ../python3-scripts/mcpipy/mcpi p3
rm p3/neurosky.py
echo "isPE = False" > p2/mcpi/settings.py
echo "isPE = False" > p3/mcpi/settings.py
echo 'address = "127.0.0.1"' > p2/server.py
echo 'is_pi = False' >> p2/server.py
echo 'address = "127.0.0.1"' > p3/server.py
echo 'is_pi = False' >> p3/server.py
chmod -R u+rw p2 p3
rm packager/assets/*.zip
(cd p2 && zip -9r ../packager/assets/p2 *)
(cd p3 && zip -9r ../packager/assets/p3 *)

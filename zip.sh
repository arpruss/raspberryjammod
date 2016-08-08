rm python-scripts.zip
echo AUTHENTICATION_USERNAME=None > python-scripts/mcpipy/mcpi/security-template.py
echo AUTHENTICATION_PASSWORD=None >> python-scripts/mcpipy/mcpi/security-template.py
cd python-scripts/mcpipy
rm -rf *.{bak,pyc} */*.{bak,pyc} __pycache__ */__pycache__ */*/__pycache__
rm -f security.py
rm -f _sunfish.*
cd ..
zip -9r ../python-scripts.zip mcpipy
cd ..

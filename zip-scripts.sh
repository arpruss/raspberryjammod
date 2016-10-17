rm python-scripts.zip
echo AUTHENTICATION_USERNAME=None > mcpipy/mcpi/security-template.py
echo AUTHENTICATION_PASSWORD=None >> mcpipy/mcpi/security-template.py
cd mcpipy
rm -rf *.{bak,pyc} */*.{bak,pyc} __pycache__ */__pycache__ */*/__pycache__
rm -f security.py
rm -f _sunfish.*
cd ..
zip -9r python-scripts.zip mcpipy


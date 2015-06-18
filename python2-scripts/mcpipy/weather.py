from mc import *
from text8x8 import *
import sys,json,urllib2

try:
    city = argv[1]
except:
    city = 'Waco,TX'

url = "http://api.openweathermap.org/data/2.5/weather?q="+city
response = urllib2.urlopen(url)
weather = json.loads(response.read())
output = ""
try:
    output += weather['name']+"\n"
except:
    pass

try:
    output += "Temperature: "+str((weather['main']['temp']-273.15)*1.8+32.0)+"\n"
except:
    pass

try:
    output += weather['weather'][0]['description']+"\n"
except:
    pass

if output[len(output)-1] == '\n':
    output = output[:-1]

mc = Minecraft()
pos = mc.player.getPos()
forward = angleToTextDirection(mc.player.getRotation())
foreground = 169 # sea lantern
background = OBSIDIAN

drawText8x8(mc, pos, forward, Vec3(0,1,0), output, foreground, background)

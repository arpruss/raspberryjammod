from PIL import Image
from os import listdir

def averageColor(filename):
    image = Image.open(filename).convert('RGB')
    r,g,b = 0.,0.,0.
    pixels = image.size[0] * image.size[1]
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            rgb = image.getpixel((x,y))
            r += rgb[0]
            g += rgb[1]
            b += rgb[2]
    image.close()
    return int(round(r/pixels)), int(round(g/pixels)), int(round(b/pixels))
	
print("colorDictionary={")	
for f in listdir('assets/minecraft/textures/blocks'):
    if f.lower().endswith(".png"):
        print("  '"+f[:-4]+"': "+str(averageColor('assets/minecraft/textures/blocks/'+f))+",")
print("}");
		
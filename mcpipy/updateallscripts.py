import json
import sys
import os.path
import os

try:
    import urllib.request as urllib_request
except:
    import urllib2 as urllib_request
    
baseDir = os.path.dirname(sys.argv[0])
    
def updateDirectory(dir, path):
    url = "https://api.github.com/repos/arpruss/raspberryjammod/contents/" + path
    print("Updating "+path+" from "+url)
    content = json.loads(urllib_request.urlopen(url).read())
    for item in content:
        if item['type'] == 'dir':
            updateDirectory(os.path.join(dir, item['name']), item['path'])
        elif item['type'] == 'file':
            name = item['name']
            print("Updating "+path+"/"+name)
            url = item['download_url']
            newPath = os.path.join(dir, name)
            tempPath = newPath+".tmpDownload"
            try:
                with open(tempPath,"wb") as f:
                    f.write(urllib_request.urlopen(url).read())
            except Exception as e:
                os.remove(tempPath)
                raise e
            if os.path.exists(newPath):
                os.remove(newPath)
            try:
                os.rename(tempPath, newPath)                
            except Exception as e:
                print("Update failed and corrupted a file. Manually copy "+tempPath+" to "+newPath)
                sys.exit(1)
    
updateDirectory(os.path.dirname(sys.argv[0]), "mcpipy")

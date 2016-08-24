from mine import *

def book(title=None, pages=["page 1", "page 2"], author=None):
    def fix(s):
        s = s.replace("\\", "\\u005c")
        s = s.replace('"', "\\u0022")
        s = s.replace(',', "\\u002c")
        s = s.replace("'", "\\u0027")
        s = s.replace('\r\n', '\\\\n')
        s = s.replace('\r', '\\\\n')
        s = s.replace('\n', '\\\\n')
        s = s.replace('}', '\\u007d')
        s = s.replace('{', '\\u007b')
        s = s.replace(']', '\\u005d')
        s = s.replace('[', '\\u005b')
        return s
    out = '{Item:{id:"minecraft:written_book",Count:1,Damage:0,tag:{'
    out += "title:'" + fix(title) + "',"
    out += "author:'" + fix(author) + "',"
    out += "pages:["
    for i,page in enumerate(pages):
        out += str(i)+":'"+fix(page)+"',"
    out += "]}}}"
    return out

mc = Minecraft()

pos = mc.player.getTilePos()
e = mc.spawnEntity('Item', pos, book(title="My title", pages=[open('writebook.py').read(), 'page 2'], author="Me, myself and I"))

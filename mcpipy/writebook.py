#
# Code by Alexander Pruss and under the MIT license
#

from mine import *

def book(title=None, pages=["page 1", "page 2"], author=None):
    def fix(s):
        s = s.replace("\r\n", "\n")
        s = s.replace("\r", "\n")
        out = ""
        for c in s:
            if c.isalnum() or c == " " or c == ".":
                out += c
            else:
                out += "\\u%04x" % ord(c)
        return out
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
mc.spawnEntity('Item', pos, book(title="writebook.py", 
    pages=[open('writebook.py').read(), 'page 2'], 
    author="Me, myself and I"))

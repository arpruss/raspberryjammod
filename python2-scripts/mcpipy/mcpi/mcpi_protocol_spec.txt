MCPI-PROTOCOL 0.1

OVERVIEW
The mcpi-protocol enables an external process (program) to interact with a
running instance of Minecraft Pi Edition.

The protocol can easily be implemented and used from any programming language
that has network socket support. The mcpi release includes api libraries (with
source) for Python and Java.

* Tcp-socket, port 4711
* Commands are clear text lines (ASCII, LF terminated)


DEFINITIONS
x,y,z -- vector of three integers.
xf,yf,zf -- vector of three floats.
blockTypeId -- integer 0-108. 0 is air.
blockData -- integer 0-15. Block data beyond the type, for example wool color.

See: http://www.minecraftwiki.net/wiki/Data_values_(Pocket_Edition)


COORDINATE SYSTEM
Most coordinates are in the form of a three integer vector (x,y,z) which
address a specific tile in the game world. (0,0,0) is the spawn point sea
level. (X,Z) is the ground plane and Y is towards the sky.


COMMANDS
-- World --
world.getBlock(x,y,z) --> blockTypeId

world.setBlock(x,y,z,blockTypeId)
world.setBlock(x,y,z,blockTypeId,blockData)

world.setBlocks(x1,y1,z1,x2,y2,z2,blockTypeId)
world.setBlocks(x1,y1,z1,x2,y2,z2,blockTypeId,blockData)

world.getHeight(x,z) --> Integer

world.checkpoint.save()
world.checkpoint.restore()

TODO: skriva ut KEYs
world.setting(KEY,0/1)

chat.post(message)

-- Camera --
camera.mode.setNormal()
camera.mode.setThirdPerson()
camera.mode.setFixed()
camera.mode.setPos(x,y,z)

-- Player --
player.getTile() --> x,y,z
player.setTile(x,y,z)

player.getPos() --> xf,yf,zf
player.setPos(xf,yf,zf)

-- Entities --
TBD


-- Events --
events.block.hits() --> pos,surface,entityId|pos,surface,entityId|... (pos is x,y,z surface is x,y,z, entityId is int)
events.clear

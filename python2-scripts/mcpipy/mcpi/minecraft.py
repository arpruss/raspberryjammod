from connection import Connection
from vec3 import Vec3
from event import BlockEvent,ChatEvent
from block import Block
import math
from util import flatten,floorFlatten

""" Minecraft PI low level api v0.1_1

    Note: many methods have the parameter *arg. This solution makes it
    simple to allow different types, and variable number of arguments.
    The actual magic is a mix of flatten_parameters() and __iter__. Example:
    A Cube class could implement __iter__ to work in Minecraft.setBlocks(c, id).

    (Because of this, it's possible to "erase" arguments. CmdPlayer removes
     entityId, by injecting [] that flattens to nothing)

    @author: Aron Nieminen, Mojang AB"""


#def strFloor(*args):
#    return [str(int(math.floor(x))) for x in flatten(args)]

class CmdPositioner:
    """Methods for setting and getting positions"""
    def __init__(self, connection, packagePrefix):
        self.conn = connection
        self.pkg = packagePrefix

    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        return int(self.conn.sendReceive_flat("world.getBlock", floorFlatten(args)))

    def getPitch(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + ".getPitch", id)
        return float(s)

    def getRotation(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + ".getRotation", id)
        return float(s)

    def getDirection(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + ".getDirection", id)
        return Vec3(*map(float, s.split(",")))

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + ".getPos", id)
        return Vec3(*map(float, s.split(",")))

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + ".getPos", id)
        return Vec3(*map(float, s.split(",")))

    def setPos(self, id, *args):
        """Set entity position (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + ".setPos", id, args)

    def setDirection(self, id, *args):
        """Set entity pitch (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + ".setDirection", id, args)

    def setRotation(self, id, *args):
        """Set entity rotation (entityId:int, angle)"""
        self.conn.send(self.pkg + ".setRotation", id, args)

    def setPitch(self, id, *args):
        """Set entity pitch (entityId:int, angle)"""
        self.conn.send(self.pkg + ".setPitch", id, args)

    def getTilePos(self, id):
        """Get entity tile position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + ".getTile", id)
        return Vec3(*map(int, s.split(",")))

    def setTilePos(self, id, *args):
        """Set entity tile position (entityId:int) => Vec3"""
        self.conn.send_flat(self.pkg + ".setTile", id, floorFlatten(*args))

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        self.conn.send(self.pkg + ".setting", setting, 1 if bool(status) else 0)


class CmdEntity(CmdPositioner):
    """Methods for entities"""
    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, "entity")


class CmdPlayer(CmdPositioner):
    """Methods for the host (Raspberry Pi) player"""
    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, "player")
        self.conn = connection

    def getDirection(self):
        return CmdPositioner.getDirection(self, [])
    def getPitch(self):
        return CmdPositioner.getPitch(self, [])
    def getRotation(self):
        return CmdPositioner.getRotation(self, [])
    def setPitch(self, *args):
        return CmdPositioner.setPitch(self, [], args)
    def setRotation(self, *args):
        return CmdPositioner.setRotation(self, [], args)
    def setDirection(self, *args):
        return CmdPositioner.setDirection(self, [], args)
    def getRotation(self):
        return CmdPositioner.getRotation(self, [])
    def getPos(self):
        return CmdPositioner.getPos(self, [])
    def setPos(self, *args):
        return CmdPositioner.setPos(self, [], args)
    def getTilePos(self):
        return CmdPositioner.getTilePos(self, [])
    def setTilePos(self, *args):
        return CmdPositioner.setTilePos(self, [], args)

class CmdCamera:
    def __init__(self, connection):
        self.conn = connection

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        self.conn.send("camera.mode.setNormal", args)

    def setFixed(self):
        """Set camera mode to fixed view"""
        self.conn.send("camera.mode.setFixed")

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        self.conn.send("camera.mode.setFollow", args)

    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        self.conn.send("camera.setPos", args)


class CmdEvents:
    """Events"""
    def __init__(self, connection):
        self.conn = connection

    def clearAll(self):
        """Clear all old events"""
        self.conn.send("events.clear")

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive("events.block.hits")
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*map(int, e.split(","))) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive("events.chat.posts")
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]

class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi."""

    def __init__(self, connection=None):
        if connection:
            self.conn = connection
        else:
            self.conn = Connection()

        self.camera = CmdCamera(self.conn)
        self.entity = CmdEntity(self.conn)
        self.player = CmdPlayer(self.conn)
        self.events = CmdEvents(self.conn)

    def spawnEntity(self, *args):
        """Spawn entity (type,x,y,z,tags) and get its id => id:int"""
        return int(self.conn.sendReceive("world.spawnEntity", args))

    def removeEntity(self, *args):
        """Remove entity (id)"""
        self.conn.send("world.removeEntity", args)

    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        return int(self.conn.sendReceive_flat("world.getBlock", floorFlatten(args)))

    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block"""
        ans = self.conn.sendReceive_flat("world.getBlockWithData", floorFlatten(args))
        return Block(*map(int, ans.split(",")))
    """
        @TODO
    """
    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        return int(self.conn.sendReceive_flat("world.getBlocks", floorFlatten(args)))

    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        self.conn.send_flat("world.setBlock", floorFlatten(args))

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        self.conn.send_flat("world.setBlocks", floorFlatten(args))

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        return int(self.conn.sendReceive_flat("world.getHeight", floorFlatten(args)))

    def getPlayerId(self, *args):
        """Get the id of the current player"""
        return int(self.conn.sendReceive_flat("world.getPlayerId", floorFlatten(args)))

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        ids = self.conn.sendReceive("world.getPlayerIds")
        return map(int, ids.split("|"))

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.conn.send("world.checkpoint.save")

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint"""
        self.conn.send("world.checkpoint.restore")

    def postToChat(self, msg):
        """Post a message to the game chat"""
        self.conn.send("chat.post", msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        self.conn.send("world.setting", setting, 1 if bool(status) else 0)

    @staticmethod
    def create(address = None, port = None):
        return Minecraft(Connection(address, port))


if __name__ == "__main__":
    mc = Minecraft.create()
    mc.postToChat("Hello, Minecraft!")

from . import settings

class Block:
    """Minecraft PI block description. Can be sent to Minecraft.setBlock/s"""
    def __init__(self, id, data=0):
        self.id = id
        self.data = data

    def __cmp__(self, rhs):
        return hash(self) - hash(rhs)

    def __hash__(self):
        return (self.id << 8) + self.data

    def withData(self, data):
        return Block(self.id, data)

    def __iter__(self):
        """Allows a Block to be sent whenever id [and data] is needed"""
        return iter((self.id, self.data))
        
    def __repr__(self):
        return "Block(%d, %d)"%(self.id, self.data)

AIR                 = Block(0)
STONE               = Block(1)
GRASS               = Block(2)
DIRT                = Block(3)
COBBLESTONE         = Block(4)
WOOD_PLANKS         = Block(5)
SAPLING             = Block(6)
BEDROCK             = Block(7)
WATER_FLOWING       = Block(8)
WATER               = WATER_FLOWING
WATER_STATIONARY    = Block(9)
LAVA_FLOWING        = Block(10)
LAVA                = LAVA_FLOWING
LAVA_STATIONARY     = Block(11)
SAND                = Block(12)
GRAVEL              = Block(13)
GOLD_ORE            = Block(14)
IRON_ORE            = Block(15)
COAL_ORE            = Block(16)
WOOD                = Block(17)
LEAVES              = Block(18)
GLASS               = Block(20)
LAPIS_LAZULI_ORE    = Block(21)
LAPIS_LAZULI_BLOCK  = Block(22)
SANDSTONE           = Block(24)
BED                 = Block(26)
COBWEB              = Block(30)
GRASS_TALL          = Block(31)
WOOL                = Block(35)
FLOWER_YELLOW       = Block(37)
FLOWER_CYAN         = Block(38)
MUSHROOM_BROWN      = Block(39)
MUSHROOM_RED        = Block(40)
GOLD_BLOCK          = Block(41)
IRON_BLOCK          = Block(42)
STONE_SLAB_DOUBLE   = Block(43)
STONE_SLAB          = Block(44)
BRICK_BLOCK         = Block(45)
TNT                 = Block(46)
BOOKSHELF           = Block(47)
MOSS_STONE          = Block(48)
OBSIDIAN            = Block(49)
TORCH               = Block(50)
FIRE                = Block(51)
STAIRS_WOOD         = Block(53)
CHEST               = Block(54)
DIAMOND_ORE         = Block(56)
DIAMOND_BLOCK       = Block(57)
CRAFTING_TABLE      = Block(58)
FARMLAND            = Block(60)
FURNACE_INACTIVE    = Block(61)
FURNACE_ACTIVE      = Block(62)
DOOR_WOOD           = Block(64)
LADDER              = Block(65)
STAIRS_COBBLESTONE  = Block(67)
DOOR_IRON           = Block(71)
REDSTONE_ORE        = Block(73)
SNOW                = Block(78)
ICE                 = Block(79)
SNOW_BLOCK          = Block(80)
CACTUS              = Block(81)
CLAY                = Block(82)
SUGAR_CANE          = Block(83)
FENCE               = Block(85)
GLOWSTONE_BLOCK     = Block(89)
BEDROCK_INVISIBLE   = Block(95)
if settings.isPE:
   STAINED_GLASS = WOOL
else:
   STAINED_GLASS = Block(95)
STONE_BRICK         = Block(98)
GLASS_PANE          = Block(102)
MELON               = Block(103)
FENCE_GATE          = Block(107)
REDSTONE_BLOCK      = Block(152)
CARPET              = Block(171)
COAL_BLOCK          = Block(173)
GLOWING_OBSIDIAN    = Block(246)
NETHER_REACTOR_CORE = Block(247)
if not settings.isPE:
    REDSTONE_LAMP_INACTIVE = Block(123)
    REDSTONE_LAMP_ACTIVE   = Block(124)
else:
    REDSTONE_LAMP_INACTIVE = OBSIDIAN
    REDSTONE_LAMP_ACTIVE = GLOWING_OBSIDIAN

SUNFLOWER  = Block(175,0)
LILAC      = Block(175,1)
DOUBLE_TALLGRASS = Block(175,2)
LARGE_FERN       = Block(175,3)
ROSE_BUSH        = Block(175,4)
PEONY            = Block(175,5)

WOOL_WHITE = Block(WOOL.id, 0)
WOOL_ORANGE = Block(WOOL.id, 1)
WOOL_MAGENTA = Block(WOOL.id, 2)
WOOL_LIGHT_BLUE = Block(WOOL.id, 3)
WOOL_YELLOW = Block(WOOL.id, 4)
WOOL_LIME = Block(WOOL.id, 5)
WOOL_PINK = Block(WOOL.id, 6)
WOOL_GRAY = Block(WOOL.id, 7)
WOOL_LIGHT_GRAY = Block(WOOL.id, 8)
WOOL_CYAN = Block(WOOL.id, 9)
WOOL_PURPLE = Block(WOOL.id, 10)
WOOL_BLUE = Block(WOOL.id, 11)
WOOL_BROWN = Block(WOOL.id, 12)
WOOL_GREEN = Block(WOOL.id, 13)
WOOL_RED = Block(WOOL.id, 14)
WOOL_BLACK = Block(WOOL.id, 15)

CARPET_WHITE = Block(CARPET.id, 0)
CARPET_ORANGE = Block(CARPET.id, 1)
CARPET_MAGENTA = Block(CARPET.id, 2)
CARPET_LIGHT_BLUE = Block(CARPET.id, 3)
CARPET_YELLOW = Block(CARPET.id, 4)
CARPET_LIME = Block(CARPET.id, 5)
CARPET_PINK = Block(CARPET.id, 6)
CARPET_GRAY = Block(CARPET.id, 7)
CARPET_LIGHT_GRAY = Block(CARPET.id, 8)
CARPET_CYAN = Block(CARPET.id, 9)
CARPET_PURPLE = Block(CARPET.id, 10)
CARPET_BLUE = Block(CARPET.id, 11)
CARPET_BROWN = Block(CARPET.id, 12)
CARPET_GREEN = Block(CARPET.id, 13)
CARPET_RED = Block(CARPET.id, 14)
CARPET_BLACK = Block(CARPET.id, 15)

STAINED_GLASS_WHITE = Block(STAINED_GLASS.id, 0)
STAINED_GLASS_ORANGE = Block(STAINED_GLASS.id, 1)
STAINED_GLASS_MAGENTA = Block(STAINED_GLASS.id, 2)
STAINED_GLASS_LIGHT_BLUE = Block(STAINED_GLASS.id, 3)
STAINED_GLASS_YELLOW = Block(STAINED_GLASS.id, 4)
STAINED_GLASS_LIME = Block(STAINED_GLASS.id, 5)
STAINED_GLASS_PINK = Block(STAINED_GLASS.id, 6)
STAINED_GLASS_GRAY = Block(STAINED_GLASS.id, 7)
STAINED_GLASS_LIGHT_GRAY = Block(STAINED_GLASS.id, 8)
STAINED_GLASS_CYAN = Block(STAINED_GLASS.id, 9)
STAINED_GLASS_PURPLE = Block(STAINED_GLASS.id, 10)
STAINED_GLASS_BLUE = Block(STAINED_GLASS.id, 11)
STAINED_GLASS_BROWN = Block(STAINED_GLASS.id, 12)
STAINED_GLASS_GREEN = Block(STAINED_GLASS.id, 13)
STAINED_GLASS_RED = Block(STAINED_GLASS.id, 14)
STAINED_GLASS_BLACK = Block(STAINED_GLASS.id, 15)

LEAVES_OAK_DECAYABLE = Block(LEAVES.id, 0)
LEAVES_SPRUCE_DECAYABLE = Block(LEAVES.id, 1)
LEAVES_BIRCH_DECAYABLE = Block(LEAVES.id, 2)
LEAVES_JUNGLE_DECAYABLE = Block(LEAVES.id, 3)
LEAVES_OAK_PERMANENT = Block(LEAVES.id, 4)
LEAVES_SPRUCE_PERMANENT = Block(LEAVES.id, 5)
LEAVES_BIRCH_PERMANENT = Block(LEAVES.id, 6)
LEAVES_JUNGLE_PERMANENT = Block(LEAVES.id, 7)
if settings.isPE:
    LEAVES_ACACIA_DECAYABLE = Block(161,0)
    LEAVES_DARK_OAK_DECAYABLE = Block(161,1)
    LEAVES_ACACIA_PERMANENT = Block(161,2)
    LEAVES_DARK_OAK_PERMANENT = Block(161,3)
else:
    LEAVES_ACACIA_DECAYABLE = LEAVES_OAK_DECAYABLE
    LEAVES_DARK_OAK_DECAYABLE = LEAVES_JUNGLE_DECAYABLE
    LEAVES_ACACIA_PERMANENT = LEAVES_OAK_PERMANENT
    LEAVES_DARK_OAK_PERMANENT = LEAVES_JUNGLE_PERMANENT

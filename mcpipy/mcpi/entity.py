class Entity:
    '''Minecraft PI entity description for RaspberryJuice compatibility'''

    def __init__(self, id, name = None):
        self.id = id
        self.name = name

    def __cmp__(self, rhs):
        return hash(self) - hash(rhs)

    def __eq__(self, rhs):
        return self.id == rhs.id

    def __hash__(self):
        return self.id

    def __iter__(self):
        '''Allows an Entity to be sent whenever id is needed'''
        return iter((self.id,))

    def __repr__(self):
        return 'Entity(%d)'%(self.id)

ITEM = "Item"
XPORB = "XPOrb"
LEASHKNOT = "LeashKnot"
PAINTING = "Painting"
ARROW = "Arrow"
SNOWBALL = "Snowball"
FIREBALL = "Fireball"
SMALLFIREBALL = "SmallFireball"
THROWNENDERPEARL = "ThrownEnderpearl"
EYEOFENDERSIGNAL = "EyeOfEnderSignal"
THROWNPOTION = "ThrownPotion"
THROWNEXPBOTTLE = "ThrownExpBottle"
ITEMFRAME = "ItemFrame"
WITHERSKULL = "WitherSkull"
PRIMEDTNT = "PrimedTnt"
FALLINGSAND = "FallingSand"
FIREWORKSROCKETENTITY = "FireworksRocketEntity"
ARMORSTAND = "ArmorStand"
BOAT = "Boat"
MINECARTRIDEABLE = "MinecartRideable"
MINECARTCHEST = "MinecartChest"
MINECARTFURNACE = "MinecartFurnace"
MINECARTTNT = "MinecartTNT"
MINECARTHOPPER = "MinecartHopper"
MINECARTSPAWNER = "MinecartSpawner"
MINECARTCOMMANDBLOCK = "MinecartCommandBlock"
MOB = "Mob"
MONSTER = "Monster"
CREEPER = "Creeper"
SKELETON = "Skeleton"
SPIDER = "Spider"
GIANT = "Giant"
ZOMBIE = "Zombie"
SLIME = "Slime"
GHAST = "Ghast"
PIGZOMBIE = "PigZombie"
ENDERMAN = "Enderman"
CAVESPIDER = "CaveSpider"
SILVERFISH = "Silverfish"
BLAZE = "Blaze"
LAVASLIME = "LavaSlime"
ENDERDRAGON = "EnderDragon"
WITHERBOSS = "WitherBoss"
BAT = "Bat"
WITCH = "Witch"
ENDERMITE = "Endermite"
GUARDIAN = "Guardian"
PIG = "Pig"
SHEEP = "Sheep"
COW = "Cow"
CHICKEN = "Chicken"
SQUID = "Squid"
WOLF = "Wolf"
MUSHROOMCOW = "MushroomCow"
SNOWMAN = "SnowMan"
OZELOT = "Ozelot"
VILLAGERGOLEM = "VillagerGolem"
HORSE = "EntityHorse"
RABBIT = "Rabbit"
VILLAGER = "Villager"
ENDERCRYSTAL = "EnderCrystal"
PLAYER = "(ThePlayer)"

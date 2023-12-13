import enum


class SpritePosition(enum.Enum):
    DOOR = (544, 437)
    FRIDGE = (302, 403)
    BED = (694, 382)
    TABLE = (400, 359)
    ANIMAL_FOOD = (226, 349)
    PLAYING_ZONE = (509, 131)
    ADD_ROOM_DOOR = (599, 283)
    ADD_WINDOW = (398, 456)
    ADD_CENTER = (408, 248)
    ADD_TABLE_CORNER = (444, 420)


class KittenPositions(enum.Enum):
    KITTEN_COUCH = (115, 229)
    KITTEN_PLAYING_ZONE = (460, 103)
    KITTEN_EAT = (223, 324)
    KITTEN_WITH_MOTHER = (336, 224)

class SpriteAngle(enum.Enum):
    BED = 260


class FaceSide(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Variables(enum.Enum):
    SATIETY = 0
    ENERGY = 1
    MONEY = 2
    PRODUCTS = 3
    LOVE = 4
    FUN = 5


class KittenStates(enum.Enum):
    EATING = 0,
    SLEEPING = 1,
    WITH_MOTHER = 2,
    PLAYING_WITH_OWNER = 3,
    SEARCHING = 4,
    SUNBEAM = 5,
    WAITING = 6


class PersonStates(enum.Enum):
    EATING = 0,
    SLEEPING = 1,
    WORKING = 2,
    BUYING_PRODUCTS = 3,
    PLAYING_WITH_CAT = 4,
    PLAYING_WITH_KITTEN = 5,
    FEEDING_CAT = 6,
    FEEDING_KITTEN = 7,
    WAITING = 8,
    WALKING = 9




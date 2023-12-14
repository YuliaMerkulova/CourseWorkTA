import enum


class SpritePosition(enum.Enum):
    PERSON_DOOR = (544, 437)
    PERSON_FRIDGE = (302, 403)
    PERSON_BED = (708, 380)
    PERSON_TABLE = (400, 359)
    PERSON_ANIMAL_FOOD = (226, 349)
    PERSON_PLAYING_ZONE = (509, 131)
    PERSON_ADD_ROOM_DOOR = (599, 283)
    PERSON_ADD_WINDOW = (398, 456)
    PERSON_ADD_CENTER = (408, 248)
    PERSON_ADD_TABLE_CORNER = (444, 420)

    KITTEN_COUCH = (115, 229)
    KITTEN_PLAYING_ZONE = (460, 103)
    KITTEN_EAT = (223, 324)
    KITTEN_WITH_MOTHER = (336, 224)


class SpriteAngle(enum.Enum):
    DEFAULT = 0
    PERSON_BED = 260


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
    EATING = 0
    SLEEPING = 1
    WITH_MOTHER = 2
    PLAYING_WITH_OWNER = 3
    SEARCHING = 4
    SUNBEAM = 5
    WAITING = 6


class PersonStates(enum.Enum):
    EATING = 0
    SLEEPING = 1
    WORKING = 2
    BUYING_PRODUCTS = 3
    PLAYING_WITH_CAT = 4
    PLAYING_WITH_KITTEN = 5
    FEEDING = 6
    WAITING = 7  # TODO: remove
    WALKING = 8  # TODO: remove

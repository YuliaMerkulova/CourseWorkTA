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



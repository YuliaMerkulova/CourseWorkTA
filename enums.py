import enum


class SpritePosition(enum.Enum):
    PERSON_DOOR = (544, 437)
    PERSON_FRIDGE = (302, 403)
    PERSON_BED = (708, 380)
    PERSON_TABLE = (400, 359)
    PERSON_ANIMAL_FOOD = (246, 359)
    PERSON_PLAYING_ZONE = (509, 131)
    PERSON_ADD_ROOM_DOOR = (599, 283)
    PERSON_ADD_WINDOW = (398, 456)
    PERSON_ADD_CENTER = (408, 298)
    PERSON_ADD_TABLE_CORNER = (444, 420)

    KITTEN_COUCH = (115, 229)
    KITTEN_PLAYING_ZONE = (460, 103)
    KITTEN_EAT = (223, 324)
    KITTEN_WITH_MOTHER = (336, 224)

    CAT_COUCH = (211, 190)
    CAT_EAT = (223, 318)
    CAT_WITH_KITTEN = (370, 216)
    CAT_PLAYING_ZONE = (460, 103)
    CAT_WINDOW = (375, 422)
    CAT_BIRD = (578, 131)  # TODO: нужно ли это после добавления мыши?
    CAT_FRIDGE = (302, 349)


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
    EATING = 'Ест'
    SLEEPING = 'Спит'
    WITH_MOTHER = 'С мамой'
    PLAYING_WITH_OWNER = 'Играет с хозяином'
    SEARCHING = 'Гуляет'
    SUNBEAM = 'Ловит зайчика'


class CatStates(enum.Enum):
    EATING = 'Ест'
    SLEEPING = 'Спит'
    WITH_KITTEN = 'С котёнком'
    PLAYING_WITH_OWNER = 'Играет с хозяином'
    WATCHING_WINDOW = 'Смотрит в окно'
    CATCHING_MOUSE = 'Ловит мышь'
    SEARCHING = 'Гуляет'


class PersonStates(enum.Enum):
    EATING = 'Ест'
    SLEEPING = 'Спит'
    WORKING = 'Работает'
    BUYING_PRODUCTS = 'Покупает продукты'
    PLAYING_WITH_CAT = 'Играет с кошкой'
    PLAYING_WITH_KITTEN = 'Играет с котёнком'
    FEEDING = 'Кормит животных'

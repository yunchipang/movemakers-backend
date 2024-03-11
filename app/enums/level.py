import enum


class Level(enum.Enum):
    BEGINNER = "Beg"
    BEGINNER_OR_INTERMEDIATE = "Beg/Int"
    INTERMEDIATE = "Int"
    INTERMEDIATE_OR_ADVANCED = "Int/Adv"
    ADVANCED = "Adv"
    ALL_LEVELS = "All Levels"

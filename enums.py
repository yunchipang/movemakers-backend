from enum import Enum


class Level(Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"
    all_levels = "All Levels"

class Role(Enum):
    instructor = "instructor"
    choreographer = "choreographer"
    director = "director"
    owner = "owner"
    member = "member"

class Style(Enum):
    hip_hop = "Hip Hop"
    contemporary = "Contemporary"
    jazz_funk = "Jazz Funk"
    afro = "Afro"
    dancehall = "Dancehall"
    heels = "Heels"
    reggaeton = "Reggaetón"
    k_pop = "K-Pop"

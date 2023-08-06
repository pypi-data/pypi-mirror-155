import random

from .print_pause import print_pause

DEATHS = [
    "Something utterly bad stabs you in the back. You died!",
    "A strange figure grabs you and kills you instantly!",
    "Something from the dark makes you so mad you die!",
]


def random_death():
    print_pause(random.choice(DEATHS), 3)

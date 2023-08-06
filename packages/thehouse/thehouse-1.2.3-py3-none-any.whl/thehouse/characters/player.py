import random

from helpers.print_pause import print_pause


class Player:
    def __init__(self):
        self.max_health = random.randint(5, 10)
        self.health = self.max_health
        self.escaped = False

    def loose_health(self):
        self.health -= 1
        health = "*" * self.health
        pt_lost = "-" * (self.max_health - self.health)
        print_pause(f"Health: {health}{pt_lost}")

    def is_alive(self):
        return True if self.health > 0 else False

    def escape_the_house(self):
        self.escaped = True

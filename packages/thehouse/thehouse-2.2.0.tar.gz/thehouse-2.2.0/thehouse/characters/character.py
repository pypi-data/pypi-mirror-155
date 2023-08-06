import random

from thehouse.helpers import print_pause


class Character:
    def __init__(self):
        self.max_health = random.randint(5, 10)
        self.health = self.max_health

    def is_alive(self):
        return True if self.health > 0 else False

    def loose_health(self, damage=1):
        self.health -= damage
        self.print_health()

    def restore_health(self):
        self.health = self.max_health
        self.print_health()

    def print_health(self):
        health = "*" * self.health
        pt_lost = "-" * (self.max_health - self.health)
        print_pause(f"Health: {health}{pt_lost}")

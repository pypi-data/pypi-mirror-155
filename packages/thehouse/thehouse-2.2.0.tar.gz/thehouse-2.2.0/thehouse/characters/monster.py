import random

from .character import Character


class Monster(Character):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def deals_damage(self):
        damage = random.randint(1, 2)

        self.player.loose_health(damage)

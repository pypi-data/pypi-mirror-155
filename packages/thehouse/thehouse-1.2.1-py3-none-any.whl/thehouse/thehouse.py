import random

import rooms
from helpers import print_pause, random_death


class TheHouse:
    def __init__(self, player):
        self.player = player
        self.rooms = {
            "studio": rooms.Studio(self.player),
            # "hallway": rooms.Hallway(),
        }
        self.current_room = random.choice(list(self.rooms.keys()))

    def play_game(self):
        while not self.player.escaped or self.player.is_alive():
            print_pause("=== THE HOUSE ===\n\n", 3)

            print_pause("You open your eyes and find yourself lying on the floor")
            print_pause("Your head is pounding and it hurts")
            print_pause("With a lot of effort you stand up")

            self.rooms[self.current_room].center()

            if not self.player.is_alive():
                random_death()
                break

            if self.player.escaped:
                print("Congratulations! You beat the game!")
                break

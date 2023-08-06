import random

from thehouse import rooms
from thehouse.helpers import print_pause, random_death


class TheHouse:
    def __init__(self, player):
        self.player = player
        self.rooms = {
            "studio": rooms.Studio(self.player, self),
            "hallway": rooms.Hallway(self.player, self),
            "hall": rooms.Hall(self.player, self),
            "bedroom": rooms.Bedroom(self.player, self),
            "livingroom": rooms.Livingroom(self.player, self),
            "kitchen": rooms.Kitchen(self.player, self),
            "diningroom": rooms.Diningroom(self.player, self),
        }
        self.current_room = random.choice(list(self.rooms.keys()))

    def play_game(self):
        while not self.player.escaped or self.player.is_alive():
            print_pause("\n\n=== THE HOUSE ===\n\n", 3)

            print_pause("Someone, or something hit you and you faint.")
            print_pause(
                "You hear that this someone or something drags you to someplace.\n", 3
            )
            print_pause("You open your eyes and find yourself lying on the floor.")
            print_pause("Your head is pounding and it hurts.")
            print_pause("With a lot of effort you stand up.")

            self.rooms[self.current_room].center()

            if not self.player.is_alive():
                random_death()
                print_pause("\n=== GAME OVER ===\n", 3)
                break

            if self.player.escaped:
                print("\nCongratulations! You beat the game!\n")
                break

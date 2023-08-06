from helpers.print_pause import print_pause
from .room import Room


class Bedroom(Room):
    def center(self):
        print_pause("You're in the bedroom!")

        self.move()

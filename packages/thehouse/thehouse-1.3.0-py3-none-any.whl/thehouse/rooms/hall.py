from .room import Room
from helpers import print_pause


class Hall(Room):
    def center(self):
        print_pause("You're in the hall!")
        print_pause("In front of you there's the main door of the house.")
        print_pause("Backwards there's the hallway.")
        # on the left
        # on the right

        self.move()

    """ BACKWARD """

    def backward(self):
        self.thehouse.rooms["hallway"].center()

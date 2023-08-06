from helpers import print_pause

from .room import Room


class Hallway(Room):
    def center(self):
        print_pause("You are in the hallway.")
        print_pause("In front of you there's the hall of the house.")
        print_pause("On your right there's a little table and a door.")
        print_pause("Behind you there's a door.")
        print_pause("On your left there's a door and two paintings.")

        self.move()

    """ BACKWARD """

    def backward(self):
        studio = self.thehouse.rooms["studio"]

        if studio.door_locked:
            print_pause("The door is locked!")
            print_pause("It seems you have to find the key!")
            print_pause("You go back.")

            self.move()
        else:
            studio.center()

    """ FORWARD """

    def forward(self):
        self.thehouse.rooms["hall"].center()

    """ RIGHT """

    def right(self):
        self.thehouse.rooms["bedroom"].center()

    """ LEFT """

    def left(self):
        self.thehouse.rooms["livingroom"].center()

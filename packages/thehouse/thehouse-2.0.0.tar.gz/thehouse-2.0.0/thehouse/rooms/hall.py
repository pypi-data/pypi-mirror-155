from helpers import print_pause

from .room import Room


class Hall(Room):
    def center(self):
        print_pause("You're in the hall!")
        print_pause("In front of you there's the main door of the house.")
        print_pause("On your right there's a door.")
        print_pause("Backwards there's the hallway.")
        print_pause("On your left there's another door.")

        self.move()

    """ BACKWARD """

    def backward(self):
        self.thehouse.rooms["hallway"].center()

    """ LEFT """

    def left(self):
        print_pause("You open the door and enter the room")
        self.thehouse.rooms["kitchen"].center()

    """ RIGHT """

    def right(self):
        print_pause("You open the door and enter the room")
        self.thehouse.rooms["diningroom"].center()

    """ FORWARD """

    def forward(self):
        if (
            "thehouse_key_1" in self.player.items
            and "thehouse_key_2" in self.player.items
            and "thehouse_key_3" in self.player.items
        ):
            print_pause("You unlock the door and finally exit the house!")
            self.player.escaped = True
        else:
            print_pause("You need three keys to open the door!")
            print_pause("You go back.")

            self.move()

import random

from helpers import print_pause, validate_input

from .room import Room


class Bedroom(Room):
    def __init__(self, player, thehouse):
        super().__init__(player, thehouse)
        self.key_in_drawer = random.randint(1, 5)

    def center(self):
        print_pause("You're in the bedroom!")
        print_pause("In front of you there's a dresser.")
        print_pause("On your right there's a window.")
        print_pause("Backwards there's a bed.")
        print_pause("On your left there's a door")

        self.move()

    """ LEFT """

    def left(self):
        self.thehouse.rooms["hallway"].center()

    """ BACKWARD """

    def backward(self):
        print_pause("You look tired.")
        print_pause("Do you want to rest a little bit?")

        choice = validate_input("Type yes or no: ", ["yes", "no"])

        if choice == "yes":
            print_pause("You've decided to rest.", 2)
            print_pause(".", 2)
            print_pause(".", 2)
            print_pause(".", 2)
            self.player.restore_health()
        else:
            print_pause("You go back.")

        self.move()

    """ RIGHT """

    def right(self):
        print_pause("You look outside of the window.")
        print_pause("Outside it's pitch black!")
        print_pause("There's something that moves in the darkness")
        print_pause("It's moving so fast that you barely can see it...")
        print_pause("You wonder how could you escape this house")
        print_pause("And if it's safe outside either...", 3)
        print_pause("You go back.")

        self.move()

    """ FORWARD """

    def forward(self):
        print_pause("There are five drawers")
        print_pause("1. open the first")
        print_pause("2. open the second")
        print_pause("3. open the third")
        print_pause("4. open the fourth")
        print_pause("5. open the fifth")

        self.pick_a_drawer()

    def pick_a_drawer(self):
        choice = validate_input(
            "Type a number between 1 and 5 included, or back: ",
            ["1", "2", "3", "4", "5", "back"],
        )

        if choice == "back":
            print_pause("You go back to the center of the room.")
            self.move()
        else:
            print_pause(
                "There's some clothes in it. You dig into them to find something..."
            )

            if int(choice) == self.key_in_drawer:
                if "thehouse_key_1" in self.player.items:
                    print_pause("You've already picked a key from this drawer!")
                    print_pause("There's nothing more in it.")
                else:
                    print_pause("You've found a key!")
                    self.player.pick_an_item("thehouse_key_1")
            else:
                print_pause("There's nothing between the clothes.")
                print_pause("Something from the outside is moving...")
                self.player.loose_health()

            if self.player.is_alive():
                self.pick_a_drawer()

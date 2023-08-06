import random

from thehouse.helpers import print_pause

from .room import Room


class Diningroom(Room):
    def __init__(self, player, thehouse):
        super().__init__(player, thehouse)
        self.key_in_corpse = random.choice(["forward", "left", "backward"])

    def center(self):
        print_pause("You're in the diningroom!")
        print_pause("There's a bloody mess here...")
        print_pause("Someone or something has killed three poeple!")
        print_pause("- Forward there's a corpse!")
        print_pause("- On your right there's another corpse!")
        print_pause("- On your back there's a third corpse!")
        print_pause("- On your left there's a door.")
        print_pause("Maybe you can check the pockets of the corpses!")

        self.move()

    """ FORWARD """

    def forward(self):
        print_pause("Something has smashed its head!")
        print_pause("There's a lot of blood and a strange material on the corpse")
        print_pause("You check its pockets")

        if self.key_in_corpse == "forward":
            if "thehouse_key_2" in self.player.items:
                print_pause("You already checked its pocket and found a key!")
                print_pause("You go back!")
            else:
                print_pause("You have found a key!")
                self.player.pick_an_item("thehouse_key_2")
                print_pause("You pick the key and go back.")
        else:
            print_pause("There's nothing inside its pocket. You go back.")

        self.move()

    """ RIGHT """

    def right(self):
        print_pause("Something has ripped its arms off!")
        print_pause("You check its pocket")

        if self.key_in_corpse == "left":
            if "thehouse_key_2" in self.player.items:
                print_pause("You already checked its pocket and found a key!")
                print_pause("You go back!")
            else:
                print_pause("You have found a key!")
                self.player.pick_an_item("thehouse_key_2")
                print_pause("You pick the key and go back.")
        else:
            print_pause("There's nothing inside its pocket. You go back.")

        self.move()

    """ BACKWARD """

    def backward(self):
        print_pause("There's a huge hole inside the chest of the corpse.")
        print_pause("Something has ripped its heart off!")
        print_pause("You check its pocket")

        if self.key_in_corpse == "backward":
            if "thehouse_key_2" in self.player.items:
                print_pause("You already checked its pocket and found a key!")
                print_pause("You go back!")
            else:
                print_pause("You have found a key!")
                self.player.pick_an_item("thehouse_key_2")
                print_pause("You pick the key and go back.")
        else:
            print_pause("There's nothing inside its pocket. You go back.")

        self.move()

    """ LEFT """

    def left(self):
        print_pause("You open the door and enter the room.")
        self.thehouse.rooms["hall"].center()

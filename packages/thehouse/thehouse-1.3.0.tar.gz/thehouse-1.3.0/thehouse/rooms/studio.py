import random

from helpers import print_pause, validate_input

from .room import Room


class Studio(Room):
    def __init__(self, player, thehouse):
        super().__init__(player, thehouse)
        self.lights = random.choice([True, False])
        self.door_locked = True
        self.key_in_book = random.randint(1, 3)

    def prompt_light(self):
        switch_position = random.choice(["right", "left", "forward", "backward"])

        print_pause("You hear something lurking in the dark")
        print_pause("You defenetly want to turn the lights on.")
        print_pause("You extend your arms to:")
        print_pause("- the right")
        print_pause("- the left")
        print_pause("- forward")
        print_pause("- backward")

        while self.player.health > 0:
            choice = validate_input(
                "Type right, left, forward or backward: ",
                ["right", "left", "backward", "forward"],
            )

            if choice == switch_position:
                print_pause("You've turned the lights on!")
                break
            else:
                print_pause("There's nothing here!")
                print_pause(
                    "But you sense there's something " "that want to reach your hand..."
                )
                self.player.loose_health()

    """ CENTER """

    def center(self):
        lights = "on" if self.lights else "off"

        print_pause(f"You find yourself in a room with the lights {lights}")

        if not self.lights:
            self.prompt_light()

        if self.player.is_alive():
            print_pause("You're in the middle of a studio")
            print_pause("Behind you there's a desk with some papers on it.")
            print_pause("On your left there's a shelf with many books on it.")
            print_pause("On your right there's a window.")
            print_pause("In front of you there's a closed door.")

            self.move()

    """ BACKWARD """

    def backward(self):
        print_pause("On your back there's a window.")
        print_pause("You have a glimpse outside but it's pitch black.")
        print_pause("You can't see anything interesting here.")
        print_pause("You go back.")
        self.move()

    """ RIGHT """

    def right(self):
        print_pause("The desk is so full of papers")
        print_pause("There's nothing particular here. You go back.")
        self.move()

    """ LEFT """

    def left(self):
        print_pause("On your left there's a shelf full of books.")
        print_pause(
            "You run your finger through the dusty books "
            "and rapidly read the titles."
        )
        print_pause("There are so many books in this shelf.")
        print_pause("You wonder yourself if you've ever read this amount of books")

        self.pick_a_book()

    def book_divine_comedy(self):
        if self.key_in_book == 1:
            if "key_studio" not in self.player.items:
                self.pick_the_key()

        print_pause("Amor, ch’a nullo amato amar perdona,")
        print_pause("mi prese del costui piacer sì forte,")
        print_pause("che, come vedi, ancor non m’abbandona")

    def book_the_king_in_yellow(self):
        if self.key_in_book == 2:
            if "key_studio" not in self.player.items:
                self.pick_the_key()

        print_pause("for I knew that the King in Yellow")
        print_pause("had opened his tattered mantle")
        print_pause("and there was only God to cry to now.")

    def book_arkhams_secrets(self):
        if self.key_in_book == 3:
            if "key_studio" not in self.player.items:
                self.pick_the_key()

        print_pause("West of Arkham the hills rise wild,")
        print_pause("and there are valleys with deep")
        print_pause("woods that no axe has ever cut.")

    def pick_the_key(self):
        print_pause("You open the book and a key fall onto the ground.")
        print_pause("You pick the key.")
        self.player.pick_an_item("key_studio")
        self.pick_a_book()

    def pick_a_book(self):
        print_pause("You pick a book:")
        print_pause("1. Divine Comedy")
        print_pause("2. The King in Yellow")
        print_pause("3. Arkham's Secrets")

        choice = validate_input("Type 1, 2, 3, or back: ", ["1", "2", "3", "back"])

        if choice == "1":
            self.book_divine_comedy()
            self.pick_a_book()
        elif choice == "2":
            self.book_the_king_in_yellow()
            self.pick_a_book()
        elif choice == "3":
            self.book_arkhams_secrets()
        elif choice == "back":
            self.move()

    """ FORWARD """

    def forward(self):
        if not self.door_locked:
            self.thehouse.rooms["hallway"].center()
        else:
            print_pause("There's a closed door in front of you")
            print_pause("Do you want to try open it?")

            choice = validate_input("Type yes or no: ", ["yes", "no"])

            if choice == "yes":
                if "key_studio" in self.player.items:
                    self.door_locked = False
                    print_pause("You use the key to unlock the door")
                    print_pause("You exit the studio.")
                    self.thehouse.rooms["hallway"].center()
                else:
                    print_pause("The door is loked.")
                    print_pause("It seems you need a key to open it!")
                    print_pause("You go back.")
                    self.move()
            else:
                print_pause("You hear something from the other side of the door!")
                print_pause("You instantly go back!")
                self.player.loose_health()

                if self.player.is_alive():
                    self.move()

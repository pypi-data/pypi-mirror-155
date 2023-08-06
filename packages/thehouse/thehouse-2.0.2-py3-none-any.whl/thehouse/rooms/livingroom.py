import random

from characters import Monster
from helpers import print_pause, validate_input

from .room import Room


class Livingroom(Room):
    def __init__(self, player, thehouse):
        super().__init__(player, thehouse)
        self.monster = Monster(self.player)
        self.tries = random.randint(3, 6)
        self.safe_open = False
        self.safe_combination = random.randint(1, 5)

    def center(self):
        if self.monster.is_alive():
            print_pause("There's a terrible monster!")
            print_pause("It's half human and half something undescribable!")
            print_pause(
                "Luckly it's slow, but one of its sort of tentacle tries to grab you!"
            )
            self.fight_or_escape()
        else:
            print_pause("You're in the livingroom!")
            print_pause("- In front of you there's a painting.")
            print_pause("- On your right there's a door.")
            print_pause("- On your back there's a window.")
            print_pause("- On your left there's another window.")

            self.move()

    def fight_or_escape(self):
        print_pause("Do you want to fight or escape?")
        choice = validate_input("Type fight or escape: ", ["fight", "escape"])

        if choice == "fight":
            self.fight()
        else:
            self.escape()

    def fight(self):
        while self.monster.is_alive():
            print_pause("It's your turn to deal damages!")

            if "knife" not in self.player.items:
                damage = 1
                print_pause("It seems like you need something to deal more damages!")
            else:
                damage = random.randint(2, 4)

            print_pause(f"You deal {damage} damage.")
            self.monster.loose_health(damage)

            if self.monster.is_alive():
                print_pause("It's the monster's turn to deal damages!")
                self.monster.deals_damage()

                if not self.player.is_alive():
                    break
                else:
                    choice = validate_input(
                        "Type fight or escape: ", ["fight", "escape"]
                    )

                    if choice == "fight":
                        self.fight()
                        break
                    else:
                        self.escape()
                        break
            else:
                print_pause("You successfully killed the monster!")
                self.center()

    def escape(self):
        print_pause("You're trying to escape the monster!")

        choice = validate_input(
            "Type a number between 1 and 6 included: ", ["1", "2", "3", "4", "5", "6"]
        )

        if int(choice) == random.randint(1, 6):
            print_pause("You successfully escaped the moster!!")
            self.thehouse.rooms["hallway"].center()
        else:
            print_pause("You panic and can't escape the fight!")
            self.tries -= 1

            if self.tries <= 0:
                print_pause("The monster reached you!")
                self.monster.deals_damage()
                self.tries = random.randint(3, 6)

            self.fight_or_escape()

    """ RIGHT """

    def right(self):
        print_pause("You open the door and enter the room.")
        self.thehouse.rooms["hallway"].center()

    """ BACK """

    def backward(self):
        print_pause("There's a window and you look outside!")
        print_pause("There's a car! Maybe you can use it to run away from this house!")
        print_pause("You go back.")

        self.move()

    """ LEFT """

    def left(self):
        print_pause("There's a balcony!")
        print_pause("Outside there's a garden.")
        print_pause("The low lights make the garden look like a bleak place.")
        print_pause("You go back.")

        self.move()

    """ FORWARD """

    def forward(self):
        if self.safe_open:
            print_pause("You opened the safe already and picked a key.")
            print_pause("You go back.")
        else:
            print_pause("There's a painting...")
            print_pause("You look closely and there's something behind it!")
            print_pause("You move the painting and reveal a safe!")
            print_pause("Maybe you can break open it!")

            self.break_open()

    def break_open(self):
        print_pause("You need a combination!")

        choice = validate_input(
            "Pick a number between 1 and 5 included: ",
            ["1", "2", "3", "4", "5", "back"],
        )

        if choice == "back":
            self.center()
        else:
            if int(choice) == self.safe_combination:
                print_pause("You successfully opened the safe!")
                print_pause("Inside there's a key!")
                print_pause("You pick the key and go back!")
                self.player.pick_an_item("thehouse_key_3")
                self.safe_open = True

                self.move()
            else:
                print_pause("The combination is wrong! Try again!")
                self.break_open()

import characters
from helpers import print_pause, validate_input

import thehouse


def play():
    player = characters.Player()
    house = thehouse.TheHouse(player)

    house.play_game()

    print_pause("Do you want to play again?")
    choice = validate_input("Type yes or no: ", ["yes", "no"])

    if choice == "yes":
        play()
    else:
        quit()


if __name__ == "__main__":
    play()

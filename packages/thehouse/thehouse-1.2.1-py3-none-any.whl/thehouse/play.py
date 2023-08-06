from characters import Player
from helpers import print_pause, validate_input

from thehouse import TheHouse


def play():
    player = Player()
    thehouse = TheHouse(player)

    thehouse.play_game()

    print_pause("Do you want to play again?")
    choice = validate_input("Type yes or no: ", ["yes", "no"])

    if choice == "yes":
        play()
    else:
        quit()

from thehouse.characters import Player
from thehouse.helpers import print_pause, validate_input
from thehouse.thehouse import TheHouse


def play():
    player = Player()
    house = TheHouse(player)

    house.play_game()

    print_pause("Do you want to play again?")
    choice = validate_input("Type yes or no: ", ["yes", "no"])

    if choice == "yes":
        play()
    else:
        quit()

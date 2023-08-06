from thehouse.helpers import print_pause, validate_input


class Room:
    def __init__(self, player, thehouse):
        self.player = player
        self.thehouse = thehouse

    def right(self):
        pass

    def left(self):
        pass

    def backward(self):
        pass

    def forward(self):
        pass

    def move(self):
        print_pause("Where do you want to go?")

        choice = validate_input(
            'Type "forward", "right", "backward", "left": ',
            ["right", "left", "forward", "backward"],
        )

        if choice == "right":
            self.right()
        elif choice == "left":
            self.left()
        elif choice == "backward":
            self.backward()
        elif choice == "forward":
            self.forward()

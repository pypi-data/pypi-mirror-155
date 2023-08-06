def validate_input(prompt, options):
    while True:
        option = input(prompt).lower()

        if option in options:
            return option

        print("Sorry, I didn't understand! Try Again!")

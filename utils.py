def show_title(title):
    """Display a formatted title."""
    print()
    print("=" * 50)
    print(title.center(50))
    print("=" * 50)


def pause():
    """Pause the game until the user presses Enter."""
    input("\nPress Enter to continue...")


def get_choice(message, valid_choices):
    """
    Get a valid choice from the user.

    valid_choices should be a list of accepted strings.
    """

    while True:
        choice = input(message).strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Please try again.")

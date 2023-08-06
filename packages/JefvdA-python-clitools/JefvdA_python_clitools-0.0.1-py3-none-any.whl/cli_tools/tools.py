import os


def clear():
    """Method to clear the cli, is OS independant"""
    command = 'clear' # If Machine is running on Unix, use clear
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def wait_for_enter():
    """Method to wait for a keypress, also prints message to user 'Press enter to continue...'.
    After keypress, clear the cli."""
    input("Press enter to continue...")
    clear()


def get_user_input(message: str):
    """Method to ask for user input, but uses following format:
    'What is your name? >>> '"""
    return input(f"{message} >>>")

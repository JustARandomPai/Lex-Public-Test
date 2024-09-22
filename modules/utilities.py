import itertools
import os
import time
from . import colors as bcolors

def debug_print(message):
    print(f"[DEBUG] {message}")

def user_prompt(config):
    config = config["settings"]
    try:
        names_input = input(f"Enter the number of valid usernames to find (current: {config['targetValidNames']}): ")
        config['targetValidNames'] = int(names_input) if names_input else config['targetValidNames']

        length_input = input(f"Enter the length of usernames (current: {config['length']}): ")
        config['length'] = int(length_input) if length_input else config['length']

        include_numbers = input(f"Include numbers in usernames? (yes/no, current: {'yes' if config['includeNumbers'] else 'no'}): ").strip().lower()
        config['includeNumbers'] = include_numbers in ['yes', 'y']
    except (ValueError, KeyError) as e:
        if e.__class__.__name__ == 'ValueError':
            print("Invalid input detected. Please enter numeric values where applicable.")
        else:
            print(f"Invalid configuration. {config}")
        

def display_menu(config):
    os.system('cls' if os.name == 'nt' else 'clear')
    config = config["settings"]
    try:
        print(f"{bcolors.HEADER}{bcolors.BOLD}")
        print("  ================================")
        print("      USERNAME VALIDATOR TOOL     ")
        print("  ================================")
        print("                Lex           ")
        print("  ================================")
        print(f"{bcolors.ENDC}")
        print(f"{bcolors.BOLD}==================================={bcolors.ENDC}")
        print(f"Target valid usernames: {config['targetValidNames']}")
        print(f"Length of usernames: {config['length']}")
        print(f"Include numbers: {'Yes' if config['includeNumbers'] else 'No'}")
    except KeyError:
        print(f"Invalid configuration. {config}")

def spinner_animation(duration=5):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    print("Loading configuration...", end="")
    
    for _ in range(duration * 2):
        print(f"\rLoading configuration... {next(spinner)}", end="")
        time.sleep(0.25)
    print("\r{' ' * 30}", end="")

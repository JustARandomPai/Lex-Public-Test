import asyncio
import logging
from modules.config_loader import load_config
from modules.username_generator import find_usernames, display_summary, reset_counters
from modules.utilities import user_prompt, display_menu, spinner_animation


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def main():
    config = load_config("./config.json")

    while True:
        display_menu(config)
        
        user_prompt(config)
        reset_counters()
        
        valid_usernames = await find_usernames(config)
        
        # Animation
        spinner_animation(duration=5)

        display_summary(valid_usernames, config)

        change_settings = input("Do you want to change the amount of usernames or the length of the usernames? (yes/no): ").strip().lower()
        if change_settings in ['yes', 'y']:
            config = load_config("./config.json")
        else:
            print("\n")

        exit_choice = input("Do you want to exit? (yes/no): ").strip().lower()
        if exit_choice in ['yes', 'y']:
            print("Exiting...")
            break
        else:
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
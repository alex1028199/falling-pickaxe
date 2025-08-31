import threading
import time
import random
import main

mock_message = {
    "timestamp": "2024-01-01 12:00:00",
    "author": "test_user",
    "message": "tnt",
    "sc_details": None,
    "ss_details": None,
    "channel_id": "test_channel_id",
    "pfp_url": "https://yt3.ggpht.com/ytc/AAUvwni-JyA8sT5r-p_Yda1Z-p_y_T6z_X_Jz_Z-p=s88-c-k-c0x00ffffff-no-rj"
}

def run_game():
    main.game()

def test_game():
    # Start the game in a separate thread
    game_thread = threading.Thread(target=run_game)
    game_thread.start()

    # Let the game run for a bit
    time.sleep(5)

    # List of commands to test
    commands = [
        "tnt", "fast", "slow", "big", "wood", "stone", "iron", "gold", "diamond", "netherite"
    ]

    start_time = time.time()
    # Run for 2 minutes
    while time.time() - start_time < 120:
        command = random.choice(commands)
        author = "test_user"

        if command == "tnt":
            main.tnt_queue.append(mock_message)
        elif command == "fast":
            main.fast_slow_queue.append((author, "Fast"))
        elif command == "slow":
            main.fast_slow_queue.append((author, "Slow"))
        elif command == "big":
            main.big_queue.append(author)
        elif command in ["wood", "stone", "iron", "gold", "diamond", "netherite"]:
            pickaxe_name = command
            if command == "wood":
                pickaxe_name = "wooden"
            elif command == "gold":
                pickaxe_name = "golden"
            main.pickaxe_queue.append((author, f"{pickaxe_name}_pickaxe"))

        print(f"Executing command: {command}")
        time.sleep(random.uniform(1, 5)) # random interval between commands

    # Stop the game
    main.game_running = False
    print("Stopping game...")

    # Wait for the game thread to finish
    game_thread.join()
    print("Game stopped.")

if __name__ == "__main__":
    test_game()

import time
import keyboard
from python_imagesearch import imagesearch
import tkinter as tk
from threading import Thread
import pygetwindow as gw

# Global variables
running = False
selected_window = None

def move_player(direction):
    # Implement your player movement logic based on the direction (W, A, S, D)
    # You might need to replace the following line with the actual code for moving your player.
    keyboard.press(direction)
    time.sleep(0.1)  # Adjust the sleep time based on your game's responsiveness
    keyboard.release(direction)

def kill_wolf():
    # Implement your logic to kill the wolf using the space bar.
    # You might need to replace the following line with the actual code for killing the wolf.
    keyboard.press('space')
    time.sleep(0.1)  # Adjust the sleep time based on your game's responsiveness
    keyboard.release('space')

def collect_items():
    # Implement your logic to collect items using the 'Z' key.
    # You might need to replace the following line with the actual code for collecting items.
    keyboard.press('z')
    time.sleep(0.1)  # Adjust the sleep time based on your game's responsiveness
    keyboard.release('z')

def main_loop():
    global running
    global selected_window

    while running:
        try:
            if selected_window is not None:
                if selected_window.isMinimized:
                    selected_window.restore()

                selected_window.activate()

                # Search for the wolf image
                resim = imagesearch.imagesearch("lvl3wolf.png")

                if resim[0] != -1:
                    # Wolf detected, get its coordinates
                    wolf_x, wolf_y = resim
                    player_x, player_y = imagesearch.imagesearch("player.png")  # Replace with player image

                    # Check if the player is close to the wolf
                    distance_threshold = 50  # Adjust as needed
                    if abs(player_x - wolf_x) < distance_threshold and abs(player_y - wolf_y) < distance_threshold:
                        # Player is close to the wolf, kill it and collect items
                        kill_wolf()
                        collect_items()
                    else:
                        # Move player towards the wolf
                        if player_x < wolf_x:
                            move_player('d')  # Move right
                        else:
                            move_player('a')  # Move left

                        if player_y < wolf_y:
                            move_player('s')  # Move down
                        else:
                            move_player('w')  # Move up
                else:
                    # No wolf detected, stop moving
                    keyboard.release('w')
                    keyboard.release('a')
                    keyboard.release('s')
                    keyboard.release('d')
        except gw.PyGetWindowException as e:
            # Handle the exception (e.g., window not found, unable to activate)
            print(f"Error: {e}")

        time.sleep(0.1)

def start_stop_script():
    global running
    global selected_window

    if running:
        running = False
        start_stop_button.config(text="Start Script")
    else:
        running = True
        start_stop_button.config(text="Stop Script")
        # Get the currently active window
        selected_window = gw.getActiveWindow()
        print(f"Selected window: {selected_window.title if selected_window else 'None'}")
        # Start a new thread for the main script loop
        script_thread = Thread(target=main_loop)
        script_thread.start()

# GUI setup
root = tk.Tk()
root.title("METİN2")

start_stop_button = tk.Button(root, text="Start Script", command=start_stop_script)
start_stop_button.pack(pady=10)

root.mainloop()

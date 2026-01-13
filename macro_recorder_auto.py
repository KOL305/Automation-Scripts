import pyautogui
import json
import os
import sys
import time
import threading
from pynput import mouse, keyboard

# Define the corner size (in pixels) for the stop condition
CORNER_SIZE = 5

def get_filename():
    """Asks the user for a filename."""
    while True:
        filename = input("Enter output filename (e.g., live_run_1): ").strip()
        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
            # Ensure scripts folder exists
            if not os.path.exists("scripts"):
                os.makedirs("scripts")
            return os.path.join("scripts", filename)
        print("Filename cannot be empty.")

def record_actions():
    print("==========================================")
    print("       PyAutoGUI LIVE Recorder")
    print("==========================================")
    print("INSTRUCTIONS:")
    print("1. The recording starts automatically after a 5-second countdown.")
    print("2. Perform your actions (clicks, keys, drags).")
    print("3. TO STOP: Slam your mouse into any corner of the screen.")
    print("==========================================")

    filename = get_filename()
    
    # Store actions here
    action_list = []
    
    # State variables
    start_time = None
    last_action_time = None
    stop_recording = False
    
    print(f"\nPrepare yourself...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
        
    print(">> RECORDING STARTED! Move to corner to stop. <<")

    # Initialize timing
    start_time = time.time()
    last_action_time = start_time

    def get_delay():
        """Calculates delay since the last action."""
        nonlocal last_action_time
        current_time = time.time()
        delay = current_time - last_action_time
        last_action_time = current_time
        return delay

    def on_move(x, y):
        nonlocal stop_recording
        # check for corner failsafe
        width, height = pyautogui.size()
        if (x <= CORNER_SIZE and y <= CORNER_SIZE) or \
           (x >= width - CORNER_SIZE and y <= CORNER_SIZE) or \
           (x <= CORNER_SIZE and y >= height - CORNER_SIZE) or \
           (x >= width - CORNER_SIZE and y >= height - CORNER_SIZE):
            stop_recording = True
            return False # Stop listener

    def on_click(x, y, button, pressed):
        if stop_recording: return False
        
        action = {
            "type": "mouseDown" if pressed else "mouseUp",
            "button": button.name, # 'left', 'right', 'middle'
            "x": x,
            "y": y,
            "delay": get_delay()
        }
        action_list.append(action)
        state = "Down" if pressed else "Up"
        print(f"Mouse {state}: {button.name} at ({x}, {y})")

    def on_key_action(key, pressed):
        if stop_recording: return False
        
        # Convert pynput key to a string format pydirectinput/pyautogui understands
        key_str = ""
        try:
            key_str = key.char # Regular characters
        except AttributeError:
            # Special keys (Key.space, Key.enter, etc)
            key_str = str(key).replace('Key.', '')

        # Filter out unknown keys or excessive noise if needed
        if not key_str: return

        action = {
            "type": "keyDown" if pressed else "keyUp",
            "key": key_str,
            # We record mouse position even for keys, just in case context matters
            "x": pyautogui.position()[0], 
            "y": pyautogui.position()[1],
            "delay": get_delay()
        }
        action_list.append(action)
        state = "Down" if pressed else "Up"
        print(f"Key {state}: {key_str}")

    def on_press(key):
        on_key_action(key, True)

    def on_release(key):
        on_key_action(key, False)

    # Setup Listeners
    # We suppress=False so the events still go through to the computer while recording
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    mouse_listener.start()
    keyboard_listener.start()

    # Main loop to wait for stop condition
    try:
        while not stop_recording:
            time.sleep(0.1)
            if not mouse_listener.is_alive() or not keyboard_listener.is_alive():
                break
    except KeyboardInterrupt:
        pass
    finally:
        # Ensure listeners are stopped
        if mouse_listener.is_alive(): mouse_listener.stop()
        if keyboard_listener.is_alive(): keyboard_listener.stop()

    print("\nRecording Stopped.")
    
    # Save
    try:
        with open(filename, 'w') as f:
            json.dump(action_list, f, indent=4)
        print(f"Saved {len(action_list)} actions to '{filename}'.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    record_actions()
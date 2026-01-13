import pyautogui
import pydirectinput
import json
import time
import os
import math

# ==========================================
#              CONFIGURATION
# ==========================================

# 1. Define your standard scripts here
# Format: ("filename", action_delay, post_script_delay)
SCRIPTS = [
    ("enter_dark_castle.json", 0.25, 4.0),
    ("menu_okay.json", 0.1, 2.0),
    ("monkey_setup.json", 0.01, 0.0),
    ("end_level.json", 0.25, 4.0)
]

# 2. Configure the Spacer
# This will click the middle of the screen every second for this duration.
SPACER_DURATION = 360  # Total time in seconds
SPACER_LOCATION = 3    # Index to insert spacer (0 is start, 3 is after 3rd script)

# 3. Build the FILES_TO_RUN list dynamically
spacer_entry = [("SPACER", SPACER_DURATION, 1.0)]
FILES_TO_RUN = SCRIPTS[0:SPACER_LOCATION] + spacer_entry + SCRIPTS[SPACER_LOCATION:]

# ========== General Settings ==============
# How many times to repeat the entire sequence
REPEAT_COUNT = 1

# How long it takes for the mouse to move to the target (seconds)
# 0.1 = very fast, 0.0 = instant teleport
MOVE_DURATION = 0.01

# How long to physically hold the button down before releasing (seconds)
# Useful for games that miss clicks if they are too fast.
BUTTON_HOLD_TIME = 0.1
# ==========================================

def run_spacer(duration, interval=1.0):
    """Clicks the middle of the screen every 'interval' seconds for 'duration'."""
    screenWidth, screenHeight = pyautogui.size()
    mid_x, mid_y = screenWidth / 2, screenHeight / 2
    
    print(f"--> Starting Spacer: Clicking center ({mid_x}, {mid_y}) for {duration}s...")
    
    start_time = time.time()
    clicks = 0
    
    while (time.time() - start_time) < duration:
        # Perform click with hold duration
        pyautogui.mouseDown(mid_x, mid_y, button='left')
        time.sleep(BUTTON_HOLD_TIME)
        pyautogui.mouseUp(mid_x, mid_y, button='left')
        
        clicks += 1
        remaining = int(duration - (time.time() - start_time))
        print(f"    [Spacer] Click {clicks} | Time remaining: {remaining}s", end='\r')
        time.sleep(interval)
    
    print(f"\n    [Spacer] Finished. Total clicks: {clicks}")

def run_script(filename, delay):
    # Ensure scripts are loaded from the scripts directory
    filename = os.path.join("scripts", filename) 
    
    if not os.path.exists(filename):
        print(f"[Error] File not found: {filename}")
        return

    print(f"--> Playing script: {filename} (Action Delay: {delay}s)")
    
    try:
        with open(filename, 'r') as f:
            actions = json.load(f)

        for i, act in enumerate(actions):
            # Move mouse (uses pyautogui for the 'duration' smoothing feature)
            pyautogui.moveTo(act['x'], act['y'], duration=MOVE_DURATION)

            # --- Handle Clicks ---
            if act['type'] == 'click':
                # Keeping pyautogui for clicks as requested, but splitting for hold time
                pyautogui.mouseDown(button=act['button'])
                time.sleep(BUTTON_HOLD_TIME)
                pyautogui.mouseUp(button=act['button'])
                print(f"    ({i+1}/{len(actions)}) Clicked {act['button']}")

            # --- Handle Single Key Press (Using pydirectinput) ---
            elif act['type'] == 'press':
                # Using pydirectinput for better game compatibility
                pydirectinput.keyDown(act['key'])
                time.sleep(BUTTON_HOLD_TIME)
                pydirectinput.keyUp(act['key'])
                print(f"    ({i+1}/{len(actions)}) Pressed key '{act['key']}'")

            # --- Handle Hotkeys (Using pydirectinput) ---
            elif act['type'] == 'hotkey':
                keys = act['keys']
                # pydirectinput requires manual chaining for hotkeys to be reliable
                for k in keys:
                    pydirectinput.keyDown(k)
                
                time.sleep(BUTTON_HOLD_TIME)
                
                # Release in reverse order
                for k in reversed(keys):
                    pydirectinput.keyUp(k)
                    
                print(f"    ({i+1}/{len(actions)}) Hotkey: {' + '.join(keys)}")

            time.sleep(delay)

    except json.JSONDecodeError:
        print(f"[Error] Could not decode JSON in {filename}. Is it corrupted?")
    except Exception as e:
        print(f"[Error] An unexpected error occurred: {e}")

def main():
    # PyDirectInput doesn't have the corner failsafe default, but PyAutoGUI still monitors it.
    pyautogui.FAILSAFE = True
    
    print("=== PyAutoGUI Player ===")
    print(f"Files queued: {len(FILES_TO_RUN)}")
    print("Move your mouse to a corner of the screen to EMERGENCY STOP.")
    print("Starting in 3 seconds...")
    time.sleep(3)

    for loop_index in range(REPEAT_COUNT):
        print(f"\n=== Loop {loop_index + 1} of {REPEAT_COUNT} ===")
        
        for file_index, item in enumerate(FILES_TO_RUN):
            # Default values
            script_delay = 0.5
            post_script_delay = 0.0
            filename = ""

            # Unpack configuration
            if isinstance(item, (tuple, list)):
                filename = item[0]
                if len(item) >= 2:
                    script_delay = item[1] # For spacers, this is DURATION
                if len(item) >= 3:
                    post_script_delay = item[2] # For spacers, this is INTERVAL
            else:
                filename = item

            # CHECK IF THIS IS A SPACER OR A FILE
            if filename == "SPACER":
                run_spacer(duration=script_delay, interval=post_script_delay)
            else:
                # Normal file execution
                run_script(filename, script_delay)
                
                # Run the specific Post-Script Delay (only for normal files)
                if post_script_delay > 0:
                    print(f"    [Post-Script] Waiting {post_script_delay}s specific delay...")
                    time.sleep(post_script_delay)

    print("\nAll tasks completed successfully.")

if __name__ == "__main__":
    main()
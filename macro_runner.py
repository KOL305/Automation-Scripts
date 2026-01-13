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
    ("enter_dark_castle.json", 0.5, 6.0),
    ("menu_okay.json", 0.01, 2.0),
    ("monkey_setup.json", 0.01, 0.0),
    ("end_level.json", 0.5, 5.0)
]

# 2. Configure the Spacer
SPACER_DURATION = 360  # Total time in seconds
SPACER_LOCATION = 3    # Index to insert spacer

# 3. Build the FILES_TO_RUN list dynamically
spacer_entry = [("SPACER", SPACER_DURATION, 1.0)]
FILES_TO_RUN = SCRIPTS[0:SPACER_LOCATION] + spacer_entry + SCRIPTS[SPACER_LOCATION:]

# ========== General Settings ==============
REPEAT_COUNT = 30
MOVE_DURATION = 0.01  # For mouse movements
BUTTON_HOLD_TIME = 0.01 # Only used for Legacy 'click'/'press' commands
# ==========================================

def run_spacer(duration, interval=1.0):
    """Clicks the middle of the screen every 'interval' seconds for 'duration'."""
    screenWidth, screenHeight = pyautogui.size()
    mid_x, mid_y = screenWidth / 2, screenHeight / 2
    
    print(f"--> Starting Spacer: Clicking center ({mid_x}, {mid_y}) for {duration}s...")
    
    start_time = time.time()
    clicks = 0
    
    while (time.time() - start_time) < duration:
        pyautogui.mouseDown(mid_x, mid_y, button='left')
        time.sleep(BUTTON_HOLD_TIME)
        pyautogui.mouseUp(mid_x, mid_y, button='left')
        
        clicks += 1
        remaining = int(duration - (time.time() - start_time))
        print(f"    [Spacer] Click {clicks} | Time remaining: {remaining}s", end='\r')
        time.sleep(interval)
    
    print(f"\n    [Spacer] Finished. Total clicks: {clicks}")

def run_script(filename, default_delay):
    filename = os.path.join("scripts", filename) 
    
    if not os.path.exists(filename):
        print(f"[Error] File not found: {filename}")
        return

    print(f"--> Playing script: {filename}")
    
    try:
        with open(filename, 'r') as f:
            actions = json.load(f)

        for i, act in enumerate(actions):
            # 1. Handle Timing
            # If the action has a recorded 'delay' (from Live Recorder), use it.
            # Otherwise use the default_delay passed from config.
            this_delay = act.get('delay', default_delay)
            
            # Wait BEFORE the action (to match rhythm)
            # Note: Recorder saves "time since last action", so we sleep before executing
            if this_delay > 0:
                time.sleep(this_delay)

            # 2. Handle Mouse Movement
            # We move before clicking/pressing to ensure cursor is there.
            if 'x' in act and 'y' in act:
                 pyautogui.moveTo(act['x'], act['y'], duration=MOVE_DURATION)

            action_type = act['type']

            # --- NEW LIVE RECORDER TYPES (Granular) ---
            if action_type == 'mouseDown':
                pyautogui.mouseDown(button=act['button'])
                print(f"    Mouse Down: {act['button']}")

            elif action_type == 'mouseUp':
                pyautogui.mouseUp(button=act['button'])
                print(f"    Mouse Up: {act['button']}")
            
            elif action_type == 'keyDown':
                key = act['key']
                # pydirectinput mapping adjustments if needed
                if key == 'ctrl_l': key = 'ctrlleft'
                if key == 'ctrl_r': key = 'ctrlright'
                if key == 'alt_l': key = 'altleft'
                if key == 'shift': key = 'shift' 
                
                try:
                    pydirectinput.keyDown(key)
                    print(f"    Key Down: {key}")
                except:
                    # Fallback for keys pydirectinput might not know
                    print(f"    [Warning] Unknown key: {key}")

            elif action_type == 'keyUp':
                key = act['key']
                if key == 'ctrl_l': key = 'ctrlleft'
                if key == 'ctrl_r': key = 'ctrlright'
                if key == 'alt_l': key = 'altleft'
                
                try:
                    pydirectinput.keyUp(key)
                    print(f"    Key Up: {key}")
                except:
                    pass

            # --- OLD LEGACY TYPES (Atomic) ---
            elif action_type == 'click':
                pyautogui.mouseDown(button=act['button'])
                time.sleep(BUTTON_HOLD_TIME)
                pyautogui.mouseUp(button=act['button'])
                print(f"    Clicked {act['button']}")

            elif action_type == 'press':
                pydirectinput.keyDown(act['key'])
                time.sleep(BUTTON_HOLD_TIME)
                pydirectinput.keyUp(act['key'])
                print(f"    Pressed '{act['key']}'")

            elif action_type == 'hotkey':
                keys = act['keys']
                for k in keys: pydirectinput.keyDown(k)
                time.sleep(BUTTON_HOLD_TIME)
                for k in reversed(keys): pydirectinput.keyUp(k)
                print(f"    Hotkey: {' + '.join(keys)}")

    except json.JSONDecodeError:
        print(f"[Error] Could not decode JSON in {filename}.")
    except Exception as e:
        print(f"[Error] An error occurred: {e}")

def main():
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

            if isinstance(item, (tuple, list)):
                filename = item[0]
                if len(item) >= 2: script_delay = item[1]
                if len(item) >= 3: post_script_delay = item[2]
            else:
                filename = item

            if filename == "SPACER":
                run_spacer(duration=script_delay, interval=post_script_delay)
            else:
                run_script(filename, script_delay)
                
                if post_script_delay > 0:
                    print(f"    [Post-Script] Waiting {post_script_delay}s...")
                    time.sleep(post_script_delay)

    print("\nAll tasks completed successfully.")

if __name__ == "__main__":
    main()
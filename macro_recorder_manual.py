import pyautogui
import json
import os
import sys

def record_actions():
    print("==========================================")
    print("       PyAutoGUI Action Recorder")
    print("==========================================")
    print("INSTRUCTIONS:")
    print("1. Move your mouse to the desired position.")
    print("2. Type a command and hit ENTER:")
    print("   'lmb'      -> Left Click")
    print("   'rmb'      -> Right Click")
    print("   'mmb'      -> Middle Click")
    print("   `[key]     -> Ctrl + Key (e.g., `c for Ctrl+C, `v for Ctrl+V)")
    print("   [key]      -> Single Key Press (e.g., 'a', 'enter')")
    print("3. Type 'STOP' to save and exit.")
    print("==========================================")

    while True:
        filename = input("Enter output filename (e.g., login_sequence): ").strip()
        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
            filename = os.path.join("scripts", filename)
            break
        print("Filename cannot be empty.")

    action_list = []
    
    print(f"\nRecording to '{filename}'... (Press Ctrl+C to abort without saving)")

    while True:
        try:
            command = input("Action >> ").strip()
            current_x, current_y = pyautogui.position()
            
            if command.upper() == 'STOP':
                break
            
            # Base action structure
            action = {
                "x": current_x,
                "y": current_y
            }

            # --- MOUSE CLICKS ---
            if command == 'lmb':
                action['type'] = 'click'
                action['button'] = 'left'
                print(f"   [Logged] Left Click @ ({current_x}, {current_y})")
            
            elif command == 'rmb':
                action['type'] = 'click'
                action['button'] = 'right'
                print(f"   [Logged] Right Click @ ({current_x}, {current_y})")

            elif command == 'mmb':
                action['type'] = 'click'
                action['button'] = 'middle'
                print(f"   [Logged] Middle Click @ ({current_x}, {current_y})")
            
            # --- CTRL SHORTCUTS (starts with backtick `) ---
            elif command.startswith('`') and len(command) > 1:
                # Extract the key after the backtick
                actual_key = command[1:] 
                action['type'] = 'hotkey'
                action['keys'] = ['ctrl', actual_key]
                print(f"   [Logged] Hotkey 'Ctrl + {actual_key}' @ ({current_x}, {current_y})")

            # --- REGULAR KEY PRESS ---
            else:
                action['type'] = 'press'
                action['key'] = command
                print(f"   [Logged] Key Press '{command}' @ ({current_x}, {current_y})")

            action_list.append(action)

        except KeyboardInterrupt:
            print("\nRecording aborted by user.")
            sys.exit()

    try:
        with open(filename, 'w') as f:
            json.dump(action_list, f, indent=4)
        print(f"\nSuccess! Saved {len(action_list)} actions to '{filename}'.")
    except Exception as e:
        print(f"\nError saving file: {e}")

if __name__ == "__main__":
    record_actions()
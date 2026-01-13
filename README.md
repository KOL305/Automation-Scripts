### SETTING UP VIRTUAL ENVIRONMENT
```bash
$ python -m venv venv
$ venv/Scripts/activate
$ pip install -r requirements.txt
```

### SETTING UP YOUR MACRO
1. Run `$ python macro_recorder.py` to create a new script
2. Follow the instructions to log key presses and clicks
3. Enter `STOP` in terminal when completed and it will save the script to the /scripts folder

**For a BTD6 xp farm you will typically record 4 scripts:**
1. A script for entering the map from the home screen
2. A script for pressing okay on the "deflation explanation" map
3. A script for setting up your towers and starting the map
4. A script for exiting the level once finished

### CONFIGURING YOUR MACRO RUNNER
At the top of `macro_runner.py` are configurable settings:
- `SCRIPTS` are the list of scripts that you want to run.
- `SPACER_DURATION` is the length of which an optional spacer will be. It will click once every second in the middle of the screen.
- `SPACER_LOCATION` is where the spacer will be inserted into the code using Python list concatenation.
- The `General Settings` tab has more available configuration options.

### RUNNING YOUR MACRO
- Run `$ python macro_runner.py` to run your script.
    - *Note: this script will take full control of your mouse and keyboard so your laptop will be rendered unusable*
- You can always emergency exit the current script by moving your mouse to a corner of your computer, but must `ctrl+c` in VScode to exit the full sequence.

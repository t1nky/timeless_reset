# Description

Python helper for better timing of resets in Domain of Timeless Conflict (Path of Exile)

Can be done without OpenCV (just start with a hotkey, feel free to contribute)

Helping to maximize XP from 5way farming (resets every 7-8 seconds).
To maximize loot, prioritize bosses (Generals) and reset every 10-11sec.

# Configuration

* **Resolution**: Set your resolution in `main.py` (edit `myResolution` variable)
* **Timer**: Change timer by editing `__calc_next_reset` in the `__init__.py` inside of the MonolithTime folder.
  - If you need more time before first reset (for example, to get HH stacks after initiating), increase `firstReset`
  - If you are resetter, you might want to lower `resetDelay` to 7
  - If you run solo, you might want to increase `resetDelay` to 9 or more

# Usage

0. Path of Exile must be in Windowed or Windowed Fullscreen mode
1. Adjust configuration
    - Your resolution
    - Adjust timer if you need to
2. Run `main.py`
3. When you hear a notification, immidiately run towards the monolith to reset and spawn enemies

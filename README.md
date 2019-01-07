# DuckieBot

## Overview

A platform to run python-modes that interact with a wheeled robot called a duckie bot.

## Requirements

|Requirement | Version |
|------------|---------|
|python      | >3.5    |
|pip         | 18.1    |

## Installation

```
pip install git+https://github.com/gregjhansell97/DuckieBot.git
```

## Creating Modes

```python
from duckie_bot import Mode
class Driver(Mode):
    '''
    Default Mode Attributes:
        car (duckie_bot.Car): car controlled by standardized functions
        keys_pressed({str}): set of keys currently pressed down
    '''
    def __init__(self):
        pass # no need to invoke super constructor
    def tick(self):
        # listen for user input and change car speed
        self.car #... DO STUFF
        self.keys_pressed #... DO STUFF
        
    def frame(self, frame):
        pass # return modified frame from camera feed
        
##################################################
# MORE INFORMATION                               #
##################################################
import duckie_bot
help(duckie_bot.Mode)
help(duckie_bot.Car)
```

## Running Modes
To run a single mode from a file:

```bash
duckie mode_1.py
```

To run multiple modes and switch between them:

```bash
duckie *.py
```

To run a package that has modes in it:

```bash
duckie directory_to_package
```
The way that ```duckie``` handles running modes varies. The pi interacts with a motor hat and pysically moves. A computer interacts with a stubbed car that prints out it's actions.

## Notes
- Early versions of pip may work, just have not been tested
- This project has been set up using PyScaffold 3.0.3. For details and usage information on PyScaffold see http://pyscaffold.org/.
- Example mode implementation can be found here: [DuckieBotModes](https://github.com/gregjhansell97/DuckieBotModes)

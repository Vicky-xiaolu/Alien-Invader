"""
Constants for Alien Invaders

This module global constants for the game Alien Invaders. These constants need to be used
in the model, the view, and the controller. As these are spread across multiple modules,
we separate the constants into their own module. This allows all modules to access them.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
import introcs
import sys

### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


### SHIP CONSTANTS ###

# the width of the ship
SHIP_WIDTH    = 44
# the height of the ship
SHIP_HEIGHT   = 44
# the distance of the (bottom of the) ship from the bottom of the screen
SHIP_BOTTOM   = 32
# The number of pixels to move the ship per update
SHIP_MOVEMENT = 5
# The number of lives a ship has
SHIP_LIVES    = 3

# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 100


### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 33
# the height of an alien
ALIEN_HEIGHT  = 33
# the horizontal separation between aliens
ALIEN_H_SEP   = 16
# the vertical separation between aliens
ALIEN_V_SEP   = 16
# the number of horizontal pixels to move an alien
ALIEN_H_WALK  = ALIEN_WIDTH // 4
# the number of vertical pixels to move an alien
ALIEN_V_WALK  = ALIEN_HEIGHT // 2
# The distance of the top alien from the top of the window
ALIEN_CEILING = 100
# the number of rows of aliens, in range 1..10
ALIEN_ROWS     = 5
# the number of aliens per row
ALIENS_IN_ROW  = 12
# the image files for the aliens (bottom to top)
ALIEN_IMAGES   = ('alien-strip1.png','alien-strip2.png','alien-strip3.png')
# the number of seconds (0 < float <= 1) between alien steps
ALIEN_SPEED = 0.7


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 4
# the height of a laser bolt
BOLT_HEIGHT = 16
# the number of pixels to move the bolt per update
BOLT_SPEED  = 10
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5


### GAME CONSTANTS ###

# state before the game has started
STATE_INACTIVE = 0
# state when we are initializing a new wave
STATE_NEWWAVE  = 1
# state when the wave is activated and in play
STATE_ACTIVE   = 2
# state when we are paused between lives
STATE_PAUSED   = 3
# state when we restoring a destroyed ship
STATE_CONTINUE = 4
# state when the game is complete (won or lost)
STATE_COMPLETE = 5
# state when the game continue with higher speed and a new wave of aliens
STATE_AGAIN = 6
# state when the game restart
STATE_RESTART = 7
# state when you are choosing the ship you like
STATE_PREP = 8

### USE COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF ALIENS IN A ROW"""
"""
sys.argv is a list of the command line arguments when you run Python. These
arguments are everything after the word python. So if you start the game typing

    python invaders 3 4 0.5

Python puts ['breakout.py', '3', '4', '0.5'] into sys.argv. Below, we take
advantage of this fact to change the constants ALIEN_ROWS, ALIENS_IN_ROW, and
ALIEN_SPEED.
"""
try:
    rows = int(sys.argv[1])
    if rows >= 1 and rows <= 10:
        ALIEN_ROWS = rows
except:
    pass # Use original value

try:
    perrow = int(sys.argv[2])
    if perrow >= 1 and perrow <= 15:
        ALIENS_IN_ROW = perrow
except:
    pass # Use original value

try:
    speed = float(sys.argv[3])
    if speed > 0 and speed <= 3:
        ALIEN_SPEED = speed
except:
    pass # Use original value

### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY ###

# the maximum number of waves for the aliens[int]
# MAX_NUM_OF_WAVE>=0
MAX_NUM_OF_WAVE = 3
# speed changes for eace new wave
SPD_INCRE_EACH_NEW_WAVE = 0.97
# second wait for the state : STATE_AGAIN
WAIT_SECONDS = 2
# time limited to press the key to change the volume of the sound
TIME_LIMIT_SOUND = 0.5
# the health meter for the barrier
HEALTH_METER = 40
# space between images og Ships
SPACE_IMAGE=200
# the width of the starting ship
PREP_WIDTH  = 100
# the height of the starting ship
RREP_HEIGHT = 100
# the number of ships that player can choose
NUM_SHIPS = 3
# the seperation between ships horizontally
SHIP_H_SEP = 200
# the vertical y value for the ships
SHIP_V_VALUE = 400
#the width of the ships while choosing
SHIP_OPTION_WIDTH = 150
#the length of the shipd while choosing
SHIP_OPTION_HEIGHT = 150
#number of barrier wall
NUM_BARRIER_WALL = 3
#distance between barrier wall
BARRIER_WALL_H_SEP = GAME_WIDTH/(NUM_BARRIER_WALL+1)
#vertical position of the barrier wall
BARRIER_WALL_V = 200
#the width of the barrier BarrierWall
BARRIER_WALL_WIDTH = 80
#height of the barrier wall
BARRIER_WALL_HEIGHT = 50
# the maximum number of bolts to change the frame of the barrierwall
BARRIER_WALL_RESISTANCE = 10

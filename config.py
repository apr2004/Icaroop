# Screen configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700 # The screen ends at pixel 700
FPS = 60
ENV_HEIGHT = 70
FLYING = False
GAME_OVER = False

# Game configuration
INITIAL_SCROLL_SPEED = 4
FLAP_COOLDOWN = 7 # For character animation
GRAVITY = 0.5
LIMIT_VELOCITY = 8
JUMP = -8
ROTATION_ANGLE = -2

# Image path
IMAGE_PATH = 'images/'

# Columns configuration
COLUMN_SCALE = 0.6
COLUMN_GAP = 150
COLUMN_FREQUENCY = 1100  # in milliseconds

# Half of the vertical gap between the top and bottom column, measured from
# the screen's vertical center to each column's inner edge.
COLUMN_GAP_HALF = 118
 
# Random vertical variation applied to the gap's center every time a new
# column pair spawns.
COLUMN_HEIGHT_VARIATION = 100
 
# Scoring / difficulty ramp-up
SCORE_INCREMENT = 1
SPEED_INCREMENT_STEP = 0.1

# Icarus configuration
ICARUS_WIDTH = 105
ICARUS_HEIGHT = 85

# Icarus starting position
ICARUS_START_X = 100
ICARUS_START_Y = SCREEN_HEIGHT // 2

# Typography configuration
FONT_PATH = 'typography/'
SCORE_FONT_SIZE = 40
TITTLE_FONT_SIZE = 80

# --- COLORS (RGB Format) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (245, 130, 50)

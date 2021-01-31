import pygame as pg
TITLE = "game"

WIDTH = int(1080)
HEIGHT = int(600)
FPS = 60
FONT_NAME = "arial"
SPRITESHEET = "BB_V2.png"
# zoom intensity:
MAX_ZOOM_X = 600
MAX_ZOOM_Y = MAX_ZOOM_X * HEIGHT/WIDTH
# parameters for the area between player and side of screen:
Y_ZOOM_PAR = .3
X_ZOOM_PAR = .25



# player properties
PLAYER_SCALE = .3
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40
PLAYER_ACC = .4
PLAYER_FRICTION = -.12
PLAYER_GRAVITY = .5
PLAYER_JUMP = -10
PLAYER_DOUBLE_JUMP = -7.5
KICK_WIDTH = 40
KICK_HEIGHT = 20

# combat stats
PLAYER_KICK_SPEED = 7
KICK_RECOVERY = 600
MAX_DAMAGE_SPEED = 300
DAMAGE_KICKBACK = .3
KICK_TIME = 350
SHOT_RATE = 500
MAX_BLOCK_TIME = 1500
MAX_BLOCK_RATE = 300
DOWN_ATT_ACC = 5

#bullet stats
BULLET_SPEED = 10
BULLET_LIFETIME = 500
BULLET_SIZE = 8


# maps
PLATFORM_LIST = [
    # map 1
    [(0, HEIGHT - 40, WIDTH, 40)],
    # mario map
    [(0, HEIGHT - 75, WIDTH, .1)],
    # test map
    [(0, HEIGHT - 40, WIDTH, .1)]
]

PLATFORM_LIST_SEC = [
                    # map 1
                    [
                        (WIDTH*.1, HEIGHT * .8, WIDTH * .2, 10),
                        (WIDTH*.7, HEIGHT * .8, WIDTH * .2, 10),
                        (WIDTH*.4, HEIGHT * .6, WIDTH * .2, 10),
                        (WIDTH*.1, HEIGHT * .4, WIDTH * .2, 10),
                        (WIDTH*.7, HEIGHT * .4, WIDTH * .2, 10)
                    ],
                    # mario map
                    [
                        (WIDTH*.18, HEIGHT * .74, 130, .10),
                        (WIDTH*.5, HEIGHT * .595, 283, .10)
                    ],
                    # test
                    [
                        (WIDTH*.1, HEIGHT * .78, 130, .10),
                        (WIDTH*.8, HEIGHT * .78, 130, .10),
                        (0, HEIGHT * .6, WIDTH, .10),
                        (.6 * WIDTH, HEIGHT * .315, WIDTH, .10),
                        (.5 * WIDTH, HEIGHT * .350, WIDTH * .1, .10)
                    ]
]


VERT_BOUND_LIST = [(0, 0, 1, HEIGHT),
                   (WIDTH, 0, 1, HEIGHT)]

# health bars
HEALTH_BAR_1 = int(.1 * WIDTH)
HEALTH_BAR_2 = int(.6 * WIDTH)
HEALTH_BAR_WIDTH = int(WIDTH * .33)


# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (169, 169, 169)

BACKGROUND = (83, 213, 233)

# images
BULLET_IMG = "bullet.png"
FOREGROUND_IMGS = ["grid.jpg", 'mario.jpg', 'tpfg.png']
BACKGROUND_IMGS = ['bg.jpg']

# controls:

PLAYER1_SELECT = pg.K_RETURN
PLAYER1_LEFT = pg.K_LEFT
PLAYER1_RIGHT = pg.K_RIGHT
PLAYER1_DOWN = pg.K_DOWN
PLAYER1_JUMP = pg.K_UP
PLAYER1_KICK = pg.K_RSHIFT
PLAYER1_SHOOT = pg.K_RCTRL
PLAYER1_BLOCK = pg.K_SLASH

PLAYER2_LEFT = pg.K_a
PLAYER2_RIGHT = pg.K_d
PLAYER2_DOWN = pg.K_s
PLAYER2_JUMP = pg.K_w
PLAYER2_KICK = pg.K_f
PLAYER2_SHOOT = pg.K_q
PLAYER2_BLOCK = pg.K_r

PLAYER1_CTRLS = [PLAYER1_LEFT, PLAYER1_RIGHT, PLAYER1_DOWN, PLAYER1_JUMP,
                 PLAYER1_KICK, PLAYER1_SHOOT, PLAYER1_BLOCK]

PLAYER2_CTRLS = [PLAYER2_LEFT, PLAYER2_RIGHT, PLAYER2_DOWN, PLAYER2_JUMP,
                 PLAYER2_KICK, PLAYER2_SHOOT, PLAYER2_BLOCK]


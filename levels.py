from main import HEIGHT, WIDTH

PLATFORMS_LVL_0 = [(0, HEIGHT - 40, WIDTH, 40),
                   (WIDTH*.4,HEIGHT * .8, WIDTH * .2, 25)]

PLATFORMS_LVL_1 = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH*.1, HEIGHT * .8, WIDTH * .2, 25),
                 (WIDTH*.7, HEIGHT * .8, WIDTH * .2, 25),
                 (WIDTH*.4, HEIGHT * .6, WIDTH * .2, 25)
                 ]

PLATFORM_LIST = [PLATFORMS_LVL_0, PLATFORMS_LVL_1]

BACKGROUND_LVL_0 = "grid.jpg"
BACKGROUND_LVL_1 = "grid.jpg"

BACKGROUND_LIST = list(BACKGROUND_LVL_0, BACKGROUND_LVL_1)



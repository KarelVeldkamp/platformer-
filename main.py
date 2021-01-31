# platform game
from sprites import *
from os import path
import time


class Game:
    def __init__(self):
        self.running = True
        self.playing = False
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        # variable that keeps track of time since last frame (starts of on a sixtieth)
        self.dt = 1 / 60
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)

        # variables for scaling when zooming in and out:
        self.scaling_factor = 1
        self.scaling_factor = 1
        self.new_left = 0
        self.new_top = 0

        # initial menu state
        self.current_page = 'main_menu'
        self.cursor = 0

        # variables for different levels
        self.background_img = None
        self.current_level = None

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")

        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()


        # load the 'foregrounds' in
        self.foreground_imgs = []
        for i in range(len(FOREGROUND_IMGS)):
            # add image to list and rescale
            self.foreground_imgs.append(pg.image.load(path.join(img_folder, FOREGROUND_IMGS[i])).convert_alpha())
            self.foreground_imgs[i] =  pg.transform.scale(self.foreground_imgs[i], (WIDTH, HEIGHT))

        self.background_imgs = []
        for i in range(len(BACKGROUND_IMGS)):
            # add image to list and rescale
            self.background_imgs.append(pg.image.load(path.join(img_folder, BACKGROUND_IMGS[i])).convert_alpha())

        #load spritesheet image:
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))

    def new(self):
        # start new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.sec_platforms = pg.sprite.Group()
        self.vert_bounds = pg.sprite.Group()
        self.player1 = Player(self, BLACK, PLAYER1_CTRLS, spawn=.25)
        self.player2 = Player(self, YELLOW, PLAYER2_CTRLS, spawn=.75)


        # seperately create opponent variable:
        self.player1.make_opponent(2)
        self.player2.make_opponent(1)

        self.bullets = pg.sprite.Group()
        self.all_sprites.add(self.player1, self.player2)

        # add main platforms
        for platform in PLATFORM_LIST[self.current_level]:
            p = Platform(*platform, self)
            self.all_sprites.add(p)
            self.platforms.add(p)
        # add secondary platforms
        for platform in PLATFORM_LIST_SEC[self.current_level]:
            p = Platform(*platform, self)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.sec_platforms.add(p)
        for bound in VERT_BOUND_LIST:
            b = Platform(*bound,self)
            self.all_sprites.add(b)
            self.vert_bounds.add(b)

        self.run()

    def run(self):
        """ game loop """
        self.playing = True
        self.clock.tick()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 10
            self.events()
            self.update()
            self.draw()

    def update(self):
        """ update """
        # update sprites:
        self.all_sprites.update()

        # check if bullets hit
        bullet_hits_1 = pg.sprite.spritecollide(self.player1, self.bullets, True)
        bullet_hits_2 = pg.sprite.spritecollide(self.player2, self.bullets, True)
        if bullet_hits_1:
            self.player1.damage(10, self.player2.rect)
        if bullet_hits_2:
            self.player2.damage(10, self.player1.rect)

        # keep track of the centre point between the players and their distance (for camera movement)
        self.player_distance = abs(self.player1.pos_unscaled.x - self.player2.pos_unscaled.x)
        self.screen_middle = max(self.player1.pos_unscaled.x, self.player2.pos_unscaled.x) - self.player_distance * .5

    def events(self):
        """ check for keys down/up and initiate/end events"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == self.player1.controls[3]:
                    self.player1.jump()
                if event.key == self.player2.controls[3]:
                    self.player2.jump()
                if event.key == self.player1.controls[4]:
                    self.player1.kick()
                if event.key == self.player2.controls[4]:
                    self.player2.kick()
                if event.key == self.player1.controls[5]:
                    self.player1.shoot()
                if event.key == self.player2.controls[5]:
                    self.player2.shoot()
                if event.key == self.player1.controls[6]:
                    self.player1.block(True)
                if event.key == self.player2.controls[6]:
                    self.player2.block(True)
            if event.type == pg.KEYUP:
                if event.key == self.player1.controls[6]:
                    self.player1.block(False)
                if event.key == self.player2.controls[6]:
                    self.player2.block(False)

    def events_menu(self, current_page, links):
        """handle user input while in menu"""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                # moving cursor
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.cursor += 1
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.cursor -= 1

                # updating current page
                if event.key == PLAYER1_SELECT:
                    for i in range(len(links)):
                        if self.cursor == i:
                            self.current_page = links[i]
                            self.cursor = 0

        # keep cursor within possible range
        self.cursor = self.cursor % len(links)

    def scale(self):
        """ scales the foreground image to appropriate size, based on distance between players """
        min_x = min(self.player1.pos_unscaled.x, self.player2.pos_unscaled.x)
        max_x = max(self.player1.pos_unscaled.x, self.player2.pos_unscaled.x)
        min_y = min(self.player1.pos_unscaled.y, self.player2.pos_unscaled.y)
        max_y = max(self.player1.pos_unscaled.y, self.player2.pos_unscaled.y)

        max_hor_rest = MAX_ZOOM_X * Y_ZOOM_PAR
        max_vert_rest = MAX_ZOOM_Y * X_ZOOM_PAR

        new_width = max_x - min_x + 2 * max_hor_rest
        new_height = max_y - min_y + 2 * max_vert_rest

        if new_width < MAX_ZOOM_X and new_height < MAX_ZOOM_Y:
            new_left = (min_x + max_x)/2 - .5 * MAX_ZOOM_X
            new_top = (min_y + max_y)/2 - .5 * MAX_ZOOM_Y
            new_height = MAX_ZOOM_Y
            new_width = MAX_ZOOM_X
        elif new_width > new_height * WIDTH/HEIGHT:
            new_height = new_width * HEIGHT/WIDTH
            new_left = min_x - max_hor_rest
            new_top = (min_y + max_y) / 2 - .5 * new_height
        else:
            new_width = new_height * WIDTH/HEIGHT
            new_top = min_y - max_vert_rest
            new_left = (min_x + max_x) / 2 - .5 * new_width

        if new_left < 0:
            new_left = 0
        if new_top < 0:
            new_top = 0
        if new_left + new_width > WIDTH:
            new_left -= (new_left + new_width) - WIDTH
        if new_top + new_height > HEIGHT:
            new_top -= (new_top + new_height) - HEIGHT

        # if the players are completely across the screen:
        if new_width > WIDTH:
            new_left = 0
            new_width = WIDTH
            new_top = 0
            new_height = HEIGHT

        #calculate x ofset
        offset_x = (new_left + new_width/2) - WIDTH/2

        bg_mid = 1920/2 + offset_x * .5
        bg_left = bg_mid - WIDTH/2


        # scoll background
        new_background = pg.Surface((1920, HEIGHT))
        new_background.blit(self.background_imgs[0], (0, 0), (bg_left, 0, WIDTH, HEIGHT))

        # scale foreground
        new_foreground = pg.Surface((int(new_width), int(new_height)), pg.SRCALPHA)
        new_foreground.blit(self.background_img, (0, 0), (int(new_left), int(new_top), int(new_width), int(new_height)))
        new_foreground.convert_alpha()



        new_foreground = pg.transform.scale(new_foreground, (WIDTH, HEIGHT))

        self.screen.blit(new_background, (0, 0))
        self.screen.blit(new_foreground, (0, 0))

        # scaling parameters factor used for moving and scaling sprites
        self.scaling_factor = WIDTH / new_width
        self.new_left = new_left
        self.new_top = new_top

    def draw(self):
        """ Draw sprites and background to screen """
        self.scale()

        player = 1
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                sprite.draw_health(player)
                player += 1
        self.all_sprites.draw(self.screen)

        # flip display after drawing everything
        pg.display.flip()

    def draw_text(self, text, size, colour, x, y):
        """ function for drawing text in menus etc """
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (int(x), int(y))
        self.screen.blit(text_surface, text_rect)

    def start_menu(self):
        # initial state
        self.current_page = 'main_menu'

        # menu loop
        while True:
            # main menu page:
            if self.current_page == 'main_menu':
                # list of options
                links = ['select_map', 'settings', 'quit']
                colors = [WHITE, WHITE, WHITE]
                colors[self.cursor] = GREY

                # draw menu
                self.screen.fill(BLACK)
                self.draw_text('main menu', 80, WHITE, WIDTH * .5, HEIGHT * .2)
                self.draw_text('Start', 50, colors[0], WIDTH * .5, HEIGHT * .4)
                self.draw_text('Settings', 50, colors[1], WIDTH * .5, HEIGHT * .5)
                self.draw_text('Quit', 50, colors[2], WIDTH * .5, HEIGHT * .6)

                pg.display.flip()

                # update menu according to user input
                self.events_menu(self, links)

            # map selection page
            if self.current_page == 'select_map':
                links = ['map1', 'map2', 'map3', 'main_menu']
                colors = [WHITE, WHITE, WHITE, WHITE]
                colors[self.cursor] = GREY

                # draw menu
                self.screen.fill(BLACK)
                self.draw_text('Choose a map', 80, WHITE, WIDTH * .5, HEIGHT * .2)
                self.draw_text('Map 1', 50, colors[0], WIDTH * .5, HEIGHT * .4)
                self.draw_text('Map 2', 50, colors[1], WIDTH * .5, HEIGHT * .5)
                self.draw_text('Map 3', 50, colors[2], WIDTH * .5, HEIGHT * .6)
                self.draw_text('Back', 50, colors[3], WIDTH * .5, HEIGHT * .7)

                pg.display.flip()

                self.events_menu(self, links)



            # quit
            if self.current_page == 'quit':
                exit()
            if self.current_page == 'map1':
                self.background_img = self.foreground_imgs[0]
                self.current_level = 0
                break
            if self.current_page == 'map2':
                self.background_img = self.foreground_imgs[1]
                self.current_level = 1
            if self.current_page == 'map3':
                self.background_img = self.foreground_imgs[2]
                self.background_img.convert_alpha()
                self.current_level = 2
                break
                


    def show_game_over(self):
        """ game over screen """
        # make sure the application is still running:
        if not self.running:
            return

        # draw game over screen:
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER!", 60, WHITE, WIDTH / 2, HEIGHT / 4)
        if self.player1.health > 0:
            winner = "player one"
        else:
            winner = "player two"
        self.draw_text(f"{winner} won!", 50, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("press the options button to start another battle", 30, WHITE, WIDTH / 2, HEIGHT * .75)
        pg.display.flip()

        # wait for spacebar/options
        self.wait_for_key(pg.K_SPACE)

    def wait_for_key(self, key=pg.KEYUP):
        """ function that sleeps until key is pressed"""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == key:
                        waiting = False


g = Game()
while g.running:
    g.start_menu()
    g.new()
    g.show_game_over()

pg.quit()
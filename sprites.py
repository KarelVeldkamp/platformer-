# sprite classes for game
from settings import *
import pygame as pg
import math
vec = pg.math.Vector2


class Spritesheet:
    # loading and parsing sprite sheets
    def __init__ (self, filename):

        self.spritesheet = pg.image.load(filename)

    def get_image(self, x, y, width, height):
        # grab image out of sprite sheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (int(width), int(height)))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game, colour, controls, spawn):
        """ Initializing character """
        self.game = game
        pg.sprite.Sprite.__init__(self)

        # state bools
        self.walking = False
        self.kicking = False
        self.damaged = False
        self.blocking = False
        self.falling = False

        # test if player is touching a wall on wither side, and whether they are hanging on a wall
        self.bumping_right = False
        self.bumping_left = False
        self.on_the_wall = False

        # action counters
        self.kicked = False
        self.jumped = 0

        # variable for left-right orientation
        self.facing = 1

        # time variables used for resetting stuff
        self.current_frame = 0
        self.last_update = 0
        self.last_damaged = 0
        self.last_shot = 0
        self.last_block_started = 0
        self.last_block_end = 0
        self.last_kick = 0
        self.last_landing = -1000

        # health
        self.health = 100

        # creating character
        self.load_imgs(colour)
        self.image = self.standing_frame_r
        self.rect = self.image.get_rect()

        self.offensive_hitbox = pg.Rect(-20, -20, 10, 10)
        self.defensive_hitbox = self.rect

        # position, velocity, acceleration and direction
        self.pos = vec(0, 0)
        self.pos_unscaled = vec(WIDTH * spawn, HEIGHT * .4)
        self.vel_unscaled = vec(0, 0)
        self.acc_unscaled = vec(0, 0)

        # player controls
        self.controls = controls

    def make_opponent(self, opp):
        """ create an opponent variable """
        if opp == 1:
            self.opponent = self.game.player1
        if opp == 2:
            self.opponent = self.game.player2

    def load_imgs(self, colour):
        """ load animation images """
        self.standing_frame_r = self.game.spritesheet.get_image(273, 80, 114, 200)
        self.standing_frame_r.set_colorkey(WHITE)

        self.standing_frame_l = pg.transform.flip(self.game.spritesheet.get_image(273, 80, 114, 200), True, False)
        self.standing_frame_l.set_colorkey(WHITE)

        self.walking_frames_r = [self.game.spritesheet.get_image(495, 80, 154, 200),
                                 self.game.spritesheet.get_image(716, 80, 154, 200),
                                 self.game.spritesheet.get_image(959, 75, 154, 212),
                                 self.game.spritesheet.get_image(716, 80, 154, 200)]

        for frame in self.walking_frames_r:
            frame.set_colorkey(WHITE)

        self.walking_frames_l = [pg.transform.flip(self.game.spritesheet.get_image(495, 80, 154, 200), True, False),
                                 pg.transform.flip(self.game.spritesheet.get_image(716, 80, 154, 200), True, False),
                                 pg.transform.flip(self.game.spritesheet.get_image(959, 75, 154, 212), True, False),
                                 pg.transform.flip(self.game.spritesheet.get_image(716, 80, 154, 200), True, False)]

        for frame in self.walking_frames_l:
            frame.set_colorkey(WHITE)

        self.kicking_frame_r = self.game.spritesheet.get_image(755, 330, 178, 215)
        self.kicking_frame_r.set_colorkey(WHITE)

        self.kicking_frame_l = pg.transform.flip(self.game.spritesheet.get_image(755, 330, 178, 215), True, False)
        self.kicking_frame_l.set_colorkey(WHITE)

        self.shooting_frame_r = self.game.spritesheet.get_image(510, 360, 215, 208)
        self.shooting_frame_r.set_colorkey(WHITE)

        self.shooting_frame_l = pg.transform.flip(self.game.spritesheet.get_image(510, 360, 215, 208), True, False)
        self.shooting_frame_l.set_colorkey(WHITE)

        self.jumping_frame_r = self.game.spritesheet.get_image(60, 345, 164, 225)
        self.jumping_frame_r.set_colorkey(WHITE)

        self.jumping_frame_l =  pg.transform.flip(self.game.spritesheet.get_image(60, 345, 170, 225), True, False)
        self.jumping_frame_l.set_colorkey(WHITE)

        self.landing_frame_r = self.game.spritesheet.get_image(285, 388, 117, 177)
        self.landing_frame_r.set_colorkey(WHITE)

        self.landing_frame_l = pg.transform.flip(self.game.spritesheet.get_image(285, 388, 117, 177), True, False)
        self.landing_frame_l.set_colorkey(WHITE)

        self.highkick_frame_r = self.game.spritesheet.get_image(973, 345, 144, 217)
        self.highkick_frame_r.set_colorkey(WHITE)

        self.highkick_frame_l = pg.transform.flip(self.game.spritesheet.get_image(973, 345, 144, 217), True, False)
        self.highkick_frame_l.set_colorkey(WHITE)

    def jump(self):
        """ jump and double jump """
        # jump if standing
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel_unscaled.y = PLAYER_JUMP
            self.jumped = 1
        # double jump if already jumping
        elif not hits and self.jumped == 1:
            self.vel_unscaled.y = PLAYER_DOUBLE_JUMP
            self.jumped = 2

    def kick(self):
        """ A kicking attack """
        # kick if player is not damaged, recovery time has passed and floor has been touched since last kick
        if not self.kicked \
                and pg.time.get_ticks() - self.last_kick > KICK_RECOVERY \
                and not self.damaged:
            if self.facing == +1:
                self.vel_unscaled.x += PLAYER_KICK_SPEED
            if self.facing == -1:
                self.vel_unscaled.x += -PLAYER_KICK_SPEED

            # some extra airtime when you kick
            self.vel_unscaled.y += -3

            # track if player has kicked this jump:
            self.kicked = True
            # track if player is currently kicking
            self.kicking = True
            self.last_kick = pg.time.get_ticks()

    def shoot(self):
        """ shoot a projectile """
        if not self.damaged \
                and pg.time.get_ticks() - self.last_shot > SHOT_RATE \
                and not self.kicking:
            Projectile(self.game, self.pos, self.facing)
            self.last_shot = pg.time.get_ticks()

    def block(self, not_ending):
        """" Block any attacks """
        # if blocking key is pressed:
        pass
        """"
        if not_ending:
            # blocks only if standing, not kicking and not damaged.
            if pg.time.get_ticks() - self.last_block_end > MAX_BLOCK_RATE \
                    and not self.damaged \
                    and not self.kicking\
                    and self.jumped == 0:
                self.blocking = True
                self.last_block_started = pg.time.get_ticks()
        # if blocking key is released:
        if self.blocking and not not_ending:
            self.blocking = False
            self.last_block_end = pg.time.get_ticks()
    """

    def damage(self, damage, damager):
        """ receiving damage """
        if pg.time.get_ticks() - self.last_damaged > MAX_DAMAGE_SPEED \
                and not self.blocking:
            self.health -= damage
            self.damaged = True
            self.last_damaged = pg.time.get_ticks()
            self.vel_unscaled.y -= damage * DAMAGE_KICKBACK

            # same for x axis, but based on hit location and corrected for aspect ratio
            if damager.collidepoint(self.rect.midleft) \
                    or damager.collidepoint(self.rect.topleft) \
                    or damager.collidepoint(self.rect.bottomleft):
                self.vel_unscaled.x += damage * DAMAGE_KICKBACK * (WIDTH/HEIGHT)

            if damager.collidepoint(self.rect.midright) \
                    or damager.collidepoint(self.rect.topright) \
                    or damager.collidepoint(self.rect.bottomright):
                self.vel_unscaled.x -= damage * DAMAGE_KICKBACK * (WIDTH/HEIGHT)

    def update_position(self):
        """ scaling positions """
        self.pos.x = (self.pos_unscaled.x - self.game.new_left) * self.game.scaling_factor
        self.pos.y = (self.pos_unscaled.y - self.game.new_top) * self.game.scaling_factor

    def move(self):
        """" Player movement """
        self.acc_unscaled = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if not self.blocking:
            if keys[self.controls[0]]:
                self.acc_unscaled.x = -PLAYER_ACC
            if keys[self.controls[1]]:
                self.acc_unscaled.x = PLAYER_ACC
            if keys[self.controls[2]]:
                self.falling = True
            else:
                self.falling = False

        # apply friction
        self.acc_unscaled.x += self.vel_unscaled.x * PLAYER_FRICTION
        # equations of motion
        self.vel_unscaled += self.acc_unscaled * self.game.dt

        # stop when hitting a wall
        if self.bumping_left:
            self.vel_unscaled.x = max(0, self.vel_unscaled.x)
            self.acc_unscaled.x = max(0, self.acc_unscaled.x)
        if self.bumping_right:
            self.vel_unscaled.x = min(0, self.vel_unscaled.x)
            self.acc_unscaled.x = min(0, self.acc_unscaled.x)

        # slide down when hitting the wall
        if self.jumped > 0 and (self.bumping_left or self.bumping_right):
            self.vel_unscaled.y = 3
            self.acc_unscaled.y = 0
            self.on_the_wall = True
        else:
            self.on_the_wall = False

        self.pos_unscaled += (self.vel_unscaled + .5 * self.acc_unscaled) * self.game.dt

        if abs(self.vel_unscaled.x) < .1:
            self.vel_unscaled.x = 0

        # set direction
        if self.vel_unscaled.x < 0:
            self.facing = -1
        if self.vel_unscaled.x > 0:
            self.facing = +1

        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos

    def collisions(self):
        """ Handle collision between players, platforms etc. """
        # specifying vulnerable hitboxes and hitboxes for attacks
        if self.kicking and self.facing == +1:
            self.offensive_hitbox = pg.Rect(self.rect.center[0], self.rect.top, KICK_WIDTH * self.game.scaling_factor * .5, KICK_HEIGHT * self.game.scaling_factor)
            self.defensive_hitbox = pg.Rect(self.rect.bottomleft[0], self.rect.top, KICK_WIDTH * self.game.scaling_factor * .5, KICK_HEIGHT * self.game.scaling_factor)
        if self.kicking and self.facing == -1:
            self.offensive_hitbox = pg.Rect(self.rect.bottomleft[0], self.rect.top, KICK_WIDTH * self.game.scaling_factor * .5, KICK_HEIGHT * self.game.scaling_factor)
            self.defensive_hitbox = pg.Rect(self.rect.center[0], self.rect.top, KICK_WIDTH * self.game.scaling_factor * .5, KICK_HEIGHT * self.game.scaling_factor)

        if not self.kicking:
            self.defensive_hitbox = self.rect
            self.offensive_hitbox = pg.Rect(self.pos_unscaled.x, self.pos_unscaled.y-500, 1, 1)

        # falling through and landing on platforms:
        if self.vel_unscaled.y > 0:
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                if not (hits[0] in self.game.sec_platforms and self.falling and self.jumped > 0):
                    self.pos_unscaled.y = hits[0].original_platform[1] + 1
                    # if just landed, note landing:
                    if self.vel_unscaled.y > 5:
                        self.last_landing = pg.time.get_ticks()
                    self.vel_unscaled.y = 0
                    # reset jumps and kicks
                    self.jumped = 0
                    self.kicked = False

        # hitting vertical boundaries:
        hits = pg.sprite.spritecollide(self, self.game.vert_bounds, False)
        if hits:
            if not (self.bumping_right or self.bumping_left):
                if self.vel_unscaled.x < 0:
                    #self.pos_unscaled.x = hits[0].original_platform[0] + 4
                    self.bumping_left = True
                if self.vel_unscaled.x > 0:
                    self.bumping_right = True
                    #self.pos_unscaled.x = hits[0].original_platform[0] - self.rect[2] +4
        else:
            self.bumping_left = self.bumping_right = False



        # hitting a kick:
        if self.kicking and not self.damaged:
            # kick hits vulnerable area:
            hits = pg.Rect.colliderect(self.offensive_hitbox, self.opponent.defensive_hitbox)
            # kick hits other attack
            double_hits = pg.Rect.colliderect(self.offensive_hitbox, self.opponent.offensive_hitbox)
            if hits and not double_hits:
                self.opponent.damage(20, damager=self.rect)
            if double_hits:
                # recoil:
                self.vel_unscaled.x -= self.facing * 10


        # players moving into each other:
        if pg.Rect.colliderect(self.defensive_hitbox, self.opponent.defensive_hitbox):
            minpos = min(self.pos_unscaled.x, self.opponent.pos_unscaled.x)
            maxpos = max(self.pos_unscaled.x, self.opponent.pos_unscaled.x) + PLAYER_WIDTH
            middle = (minpos + maxpos) / 2
            # if you are the left player (and only if players are facing eachother).
            if self.pos_unscaled.x == minpos:
                self.pos_unscaled.x = middle - 35
                self.opponent.pos_unscaled.x = middle
            self.vel_unscaled.x = 0
            self.opponent.vel_unscaled.x = 0

    def update(self):
        """ updating player sprite """
        self.update_position()
        self.animate()
        self.move()
        self.collisions()


        # if player dies
        if self.health <= 0:
            self.game.playing = False

    def animate(self):
        """ animating character """
        now = pg.time.get_ticks()
        if self.vel_unscaled.x != 0 and self.jumped < 1:
            self.walking = True
        else:
            self.walking = False

        if not self.walking and not self.kicking:
            if self.facing == 1:
                self.image = self.standing_frame_r
            else:
                self.image = self.standing_frame_l

        # jumping animation
        if self.jumped > 0:
            if self.facing == 1:
                self.image = self.jumping_frame_r
            else:
                self.image = self.jumping_frame_l

        if self.kicking:
            if now - self.last_kick < KICK_TIME:
                # jump kick animation
                if self.jumped:
                    if self.facing == 1:
                        self.image = self.kicking_frame_r
                    else:
                        self.image = self.kicking_frame_l
                # high (standing) kick animation
                else:
                    if self.facing == 1:
                        self.image = self.highkick_frame_r
                    else:
                        self.image = self.highkick_frame_l

            else:
                self.kicking = False
                if self.facing == 1:
                    self.image = self.standing_frame_r
                else:
                    self.image = self.standing_frame_l
            self.rect = self.image.get_rect()

        if self.damaged:
            if now - self.last_damaged < 200:
                print("damaged")
            else:
                self.damaged = False
                if self.facing == 1:
                    self.image = self.standing_frame_r
                else:
                    self.image = self.standing_frame_l

        if self.blocking:
            if now - self.last_block_started < MAX_BLOCK_TIME:
                self.image = self.blocking_frame
            else:
                self.blocking = False
                self.last_block_end = now

        # walking animation
        if self.walking and not self.kicking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
            bottom = self.rect.bottom
            if self.facing == 1:
                self.image = self.walking_frames_r[self.current_frame]
            else:
                self.image = self.walking_frames_l[self.current_frame]

            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # landing animaton
        if now - self.last_landing < 200:
            if self.facing == 1:
                self.image = self.landing_frame_r
            else:
                self.image = self.landing_frame_l

        # shooting animation
        if now - self.last_shot < 150:
            if self.facing == 1:
                self.image = self.shooting_frame_r
            else:
                self.image = self.shooting_frame_l

        # update animation size for scaling
        size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (int(size[0] * self.game.scaling_factor),
                                                     int(size[1] * self.game.scaling_factor)))

        # make image smaller (here because if resolution)
        size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (int(size[0]*PLAYER_SCALE), int(size[1]*PLAYER_SCALE)))

        # get rekt m8
        self.rect = self.image.get_rect()

    def draw_health(self, player):
        """ draw health bar """
        if self.health > 60:
            colour = GREEN
        elif self.health > 30:
            colour = YELLOW
        else:
            colour = RED

        width = HEALTH_BAR_WIDTH * self.health/100
        if player == 1:
            self.health_bar = pg.Rect(HEALTH_BAR_1, 0, width, 25)
        if player == 2:
            self.health_bar = pg.Rect(HEALTH_BAR_2, 0, width, 25)
        pg.draw.rect(self.game.screen, colour, self.health_bar)


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_platform = (x, y, w, h)

    def update(self):
        """ update platform according to scaling. """
        self.rect.x = (self.original_platform[0] - self.game.new_left) * self.game.scaling_factor
        self.rect.y = (self.original_platform[1] - self.game.new_top) * self.game.scaling_factor
        self.rect.w = self.original_platform[2] * self.game.scaling_factor
        self.rect.h = self.original_platform[3] * self.game.scaling_factor
        self.image = pg.transform.scale(self.image, (int(self.original_platform[2] * self.game.scaling_factor),
                                                     int(self.original_platform[3] * self.game.scaling_factor)))


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, pos, facing):
        self.game = game
        self.groups = self.game.all_sprites, self.game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.scale(game.bullet_img,
                                        (int(BULLET_SIZE * 2 * self.game.scaling_factor), int(BULLET_SIZE * self.game.scaling_factor)))
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        # making sure bullet is shot from middle, and doesnt collide with self
        # (the facing * 10 is because shooting to the right would hit self)
        PLAYER_SHOOTING_WIDTH = 150
        self.pos.y -= 20 * self.game.scaling_factor
        self.pos.x += facing * (self.game.scaling_factor * .5 * PLAYER_SHOOTING_WIDTH)

        self.rect.center = pos
        self.vel = facing * BULLET_SPEED * self.game.scaling_factor
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos.x += self.vel * self.game.dt
        self.rect.center = self.pos

        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()










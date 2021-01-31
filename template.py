import random
import pygame
from settings import *

# initialize pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
# Game loop
running = True
while running:
    #keep loop running at right speed


    # Update
    all_sprites.update()

    # draw/render
    screen.fill(BLACK)
    all.sprites.draw(screen)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()


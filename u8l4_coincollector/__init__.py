import pygame
from datetime import datetime
from random import randint
from fox import Fox
from fox2 import Fox2
from coin import Coin
from bonus_coin import BonusCoin


# set up pygame modules
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("Arial", 15)
pygame.display.set_caption("Coin Collector!")


# set up variables for the display
SCREEN_HEIGHT = 370
SCREEN_WIDTH = 530
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)


name = "Collect coins as fast as you can!"
r = 97
g = 16
b = 162


# render the text for later
display_name = my_font.render(name, True, (255, 255, 255))


f1 = Fox(40, 60, (SCREEN_WIDTH, SCREEN_HEIGHT))
max_sprite_bounds = (SCREEN_WIDTH - f1.image_size[0], SCREEN_HEIGHT - f1.image_size[1])
f1 = Fox(40, 60, max_sprite_bounds)
f2 = Fox2(40, 60, max_sprite_bounds)
c = Coin(200, 85)
bc = BonusCoin(200, 85)


# The loop will carry on until the user exits the game (e.g. clicks the close button).
run = True


# -------- Main Program Loop -----------
p1_score, p2_score = 0, 0
p1_flip, p2_flip = False, False
title_screen = True
two_player = False
while run:
    while title_screen:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                title_screen = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                title_screen = False
                two_player = True
            if event.type == pygame.QUIT:
                run = False
                title_screen = False

        screen.fill((r, g, b))
        title_message = "Coin Snatcher!"
        subtitle_message = "CLICK TO START or [↑] for 2 player mode"
        title_font = pygame.font.SysFont("Arial", 50)
        display_title = title_font.render(title_message, True, (255, 255, 255))
        display_subtitle = my_font.render(subtitle_message, True, (255, 255, 255))
        text_x = (SCREEN_WIDTH - display_title.get_width()) // 2
        text_y = (SCREEN_HEIGHT - display_title.get_height()) // 2
        screen.blit(display_title, (text_x, text_y))
        screen.blit(display_subtitle, (text_x, text_y + display_title.get_height()))
        pygame.display.update()

    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_w]:
        f1.move_direction("up")
    if keys[pygame.K_a]:
        f1.move_direction("left")
        if not p1_flip:
            f1.image = pygame.transform.flip(f1.image, True, False)
            p1_flip = True
    if keys[pygame.K_s]:
        f1.move_direction("down")
    if keys[pygame.K_d]:
        f1.move_direction("right")
        if p1_flip:
            f1.image = pygame.transform.flip(f1.image, True, False)
            p1_flip = False

    if two_player:
        if keys[pygame.K_UP]:
            f2.move_direction("up")
        if keys[pygame.K_LEFT]:
            f2.move_direction("left")
            if not p2_flip:
                f2.image = pygame.transform.flip(f2.image, True, False)
                p2_flip = True
        if keys[pygame.K_DOWN]:
            f2.move_direction("down")
        if keys[pygame.K_RIGHT]:
            f2.move_direction("right")
            if p2_flip:
                f2.image = pygame.transform.flip(f2.image, True, False)
                p2_flip = False
    
    if datetime.now().microsecond % 1000 == 0 and randint(0, 100) == 0:
        bc.new_location(SCREEN_WIDTH, SCREEN_HEIGHT)

    # collision
    if f1.rect.colliderect(c.rect):
        c.new_location(SCREEN_WIDTH, SCREEN_HEIGHT)
        p1_score += 10

    if two_player:
        if f2.rect.colliderect(c.rect):
            c.new_location(SCREEN_WIDTH, SCREEN_HEIGHT)
            p2_score += 10

        display_p2_score = my_font.render(
            f"Player 2: {p2_score}", True, (255, 255, 255)
        )

    display_p1_score = my_font.render(
        f"{'Score' if not two_player else 'Player 1'}: {p1_score}",
        True,
        (255, 255, 255),
    )

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False

    screen.fill((r, g, b))
    screen.blit(display_name, (0, 0))
    screen.blit(display_p1_score, (0, 15))
    screen.blit(c.image, c.rect)
    screen.blit(bc.image, bc.rect)
    screen.blit(f1.image, f1.rect)
    if two_player:
        screen.blit(f2.image, f2.rect)
        screen.blit(display_p2_score, (0, 30))
    pygame.display.update()


# Once we have exited the main program loop we can stop the game engine:
pygame.quit()

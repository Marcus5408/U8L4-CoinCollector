import pygame
from datetime import datetime
from random import randint
from fox import Fox
from coin import Coin
from bonus_coin import BonusCoin
from bomb import Bomb


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


f1 = Fox(40, 60, (SCREEN_WIDTH, SCREEN_HEIGHT), "orange-fox-sprite.png")
max_sprite_bounds = (SCREEN_WIDTH - f1.image_size[0], SCREEN_HEIGHT - f1.image_size[1])
f1 = Fox(40, 60, max_sprite_bounds, "orange-fox-sprite.png")
f2 = Fox(40, 60, max_sprite_bounds, "brown-fox-sprite.png")
c = Coin(200, 85)
bc = BonusCoin(200, 85)
bomb = Bomb(0, -40)


# The loop will carry on until the user exits the game (e.g. clicks the close button).
run = True


# -------- Main Program Loop -----------
try:
    with open(f"{__file__.replace('__init__.py', '')}high_score.txt", "r") as file:
        file_contents = file.read()
        high_score = int(file_contents) if file_contents else 0
except FileNotFoundError:
    # create file if it doesn't exist
    with open(f"{__file__.replace('__init__.py', '')}high_score.txt", "w") as file:
        file.write("0")
        high_score = 0

p1_score, p2_score = 0, 0
p1_flip, p2_flip = False, False
title_screen, end_screen = True, False
two_player = False
bc_timer = datetime.now()
bc_ttl = randint(2, 5)  # time to live for bonus coin
clock = pygame.time.Clock()
while run:
    clock.tick(60)
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
        game_start = datetime.now()

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

    if (datetime.now() - bc_timer).total_seconds() * 1000 > (bc_ttl * 1000):
        bc.set_location(SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1)
        bc_timer = datetime.now()
    else:
        if datetime.now().microsecond % 1000 == 0:
            if randint(0, 10) == 0:
                bc.new_location(SCREEN_WIDTH, SCREEN_HEIGHT)
                bc_timer = datetime.now()
            else:
                bomb.new_location(SCREEN_WIDTH)

    # collision
    if f1.rect.colliderect(bc.rect):
        bc.set_location(SCREEN_WIDTH, SCREEN_HEIGHT)
        p1_score += 50

    if f1.rect.colliderect(c.rect):
        c.new_location(SCREEN_WIDTH, SCREEN_HEIGHT)
        p1_score += 10

    if f1.rect.colliderect(bomb.rect):
        bomb.new_location(SCREEN_WIDTH)
        p1_score -= 20

    if two_player:
        if f2.rect.colliderect(c.rect):
            c.new_location(SCREEN_WIDTH, SCREEN_HEIGHT)
            p2_score += 10

        if f2.rect.colliderect(bc.rect):
            bc.set_location(SCREEN_WIDTH, SCREEN_HEIGHT)
            p2_score += 50

        if f2.rect.colliderect(bomb.rect):
            bomb.new_location(SCREEN_WIDTH)
            p2_score -= 20

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
    time_remaining_display = my_font.render(
        f"Time remaining: {60 - (datetime.now() - game_start).seconds} seconds",
        True,
        (255, 255, 255),
    )
    screen.blit(time_remaining_display, (0, 30))
    screen.blit(c.image, c.rect)
    screen.blit(bc.image, bc.rect)
    screen.blit(f1.image, f1.rect)
    screen.blit(bomb.image, bomb.rect)
    if two_player:
        screen.blit(f2.image, f2.rect)
        screen.blit(display_p2_score, (0, 30))

    bomb.set_location(bomb.x, bomb.y + 5)
    pygame.display.update()

    if (datetime.now() - game_start).total_seconds() > 2:
        end_screen = True

    while end_screen:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                end_screen = False

        screen.fill((r, g, b))
        end_message = "Game Over!"
        end_font = pygame.font.SysFont("Arial", 50)
        display_end = end_font.render(end_message, True, (255, 255, 255))
        text_x = (SCREEN_WIDTH - display_end.get_width()) // 2
        text_y = (SCREEN_HEIGHT - display_end.get_height()) // 2
        screen.blit(display_end, (text_x, text_y - 25))
        if two_player:
            if p1_score == p2_score:
                winner = "It's a tie!"
            elif p1_score > p2_score:
                winner = f"Player 1 wins, with {p1_score} points!"
            else:
                winner = f"Player 2 wins, with {p2_score} points!"
        else:
            winner = f"Your score: {p1_score}"
        display_winner = my_font.render(winner, True, (255, 255, 255))
        screen.blit(display_winner, (text_x, text_y + 25))
        display_click_to_exit = my_font.render("Click to exit", True, (255, 255, 255))
        screen.blit(display_click_to_exit, (text_x, text_y + 50))
        pygame.display.update()

with open(f"{__file__.replace('__init__.py', '')}high_score.txt", "w") as file:
    file.truncate(0)
    if p1_score > high_score:
        file.write(str(p1_score))
    elif two_player and p2_score > high_score:
        file.write(str(p2_score))
    else:
        file.write(str(high_score))
# Once we have exited the main program loop we can stop the game engine:
pygame.quit()

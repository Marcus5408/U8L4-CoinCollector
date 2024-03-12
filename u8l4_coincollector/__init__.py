import pygame
from fox import Fox
from coin import Coin


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
message = "Collision not detected"
r = 50
g = 0
b = 100


# render the text for later
display_name = my_font.render(name, True, (255, 255, 255))
display_message = my_font.render(message, True, (255, 255, 255))


f = Fox(40, 60)
c = Coin(200, 85)


# The loop will carry on until the user exits the game (e.g. clicks the close button).
run = True


# -------- Main Program Loop -----------
while run:

    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_d]:
        f.move_direction("right")

    # collision
    if f.rect.colliderect(c.rect):
        message = "Collision detected"
        display_message = my_font.render(message, True, (255, 255, 255))
    else:
        message = "Collision not detected"
        display_message = my_font.render(message, True, (255, 255, 255))

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False

    screen.fill((r, g, b))
    screen.blit(display_name, (0, 0))
    screen.blit(display_message, (0, 15))
    screen.blit(f.image, f.rect)
    screen.blit(c.image, c.rect)
    pygame.display.update()


# Once we have exited the main program loop we can stop the game engine:
pygame.quit()

import pygame, sys
from pygame.locals import *
from game_logic import Bob, Zombie, screen, unit_length, screen_width, screen_height, next_zombie
import random

pygame.init()

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
mainLoop = True
background = 150, 150, 150


# Load Crosshair

target = pygame.image.load("target.gif")
target = pygame.transform.scale(target, (5 * unit_length / 6, 5 * unit_length / 6))
target_rect = target.get_rect()


bob_rect = pygame.Rect((screen_width / 2, screen_height / 2), (unit_length, 2 * unit_length))


def generate_new_zombie(speed):
    side = random.choice(["top", "top", "top", "top", "bottom", "bottom", "bottom", "bottom", "left", "left", "left", "right", "right", "right"])
    if side == "top":
        x = random.randint(0, screen_width)
        y = -2 * unit_length
    elif side == "bottom":
        x = random.randint(0, screen_width)
        y = screen_height + 2 * unit_length
    elif side == "left":
        x = -unit_length
        y = random.randint(0, screen_height)
    else:
        x = screen_width + unit_length
        y = random.randint(0, screen_height)
    rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
    return Zombie(rect, 0, "left", speed)


zombies = [generate_new_zombie(0.14)]

bob = Bob(bob_rect, 0, "left", 0.3, "pistol")

while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

    # Time elapsed since last iteration
    dt = clock.tick(60)

    screen.fill(background)


    # Bob
    bob.get_velocity(dt)
    bob.get_direction()
    if bob.count > 200:
        bob.get_step()
    bob.paint()
    bob.rect = bob.rect.move([t * dt for t in bob.velocity])

    # Zombies
    for zombie in zombies:
        zombie.rect = zombie.rect.move([t * dt for t in zombie.get_speed(bob.rect)])
        zombie.count += 1
        if zombie.count > 15:
            zombie.get_step()
        zombie.paint(bob.rect)

    if pygame.time.get_ticks() > next_zombie:
        next_zombie += 2000
        zombies.append(generate_new_zombie(0.14))



    # Crosshair
    target_rect.center = pygame.mouse.get_pos()  # update position
    screen.blit(target, target_rect)  # draw the cursor

    pygame.display.update()
    if pygame.key.get_pressed()[K_ESCAPE]:
        break

pygame.quit()
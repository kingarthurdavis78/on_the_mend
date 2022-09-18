import pygame, sys
from pygame.locals import *
import math

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.mouse.set_visible(False)
mainLoop = True
background = 150, 150, 150

speed = [0, 0]
speed_increment = 0.3
zombie_speed_constant = 0.14
direction = "RIGHT"
zombie_step = "left"
movement_counter = 0
zombie_movement_counter = 0
step = "left"

target = pygame.image.load("target.gif")
target = pygame.transform.scale(target, (50, 50))
target_rect = target.get_rect()

# Load Bob pictures
bob_left_step = pygame.image.load("bob-pistol-left.gif")
bob_left_step = pygame.transform.scale(bob_left_step, (80, 120))

bob_right_step = pygame.image.load("bob-pistol-right.gif")
bob_right_step = pygame.transform.scale(bob_right_step, (80, 120))

bob = pygame.image.load("bob-pistol.gif")
bob = pygame.transform.scale(bob, (80, 120))

bob_rect = pygame.Rect((0, 0), (60, 120))


# Load Zombie pictures
zombie_facing_right_left_step = pygame.image.load("zombie-facing-right-left-foot.gif")
zombie_facing_right_left_step = pygame.transform.scale(zombie_facing_right_left_step, (60, 120))

zombie_facing_right_right_step = pygame.image.load("zombie-facing-right-right-foot.gif")
zombie_facing_right_right_step = pygame.transform.scale(zombie_facing_right_right_step, (60, 120))

zombie_facing_left_left_step = pygame.image.load("zombie-facing-left-left-foot.gif")
zombie_facing_left_left_step = pygame.transform.scale(zombie_facing_left_left_step, (60, 120))

zombie_facing_left_right_step = pygame.image.load("zombie-facing-left-right-foot.gif")
zombie_facing_left_right_step = pygame.transform.scale(zombie_facing_left_right_step, (60, 120))

zombie_rect = pygame.Rect((500, 500), (60, 120))

# Square Root of 2
root_two = math.sqrt(2)


def get_speed(counter, dt):
    if pygame.key.get_pressed()[K_w] and pygame.key.get_pressed()[K_d]:
        speed = [speed_increment / root_two, -speed_increment / root_two]
        counter += dt
    elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_d]:
        speed = [speed_increment / root_two, speed_increment / root_two]
        counter += dt
    elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_a]:
        speed = [-speed_increment / root_two, speed_increment / root_two]
        counter += dt
    elif pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_w]:
        speed = [-speed_increment / root_two, -speed_increment / root_two]
        counter += dt
    elif pygame.key.get_pressed()[K_w]:
        speed = [0, -speed_increment]
        counter += dt
    elif pygame.key.get_pressed()[K_d]:
        speed = [speed_increment, 0]
        counter += dt
    elif pygame.key.get_pressed()[K_s]:
        speed = [0, speed_increment]
        counter += dt
    elif pygame.key.get_pressed()[K_a]:
        speed = [-speed_increment, 0]
        counter += dt
    else:
        speed = [0, 0]

    if pygame.key.get_pressed()[K_w] and pygame.key.get_pressed()[K_s]:
        speed[1] = 0
    if pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_d]:
        speed[0] = 0
    return speed, counter


def get_direction(direction):
    if pygame.mouse.get_pos()[0] < bob_rect.center[0] and direction == "RIGHT":
        return "LEFT", pygame.transform.flip(bob, True, False), pygame.transform.flip(bob_left_step, True, False), pygame.transform.flip(bob_right_step, True, False)
    if pygame.mouse.get_pos()[0] > bob_rect.center[0] and direction == "LEFT":
        return "RIGHT", pygame.transform.flip(bob, True, False), pygame.transform.flip(bob_left_step, True, False), pygame.transform.flip(bob_right_step, True, False)
    return direction, bob, bob_left_step, bob_right_step


def get_step(step_direction, counter):
    counter = 0
    if step_direction == "left":
        step_direction = "right"
    else:
        step_direction = "left"
    return step_direction, counter


def paint_bob(speed, step):
    if speed == [0, 0]:
        screen.blit(bob, bob_rect)
    elif step == "left":
        screen.blit(bob_left_step, bob_rect)
    elif step == "right":
        screen.blit(bob_right_step, bob_rect)


def get_zombie_speed():
    dx = bob_rect.center[0] - zombie_rect.center[0]
    dy = bob_rect.center[1] - zombie_rect.center[1]
    norm = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    return zombie_speed_constant * dx / norm, zombie_speed_constant * dy / norm


while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

    # Time elapsed since last iteration
    dt = clock.tick(60)

    # Bob
    speed, movement_counter = get_speed(movement_counter, dt)
    direction, bob, bob_left_step, bob_right_step = get_direction(direction)
    screen.fill(background)
    if movement_counter > 200:
        step, movement_counter = get_step(step, movement_counter)
    paint_bob(speed, step)
    bob_rect = bob_rect.move([t * dt for t in speed])

    # Zombies
    zombie_rect = zombie_rect.move([t * dt for t in get_zombie_speed()])
    zombie_movement_counter += 1
    if zombie_movement_counter > 15:
        zombie_movement_counter = 0
        if zombie_step == "left":
            zombie_step = "right"
        else:
            zombie_step = "left"
    if zombie_step == "left":
        if bob_rect.center[0] > zombie_rect.center[0]:
            screen.blit(zombie_facing_right_left_step, zombie_rect)
        else:
            screen.blit(zombie_facing_left_left_step, zombie_rect)
    else:
        if bob_rect.center[0] > zombie_rect.center[0]:
            screen.blit(zombie_facing_right_right_step, zombie_rect)
        else:
            screen.blit(zombie_facing_left_right_step, zombie_rect)

    # Crosshair
    target_rect.center = pygame.mouse.get_pos()  # update position
    screen.blit(target, target_rect)  # draw the cursor

    pygame.display.update()
    if pygame.key.get_pressed()[K_ESCAPE]:
        pygame.quit()

pygame.quit()
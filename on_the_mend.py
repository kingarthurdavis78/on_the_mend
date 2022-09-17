import pygame, sys
from pygame.locals import *
import math

pygame.init()

#Create a displace surface object
screen = pygame.display.set_mode((1000, 1000))

pygame.mouse.set_visible(False)

mainLoop = True
background = 150, 150, 150

speed = [0, 0]
direction = "RIGHT"
movement_counter = 0
step = "left"

target = pygame.image.load("target.gif")
target = pygame.transform.scale(target, (50, 50))
target_rect = target.get_rect()

bob_left_step = pygame.image.load("bob-pistol-left.gif")
bob_left_step = pygame.transform.scale(bob_left_step, (80, 120))

bob_right_step = pygame.image.load("bob-pistol-right.gif")
bob_right_step = pygame.transform.scale(bob_right_step, (80, 120))

bob = pygame.image.load("bob-pistol.gif")
bob = pygame.transform.scale(bob, (80, 120))

bobrect = pygame.Rect((0, 0), (60, 120))

root_two = math.sqrt(2)


def get_speed(counter):
    if pygame.key.get_pressed()[K_w] and pygame.key.get_pressed()[K_d]:
        speed = [root_two, -root_two]
        counter += 1
    elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_d]:
        speed = [root_two, root_two]
        counter += 1
    elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_a]:
        speed = [-root_two, root_two]
        counter += 1
    elif pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_w]:
        speed = [-root_two, -root_two]
        counter += 1
    elif pygame.key.get_pressed()[K_w]:
        speed = [0, -1]
        counter += 1
    elif pygame.key.get_pressed()[K_d]:
        speed = [1, 0]
        counter += 1
    elif pygame.key.get_pressed()[K_s]:
        speed = [0, 1]
        counter += 1
    elif pygame.key.get_pressed()[K_a]:
        speed = [-1, 0]
        counter += 1
    else:
        speed = [0, 0]

    if pygame.key.get_pressed()[K_w] and pygame.key.get_pressed()[K_s]:
        speed[1] = 0
    if pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_d]:
        speed[0] = 0
    return speed, counter


def get_direction(direction):
    if pygame.mouse.get_pos()[0] < bobrect.center[0] and direction == "RIGHT":
        return "LEFT", pygame.transform.flip(bob, True, False), pygame.transform.flip(bob_left_step, True, False), pygame.transform.flip(bob_right_step, True, False)
    if pygame.mouse.get_pos()[0] > bobrect.center[0] and direction == "LEFT":
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
        screen.blit(bob, bobrect)
    elif step == "left":
        screen.blit(bob_left_step, bobrect)
    elif step == "right":
        screen.blit(bob_right_step, bobrect)


while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

    # Bob
    speed, movement_counter = get_speed(movement_counter)
    direction, bob, bob_left_step, bob_right_step = get_direction(direction)
    screen.fill(background)
    if movement_counter > 15:
        step, movement_counter = get_step(step, movement_counter)
    paint_bob(speed, step)
    bobrect = bobrect.move(speed)

    # in your main loop update the position every frame and blit the image
    target_rect.center = pygame.mouse.get_pos()  # update position
    screen.blit(target, target_rect)  # draw the cursor

    pygame.display.update()

pygame.quit()
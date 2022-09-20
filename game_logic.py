import math
import pygame
from pygame.locals import *
import random

# Square Root of 2
root_two = math.sqrt(2)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
unit_length = screen_width / 40

zombie_frequency = 400
zombie_timer = 0

gun = "pistol"

# Load Bob Pictures
bob_facing_right_still = pygame.image.load(f"bob-{gun}-facing-right-still.gif")
bob_facing_right_still = pygame.transform.scale(bob_facing_right_still, (4 * unit_length / 3, 2 * unit_length))

bob_facing_right_left_step = pygame.image.load(f"bob-{gun}-facing-right-left-foot.gif")
bob_facing_right_left_step = pygame.transform.scale(bob_facing_right_left_step, (4 * unit_length / 3, 2 * unit_length))

bob_facing_right_right_step = pygame.image.load(f"bob-{gun}-facing-right-right-foot.gif")
bob_facing_right_right_step = pygame.transform.scale(bob_facing_right_right_step, (4 * unit_length / 3, 2 * unit_length))

bob_facing_left_still = pygame.image.load(f"bob-{gun}-facing-left-still.gif")
bob_facing_left_still = pygame.transform.scale(bob_facing_left_still, (4 * unit_length / 3, 2 * unit_length))

bob_facing_left_left_step = pygame.image.load(f"bob-{gun}-facing-left-left-foot.gif")
bob_facing_left_left_step = pygame.transform.scale(bob_facing_left_left_step, (4 * unit_length / 3, 2 * unit_length))

bob_facing_left_right_step = pygame.image.load(f"bob-{gun}-facing-left-right-foot.gif")
bob_facing_left_right_step = pygame.transform.scale(bob_facing_left_right_step, (4 * unit_length / 3, 2 * unit_length))


# Load Zombie Pictures
zombie_facing_right_left_step = pygame.image.load("zombie-facing-right-left-foot.gif")
zombie_facing_right_left_step = pygame.transform.scale(zombie_facing_right_left_step, (unit_length, 2 * unit_length))

zombie_facing_right_right_step = pygame.image.load("zombie-facing-right-right-foot.gif")
zombie_facing_right_right_step = pygame.transform.scale(zombie_facing_right_right_step, (unit_length, 2 * unit_length))

zombie_facing_left_left_step = pygame.image.load("zombie-facing-left-left-foot.gif")
zombie_facing_left_left_step = pygame.transform.scale(zombie_facing_left_left_step, (unit_length, 2 * unit_length))

zombie_facing_left_right_step = pygame.image.load("zombie-facing-left-right-foot.gif")
zombie_facing_left_right_step = pygame.transform.scale(zombie_facing_left_right_step, (unit_length, 2 * unit_length))


def norm(dy, dx):
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))


class Bob:
    def __init__(self, count, step, speed, gun):
        self.rect = pygame.Rect((screen_width / 2, screen_height / 2), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.images = [bob_facing_right_still, bob_facing_right_left_step, bob_facing_right_right_step]

    def x(self):
        return self.rect.center[0]

    def y(self):
        return self.rect.center[1]

    def get_velocity(self, dt):
        if pygame.key.get_pressed()[K_w] and pygame.key.get_pressed()[K_d]:
            self.velocity = [self.speed / root_two, -self.speed / root_two]
            self.count += dt
        elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_d]:
            self.velocity = [self.speed / root_two, self.speed / root_two]
            self.count += dt
        elif pygame.key.get_pressed()[K_s] and pygame.key.get_pressed()[K_a]:
            self.velocity = [-self.speed / root_two, self.speed / root_two]
            self.count += dt
        elif pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_w]:
            self.velocity = [-self.speed / root_two, -self.speed / root_two]
            self.count += dt
        elif pygame.key.get_pressed()[K_w]:
            self.velocity = [0, -self.speed]
            self.count += dt
        elif pygame.key.get_pressed()[K_d]:
            self.velocity = [self.speed, 0]
            self.count += dt
        elif pygame.key.get_pressed()[K_s]:
            self.velocity = [0, self.speed]
            self.count += dt
        elif pygame.key.get_pressed()[K_a]:
            self.velocity = [-self.speed, 0]
            self.count += dt
        else:
            self.velocity = [0, 0]

        if pygame.key.get_pressed()[K_w] and pygame.key.get_pressed()[K_s]:
            self.velocity[1] = 0
        if pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_d]:
            self.velocity[0] = 0

    def get_direction(self):
        if pygame.mouse.get_pos()[0] < self.rect.center[0] and self.direction == "right":
            self.direction = "left"
            self.images = [bob_facing_left_still, bob_facing_left_left_step, bob_facing_left_right_step]
        if pygame.mouse.get_pos()[0] > self.rect.center[0] and self.direction == "left":
            self.direction = "right"
            self.images = [bob_facing_right_still, bob_facing_right_left_step, bob_facing_right_right_step]

    def get_step(self):
        if self.step == "left":
            self.step = "right"
        else:
            self.step = "left"
        self.count = 0

    def paint(self):
        if self.velocity == [0, 0]:
            screen.blit(self.images[0], self.rect)
        elif self.step == "left":
            screen.blit(self.images[1], self.rect)
        elif self.step == "right":
            screen.blit(self.images[2], self.rect)


class Zombie:
    def __init__(self, rect, count, step, speed):
        self.rect = rect
        self.count = count
        self.step = step
        self.speed = speed

    def x(self):
        return self.rect.center[0]

    def y(self):
        return self.rect.center[1]

    def get_speed(self, bob_rect):
        dx = bob_rect.center[0] - self.rect.center[0]
        dy = bob_rect.center[1] - self.rect.center[1]
        return self.speed * dx / norm(dy, dx), self.speed * dy / norm(dy, dx)

    def get_step(self):
        if self.step == "left":
            self.step = "right"
        else:
            self.step = "left"
        self.count = 0

    def paint(self, bob_rect):
        if self.step == "left":
            if bob_rect.center[0] > self.x():
                screen.blit(zombie_facing_right_left_step, self.rect)
            else:
                screen.blit(zombie_facing_left_left_step, self.rect)
        else:
            if bob_rect.center[0] > self.x():
                screen.blit(zombie_facing_right_right_step, self.rect)
            else:
                screen.blit(zombie_facing_left_right_step, self.rect)


class Bullet:
    def __init__(self, velocity, speed, x, y):
        self.velocity = velocity
        self.speed = speed
        self.rect = pygame.Rect((x, y), (unit_length/6, unit_length/6))

    def x(self):
        return self.rect.center[0]

    def y(self):
        return self.rect.center[1]

    def paint(self):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)


class Gun:
    def __init__(self, name, speed, reload_time):
        self.name = name
        self.speed = speed
        self.reload_counter = 0
        self.reload_time = reload_time


class Crosshair:
    image = pygame.transform.scale(pygame.image.load("target.gif"), (5 * unit_length / 6, 5 * unit_length / 6))

    def __init__(self, image):
        self.rect = image.get_rect()

    def paint(self):
        screen.blit(self.image, self.rect)


def new_bullet(bob, speed):
    dx = pygame.mouse.get_pos()[0] - bob.x()
    dy = pygame.mouse.get_pos()[1] - bob.y()
    bob.reload = 0
    bullet_vector = [dx / norm(dy, dx), dy / norm(dy, dx)]
    return Bullet(bullet_vector, speed, bob.x(), bob.y())


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


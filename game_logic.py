import math
import pygame
from pygame.locals import *
import random
from pathlib import Path

bob_images = Path(__file__).parent / "bob-images"
crosshair_images = Path(__file__).parent / "crosshair-images"
zombie_images = Path(__file__).parent / "zombie-images"
gun_images = Path(__file__).parent / "gun-images"



# Square Root of 2
root_two = math.sqrt(2)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
unit_length = screen_width / 40

# Load Bob Pictures
bob_facing_right_still = pygame.image.load(bob_images / "blue-right-still.gif")
bob_facing_right_still = pygame.transform.scale(bob_facing_right_still, (unit_length, 2 * unit_length))

bob_facing_right_left_step = pygame.image.load(bob_images / "blue-right-left.gif")
bob_facing_right_left_step = pygame.transform.scale(bob_facing_right_left_step, (unit_length, 2 * unit_length))

bob_facing_right_right_step = pygame.image.load(bob_images / "blue-right-right.gif")
bob_facing_right_right_step = pygame.transform.scale(bob_facing_right_right_step, (unit_length, 2 * unit_length))

bob_facing_left_still = pygame.image.load(bob_images / "blue-left-right.gif")
bob_facing_left_still = pygame.transform.scale(bob_facing_left_still, (unit_length, 2 * unit_length))

bob_facing_left_left_step = pygame.image.load(bob_images / "blue-left-left.gif")
bob_facing_left_left_step = pygame.transform.scale(bob_facing_left_left_step, (unit_length, 2 * unit_length))

bob_facing_left_right_step = pygame.image.load(bob_images / "blue-left-right.gif")
bob_facing_left_right_step = pygame.transform.scale(bob_facing_left_right_step, (unit_length, 2 * unit_length))

# Guns
pistol_right = pygame.image.load(gun_images / "pistol-right.gif")
pistol_right = pygame.transform.scale(pistol_right, (2 * unit_length, 2 * unit_length))

pistol_left = pygame.image.load(gun_images / "pistol-left.gif")
pistol_left = pygame.transform.scale(pistol_left, (2 * unit_length, 2 * unit_length))

shotgun_right = pygame.image.load(gun_images / "shotgun-right.gif")
shotgun_right = pygame.transform.scale(shotgun_right, (2 * unit_length, 2 * unit_length))

shotgun_left = pygame.image.load(gun_images / "shotgun-left.gif")
shotgun_left = pygame.transform.scale(shotgun_left, (2 * unit_length, 2 * unit_length))


# Load Zombie Pictures
zombie_facing_right_left_step = pygame.image.load(zombie_images / "zombie-facing-right-left-foot.gif")
zombie_facing_right_left_step = pygame.transform.scale(zombie_facing_right_left_step, (unit_length, 2 * unit_length))

zombie_facing_right_right_step = pygame.image.load(zombie_images / "zombie-facing-right-right-foot.gif")
zombie_facing_right_right_step = pygame.transform.scale(zombie_facing_right_right_step, (unit_length, 2 * unit_length))

zombie_facing_left_left_step = pygame.image.load(zombie_images / "zombie-facing-left-left-foot.gif")
zombie_facing_left_left_step = pygame.transform.scale(zombie_facing_left_left_step, (unit_length, 2 * unit_length))

zombie_facing_left_right_step = pygame.image.load(zombie_images / "zombie-facing-left-right-foot.gif")
zombie_facing_left_right_step = pygame.transform.scale(zombie_facing_left_right_step, (unit_length, 2 * unit_length))

# Create Color Dictionary
colors_to_rgb = {}
colors_to_rgb["red"] = (255, 0, 0)
colors_to_rgb["blue"] = (0, 0, 255)
colors_to_rgb["yellow"] = (255, 255, 0)
colors_to_rgb["pink"] = (255, 0, 255)
colors_to_rgb["turquoise"] = (0, 255, 255)
colors_to_rgb["orange"] = (255, 173, 0)
colors_to_rgb["black"] = (0, 0, 0)


# Calculate Magnitude of Vector
def norm(dy, dx):
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))


# Keyboard Bob
class Bob:
    def __init__(self, player_name, x, y, count, step, speed, gun, crosshair):
        self.player_name = player_name
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.images = [bob_facing_right_still, bob_facing_right_left_step, bob_facing_right_right_step]
        self.crosshair = crosshair
        self.cross_dx = 0
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0

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
            self.gun.image = self.gun.images[0]
        if pygame.mouse.get_pos()[0] > self.rect.center[0] and self.direction == "left":
            self.direction = "right"
            self.images = [bob_facing_right_still, bob_facing_right_left_step, bob_facing_right_right_step]
            self.gun.image = self.gun.images[1]



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

    def update_crosshair(self, stufff, stuff):
        self.crosshair.rect.center = pygame.mouse.get_pos()
        return stufff, stuff

    def shoot(self):
        if pygame.mouse.get_pressed()[0]:
            return True
        return False

    def paint_health(self, index, num_players):
        color = colors_to_rgb[self.crosshair.color]
        pygame.draw.rect(screen, color, (index * int(screen_width / num_players), screen_height - int(screen_height / 20), int((self.health * (screen_width / num_players)) / 100), int(screen_height / 20)))

    def paint_revive(self, index, num_players):
        pygame.draw.rect(screen, (0, 255, 0), (index * int(screen_width / num_players), screen_height - int(screen_height / 20), int((self.revive_count * (screen_width / num_players)) / 1000), int(screen_height / 20)))

    def revive(self, dead_bob):
        if self.rect.colliderect(dead_bob.rect) and pygame.key.get_pressed()[K_RETURN]:
            return True
        return False


    def paint_gun(self):
        self.gun.rect.center = self.rect.center
        screen.blit(self.gun.image, self.gun.rect)

# USB Controller Bob
class Bob_Joystick_USB:
    def __init__(self, player_name, x, y, count, step, speed, gun, joystick, crosshair):
        self.player_name = player_name
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.images = [bob_facing_right_still, bob_facing_right_left_step, bob_facing_right_right_step]
        self.joystick = joystick
        self.crosshair = crosshair
        self.cross_dx = 1
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0

    def x(self):
        return self.rect.centerx

    def y(self):
        return self.rect.centery

    def get_velocity(self, dt):
        dx = self.joystick.get_axis(0)
        dy = self.joystick.get_axis(1)
        if abs(dx) < 0.05:
            dx = 0
        if abs(dy) < 0.05:
            dy = 0
        if norm(dy, dx) == 0:
            self.velocity = [0, 0]
        else:
            self.velocity = [self.speed * dx / norm(dy, dx), self.speed * dy / norm(dy, dx)]
            self.count += dt

    def get_direction(self):
        if self.crosshair.rect.centerx < self.rect.centerx and self.direction == "right":
            self.direction = "left"
            self.images = [bob_facing_left_still, bob_facing_left_left_step, bob_facing_left_right_step]
        if self.crosshair.rect.centerx > self.rect.centerx and self.direction == "left":
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

    def update_crosshair(self, past_dx, past_dy):
        dx = self.joystick.get_axis(2)
        dy = self.joystick.get_axis(3)
        if abs(dx) < 0.05 and abs(dy) < 0.05:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * past_dx / norm(past_dy, past_dx), self.rect.centery + 5 * unit_length * past_dy / norm(past_dy, past_dx)]
            return past_dx, past_dy
        else:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * dx / norm(dy, dx), self.rect.centery + 5 * unit_length * dy / norm(dy, dx)]
            return dx, dy

    def shoot(self):
        if self.joystick.get_axis(5) > 0:
            return True
        return False

    def paint_health(self, index, num_players):
        color = colors_to_rgb[self.crosshair.color]
        pygame.draw.rect(screen, color, (index * int(screen_width / num_players), screen_height - int(screen_height / 20), int((self.health * (screen_width / num_players)) / 100), int(screen_height / 20)))

    def revive(self, dead_bob):
        dx = dead_bob.rect.centerx - self.rect.centerx
        dy = dead_bob.rect.centery - self.rect.centery
        if norm(dy, dx) < unit_length and self.joystick.get_button(0):
            return True
        return False

# Xbox Controller Bob
class Bob_Joystick_XboxOne:
    def __init__(self, player_name, x, y, count, step, speed, gun, joystick, crosshair):
        self.player_name = player_name
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.images = [bob_facing_right_still, bob_facing_right_left_step, bob_facing_right_right_step]
        self.joystick = joystick
        self.crosshair = crosshair
        self.cross_dx = 1
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0

    def x(self):
        return self.rect.centerx

    def y(self):
        return self.rect.centery

    def get_velocity(self, dt):
        dx = self.joystick.get_axis(0)
        dy = self.joystick.get_axis(1)
        if abs(dx) < 0.05:
            dx = 0
        if abs(dy) < 0.05:
            dy = 0
        if norm(dy, dx) == 0:
            self.velocity = [0, 0]
        else:
            self.velocity = [self.speed * dx / norm(dy, dx), self.speed * dy / norm(dy, dx)]
            self.count += dt

    def get_direction(self):
        if self.crosshair.rect.centerx < self.rect.centerx and self.direction == "right":
            self.direction = "left"
            self.images = [bob_facing_left_still, bob_facing_left_left_step, bob_facing_left_right_step]
        if self.crosshair.rect.centerx >= self.rect.centerx and self.direction == "left":
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

    def update_crosshair(self, past_dx, past_dy):
        dx = self.joystick.get_axis(3)
        dy = self.joystick.get_axis(4)
        if abs(dx) < 0.05 and abs(dy) < 0.05:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * past_dx / norm(past_dy, past_dx), self.rect.centery + 5 * unit_length * past_dy / norm(past_dy, past_dx)]
            return past_dx, past_dy
        else:
            if dx == -1:
                dx = -math.sqrt(1 - pow(dy, 2))
            elif dx == 1:
                dx = math.sqrt(1 - pow(dy, 2))
            elif dy == -1:
                dy = -math.sqrt(1 - pow(dx, 2))
            elif dy == 1:
                dy = math.sqrt(1 - pow(dx, 2))
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * dx / norm(dy, dx), self.rect.centery + 5 * unit_length * dy / norm(dy, dx)]
            return dx, dy

    def shoot(self):
        if self.joystick.get_axis(5) > 0:
            return True
        return False

    def paint_health(self, index, num_players):
        color = colors_to_rgb[self.crosshair.color]
        pygame.draw.rect(screen, color, (index * int(screen_width / num_players), screen_height - int(screen_height / 20), int((self.health * (screen_width / num_players)) / 100), int(screen_height / 20)))

    def revive(self, dead_bob):
        dx = dead_bob.rect.centerx - self.rect.centerx
        dy = dead_bob.rect.centery - self.rect.centery
        if norm(dy, dx) < unit_length and self.joystick.get_button(0):
            return True
        return False

# Pro Controller Bob
class Bob_Joystick_ProController:
    def __init__(self, player_name, x, y, count, step, speed, gun, joystick, crosshair):
        self.player_name = player_name
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.images = [bob_facing_right_still, bob_facing_right_left_step, bob_facing_right_right_step]
        self.joystick = joystick
        self.crosshair = crosshair
        self.cross_dx = 1
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0

    def x(self):
        return self.rect.centerx

    def y(self):
        return self.rect.centery

    def get_velocity(self, dt):
        dx = 2 * self.joystick.get_axis(0)
        dy = 2 * self.joystick.get_axis(1)
        if abs(dx) < 0.35:
            dx = 0
        if abs(dy) < 0.35:
            dy = 0
        if norm(dy, dx) == 0:
            self.velocity = [0, 0]
        else:
            self.velocity = [self.speed * dx / norm(dy, dx), self.speed * dy / norm(dy, dx)]
            self.count += dt

    def get_direction(self):
        if self.crosshair.rect.centerx < self.rect.centerx and self.direction == "right":
            self.direction = "left"
            self.images = [bob_facing_left_still, bob_facing_left_left_step, bob_facing_left_right_step]
        if self.crosshair.rect.centerx >= self.rect.centerx and self.direction == "left":
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

    def update_crosshair(self, past_dx, past_dy):
        dx = self.joystick.get_axis(2)
        dy = self.joystick.get_axis(3)
        if abs(dx) < 0.35 and abs(dy) < 0.35:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * past_dx / norm(past_dy, past_dx), self.rect.centery + 5 * unit_length * past_dy / norm(past_dy, past_dx)]
            return past_dx, past_dy
        else:
            if dx == -1:
                dx = -math.sqrt(1 - pow(dy, 2))
            elif dx == 1:
                dx = math.sqrt(1 - pow(dy, 2))
            elif dy == -1:
                dy = -math.sqrt(1 - pow(dx, 2))
            elif dy == 1:
                dy = math.sqrt(1 - pow(dx, 2))
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * dx / norm(dy, dx), self.rect.centery + 5 * unit_length * dy / norm(dy, dx)]
            return dx, dy

    def shoot(self):
        if self.joystick.get_button(7) > 0:
            return True
        return False

    def paint_health(self, index, num_players):
        color = colors_to_rgb[self.crosshair.color]
        pygame.draw.rect(screen, color, (index * int(screen_width / num_players), screen_height - int(screen_height / 20), int((self.health * (screen_width / num_players)) / 100), int(screen_height / 20)))

    def revive(self, dead_bob):
        dx = dead_bob.rect.centerx - self.rect.centerx
        dy = dead_bob.rect.centery - self.rect.centery
        if norm(dy, dx) < unit_length and self.joystick.get_button(0):
            return True
        return False


class Zombie:

    frequency = 400
    timer = 0

    speed_frequency = 2000
    speed_timer = 0

    def __init__(self, rect, count, step, speed):
        self.rect = rect
        self.count = count
        self.step = step
        self.speed = speed
        self.health = 3

    def x(self):
        return self.rect.center[0]

    def y(self):
        return self.rect.center[1]

    def get_speed(self, bob_rect):
        dx = bob_rect.centerx - self.rect.centerx
        dy = bob_rect.centery - self.rect.centery
        if norm(dy, dx) == 0:
            return 0, 0
        else:
            return self.speed * dx / norm(dy, dx), self.speed * dy / norm(dy, dx)

    def get_step(self):
        if self.step == "left":
            self.step = "right"
        else:
            self.step = "left"
        self.count = 0

    def paint(self, bob_rect):
        if self.step == "left":
            if bob_rect.centerx > self.rect.centerx:
                screen.blit(zombie_facing_right_left_step, self.rect)
            else:
                screen.blit(zombie_facing_left_left_step, self.rect)
        else:
            if bob_rect.centerx > self.rect.centerx:
                screen.blit(zombie_facing_right_right_step, self.rect)
            else:
                screen.blit(zombie_facing_left_right_step, self.rect)

    def find_closest_bob(self, bobs):
        closest_bob = None
        shortest_distance = 1000000000
        for bob in bobs:
            if bob.is_alive:
                dx = bob.rect.centerx - self.rect.centerx
                dy = bob.rect.centery - self.rect.centery
                distance = math.sqrt(pow(dx, 2) + pow(dy, 2))
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_bob = bob
        return closest_bob


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
    def __init__(self, id, speed, reload_time):
        self.id = id
        self.speed = speed
        self.reload_counter = 0
        self.reload_time = reload_time
        self.image = pistol_right
        self.images = [pistol_left, pistol_right]
        self.rect = self.image.get_rect()



class Crosshair:

    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load(crosshair_images / f"{color}_crosshair.gif"), (5 * unit_length / 6, 5 * unit_length / 6))
        self.rect = self.image.get_rect()

    def paint(self):
        screen.blit(self.image, self.rect)


def new_bullet(bob, speed):
    dx = bob.crosshair.rect.centerx - bob.rect.centerx
    dy = bob.crosshair.rect.centery - bob.rect.centery
    bob.reload = 0
    bullet_vector = [3 * dx / norm(dy, dx), 3 * dy / norm(dy, dx)]
    return Bullet(bullet_vector, speed, bob.rect.centerx, bob.rect.centery)


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


def paint_bullets(bullets, zombies, dt):
    for bullet in bullets:
        deleted = False
        if bullet.x() < 0 or bullet.x() > screen_width:
            bullets.remove(bullet)
            del bullet
            continue
        if bullet.y() < 0 or bullet.y() > screen_height:
            bullets.remove(bullet)
            del bullet
            continue
        for zombie in zombies:
            if bullet.rect.colliderect(zombie.rect):
                bullets.remove(bullet)
                del bullet
                zombies.remove(zombie)
                del zombie
                deleted = True
                break
        if not deleted:
            bullet.rect = bullet.rect.move([v * dt * bullet.speed for v in bullet.velocity])
            bullet.paint()
    return bullets, zombies


def paint_revive(index, num_players, bob):
    pygame.draw.rect(screen, (0, 255, 0), (index * int(screen_width / num_players), screen_height - int(screen_height / 20), int((bob.revive_count * (screen_width / num_players)) / 1000), int(screen_height / 20)))



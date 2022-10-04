import math
import pygame
from pygame.locals import *
import random
from pathlib import Path

bob_images = Path(__file__).parent / "bob-images"
crosshair_images = Path(__file__).parent / "crosshair-images"
zombie_images = Path(__file__).parent / "zombie-images"
gun_images = Path(__file__).parent / "gun-images"
item_images = Path(__file__).parent / "item-images"

# Square Root of 2
root_two = math.sqrt(2)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
unit_length = screen_width / 40

# Health Kit
health_kit_image = pygame.transform.scale(pygame.image.load(item_images / "first-aid-kit.gif"),
                                            (5 * unit_length / 6, 5 * unit_length / 6))

# Guns
pistol_right = pygame.image.load(gun_images / "pistol-right.gif")
pistol_right = pygame.transform.scale(pistol_right, (2 * unit_length, 2 * unit_length))

pistol_left = pygame.image.load(gun_images / "pistol-left.gif")
pistol_left = pygame.transform.scale(pistol_left, (2 * unit_length, 2 * unit_length))

shotgun_right = pygame.image.load(gun_images / "shotgun-right.gif")
shotgun_right = pygame.transform.scale(shotgun_right, (2 * unit_length, 2 * unit_length))

shotgun_left = pygame.image.load(gun_images / "shotgun-left.gif")
shotgun_left = pygame.transform.scale(shotgun_left, (2 * unit_length, 2 * unit_length))

minigun_right = pygame.image.load(gun_images / "minigun-right.gif")
minigun_right = pygame.transform.scale(minigun_right, (2 * unit_length, 2 * unit_length))

minigun_left = pygame.image.load(gun_images / "minigun-left.gif")
minigun_left = pygame.transform.scale(minigun_left, (2 * unit_length, 2 * unit_length))

# Load Zombie Pictures
zombie_facing_right_left_step = pygame.image.load(zombie_images / "zombie-facing-right-left-foot.gif")
zombie_facing_right_left_step = pygame.transform.scale(zombie_facing_right_left_step, (unit_length, 2 * unit_length))

zombie_facing_right_right_step = pygame.image.load(zombie_images / "zombie-facing-right-right-foot.gif")
zombie_facing_right_right_step = pygame.transform.scale(zombie_facing_right_right_step, (unit_length, 2 * unit_length))

zombie_facing_left_left_step = pygame.image.load(zombie_images / "zombie-facing-left-left-foot.gif")
zombie_facing_left_left_step = pygame.transform.scale(zombie_facing_left_left_step, (unit_length, 2 * unit_length))

zombie_facing_left_right_step = pygame.image.load(zombie_images / "zombie-facing-left-right-foot.gif")
zombie_facing_left_right_step = pygame.transform.scale(zombie_facing_left_right_step, (unit_length, 2 * unit_length))

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 32)


# Create Color Dictionary
colors_to_rgb = {}
colors_to_rgb["red"] = (255, 0, 0)
colors_to_rgb["blue"] = (0, 0, 255)
colors_to_rgb["yellow"] = (255, 255, 0)
colors_to_rgb["pink"] = (255, 0, 255)
colors_to_rgb["turquoise"] = (0, 255, 255)
colors_to_rgb["orange"] = (255, 173, 0)
colors_to_rgb["black"] = (0, 0, 0)

standard_speed = 600

# Calculate Magnitude of Vector
def norm(dy, dx):
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))


# Keyboard Bob
class Bob:
    def __init__(self, player_name, color, x, y, count, step, speed, gun, crosshair):
        self.player_name = player_name
        self.color = color
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.image = pygame.transform.scale(pygame.image.load(bob_images / f"{color}-right-still.gif"),
                                            (unit_length, 2 * unit_length))
        self.crosshair = crosshair
        self.cross_dx = 0
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0
        self.kill_count = 0

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

    def update_crosshair(self, stufff, stuff):
        self.crosshair.rect.center = pygame.mouse.get_pos()
        return stufff, stuff

    def shoot(self):
        if pygame.mouse.get_pressed()[0]:
            return True
        return False

    def revive(self, dead_bob):
        if self.rect.colliderect(dead_bob.rect) and pygame.key.get_pressed()[K_RETURN]:
            return True
        return False


# USB Controller Bob
class Bob_Joystick_USB:
    def __init__(self, player_name, color, x, y, count, step, speed, gun, joystick, crosshair):
        self.player_name = player_name
        self.color = color
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.image = pygame.transform.scale(pygame.image.load(bob_images / f"{color}-right-still.gif"),
                                            (unit_length, 2 * unit_length))
        self.joystick = joystick
        self.crosshair = crosshair
        self.cross_dx = 1
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0
        self.kill_count = 0

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

    def update_crosshair(self, past_dx, past_dy):
        dx = self.joystick.get_axis(2)
        dy = self.joystick.get_axis(3)
        if abs(dx) < 0.05 and abs(dy) < 0.05:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * past_dx / norm(past_dy, past_dx),
                                          self.rect.centery + 5 * unit_length * past_dy / norm(past_dy, past_dx)]
            return past_dx, past_dy
        else:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * dx / norm(dy, dx),
                                          self.rect.centery + 5 * unit_length * dy / norm(dy, dx)]
            return dx, dy

    def shoot(self):
        if self.joystick.get_axis(5) > 0:
            return True
        return False

    def revive(self, dead_bob):
        dx = dead_bob.rect.centerx - self.rect.centerx
        dy = dead_bob.rect.centery - self.rect.centery
        if norm(dy, dx) < unit_length and self.joystick.get_button(0):
            return True
        return False


# Xbox Controller Bob
class Bob_Joystick_XboxOne:
    def __init__(self, player_name, color, x, y, count, step, speed, gun, joystick, crosshair):
        self.player_name = player_name
        self.color = color
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.image = pygame.transform.scale(pygame.image.load(bob_images / f"{color}-right-still.gif"),
                                            (unit_length, 2 * unit_length))
        self.joystick = joystick
        self.crosshair = crosshair
        self.cross_dx = 1
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0
        self.kill_count = 0


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

    def update_crosshair(self, past_dx, past_dy):
        dx = self.joystick.get_axis(3)
        dy = self.joystick.get_axis(4)
        if abs(dx) < 0.05 and abs(dy) < 0.05:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * past_dx / norm(past_dy, past_dx),
                                          self.rect.centery + 5 * unit_length * past_dy / norm(past_dy, past_dx)]
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
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * dx / norm(dy, dx),
                                          self.rect.centery + 5 * unit_length * dy / norm(dy, dx)]
            return dx, dy

    def shoot(self):
        if self.joystick.get_axis(5) > 0:
            return True
        return False

    def revive(self, dead_bob):
        dx = dead_bob.rect.centerx - self.rect.centerx
        dy = dead_bob.rect.centery - self.rect.centery
        if norm(dy, dx) < unit_length and self.joystick.get_button(0):
            return True
        return False

# Pro Controller Bob
class Bob_Joystick_ProController:
    def __init__(self, player_name, color, x, y, count, step, speed, gun, joystick, crosshair):
        self.player_name = player_name
        self.color = color
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.image = pygame.transform.scale(pygame.image.load(bob_images / f"{color}-right-still.gif"),
                                            (unit_length, 2 * unit_length))
        self.joystick = joystick
        self.crosshair = crosshair
        self.cross_dx = 1
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0
        self.kill_count = 0


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

    def update_crosshair(self, past_dx, past_dy):
        dx = self.joystick.get_axis(2)
        dy = self.joystick.get_axis(3)
        if abs(dx) < 0.35 and abs(dy) < 0.35:
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * past_dx / norm(past_dy, past_dx),
                                          self.rect.centery + 5 * unit_length * past_dy / norm(past_dy, past_dx)]
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
            self.crosshair.rect.center = [self.rect.centerx + 5 * unit_length * dx / norm(dy, dx),
                                          self.rect.centery + 5 * unit_length * dy / norm(dy, dx)]
            return dx, dy

    def shoot(self):
        if self.joystick.get_button(7) > 0:
            return True
        return False

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

    def __init__(self, rect, count, step, speed, health):
        self.rect = rect
        self.count = count
        self.step = step
        self.speed = speed
        self.health = health
        self.direction = None

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
        if bob_rect.centerx > self.rect.centerx:
            if self.step == "left":
                screen.blit(zombie_facing_right_left_step, self.rect)
            else:
                screen.blit(zombie_facing_right_right_step, self.rect)
            if self.health < 3:
                screen.blit(pygame.transform.scale(pygame.image.load(zombie_images / f"blood-right-{self.health}.gif"), (unit_length, 2 * unit_length)), self.rect)
        else:
            if self.step == "left":
                screen.blit(zombie_facing_left_left_step, self.rect)
            else:
                screen.blit(zombie_facing_left_right_step, self.rect)
            if self.health < 3:
                screen.blit(pygame.transform.scale(pygame.image.load(zombie_images / f"blood-left-{self.health}.gif"), (unit_length, 2 * unit_length)), self.rect)


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
    def __init__(self, owner, velocity, speed, x, y):
        self.owner = owner
        self.velocity = velocity
        self.speed = speed
        self.rect = pygame.Rect((x, y), (unit_length / 6, unit_length / 6))

    def paint(self):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)


class Gun:
    def __init__(self, player_number, name, speed, reload_time):
        self.player_number = player_number
        self.name = name
        self.reload_counter = 0
        self.bullet_per_shot = 1
        self.error = 0
        if self.name == "pistol":
            self.speed = speed
            self.reload_time = reload_time
            self.image = pistol_right
            self.images = [pistol_left, pistol_right]
        elif self.name == "shotgun":
            self.error = 20
            self.bullet_per_shot = 4
            self.speed = speed
            self.reload_time = 2 * reload_time
            self.image = shotgun_right
            self.images = [shotgun_left, shotgun_right]
        elif self.name == "minigun":
            self.error = 10
            self.bullet_per_shot = 1
            self.speed = speed
            self.reload_time = reload_time / 5
            self.image = minigun_right
            self.images = [minigun_left, minigun_right]
        self.rect = self.image.get_rect()


class Crosshair:

    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load(crosshair_images / f"{color}_crosshair.gif"),
                                            (5 * unit_length / 6, 5 * unit_length / 6))
        self.rect = self.image.get_rect()

    def paint(self):
        screen.blit(self.image, self.rect)


class Item:
    def __init__(self, item, type, x, y):
        self.get = item
        self.type = type
        item.rect.centerx = x
        item.rect.centery = y

    def paint(self):
        screen.blit(self.get.image, self.get.rect)


class Health_Item:
    def __init__(self, name, power):
        self.name = name
        self.power = power
        self.image = pygame.transform.scale(pygame.image.load(item_images / f"{name}.gif"),
                                            (5 * unit_length / 6, 5 * unit_length / 6))
        self.rect = self.image.get_rect()


def generate_item(items, num_players):
    item = random.choice(items)
    x = random.randint(unit_length, screen_width - unit_length)
    y = random.randint(unit_length, screen_height - unit_length)
    if item in "shotgun pistol minigun":
        return Item(Gun(None, item, 1 / num_players, standard_speed), "gun", x, y)
    elif item == "first-aid-kit":
        return Item(Health_Item(item, 25), "heal", x, y)


def paint_bob(self):
    if self.velocity == [0, 0]:
        self.image = pygame.transform.scale(
            pygame.image.load(bob_images / f"{self.color}-{self.direction}-still.gif"),
            (unit_length, 2 * unit_length))
    else:
        self.image = pygame.transform.scale(
            pygame.image.load(bob_images / f"{self.color}-{self.direction}-{self.step}.gif"),
            (unit_length, 2 * unit_length))
    screen.blit(self.image, self.rect)


def paint_gun(self):
    self.gun.rect.center = self.rect.center
    screen.blit(self.gun.image, self.gun.rect)


def get_step(self):
    if self.step == "left":
        self.step = "right"
    else:
        self.step = "left"
    self.count = 0


def get_direction(self):
    if self.crosshair.rect.centerx < self.rect.center[0] and self.direction == "right":
        self.direction = "left"
        self.gun.image = self.gun.images[0]
    if self.crosshair.rect.centerx > self.rect.center[0] and self.direction == "left":
        self.direction = "right"
        self.gun.image = self.gun.images[1]


def paint_level(difficulty, win_level):
    if difficulty == 0:
        difficulty = 460
    text = font.render(f'Level {difficulty} / {win_level}', True, (255, 255, 255), (150, 150, 150))
    text_rect = text.get_rect()
    text_rect.x = 0
    text_rect.y = 0
    screen.blit(text, text_rect)



def paint_health(bob, index, num_players):
    # Health Bar
    color = colors_to_rgb[bob.crosshair.color]
    health_bar = pygame.draw.rect(screen, color, (
        index * int(screen_width / num_players), screen_height - int(screen_height / 20),
        int((bob.health * (screen_width / num_players)) / 100), int(screen_height / 20)))
    # Player Stats
    text = font.render(f'Player {index}: Kills: {bob.kill_count}', True, (255, 255, 255), (150, 150, 150))
    text_rect = text.get_rect()
    text_rect.x = health_bar.x
    text_rect.y = health_bar.y - unit_length
    screen.blit(text, text_rect)


def new_bullet(bob, speed):
    bob.reload = 0
    bullet_error_x = random.randint(-bob.gun.error, bob.gun.error) / 100
    bullet_error_y = random.randint(-bob.gun.error, bob.gun.error) / 100
    dx = bob.crosshair.rect.centerx - bob.rect.centerx
    dy = bob.crosshair.rect.centery - bob.rect.centery
    new_dx = dx / norm(dy, dx) + bullet_error_x
    new_dy = dy / norm(dy, dx) + bullet_error_y
    bullet_vector = [2.5 * new_dx / norm(new_dy, new_dx), 2.5 * new_dy / norm(new_dy, new_dx)]
    return Bullet(bob, bullet_vector, speed, bob.rect.centerx, bob.rect.centery)


def generate_new_zombie(speed, health):
    side = random.choice(
        ["top", "top", "top", "top", "bottom", "bottom", "bottom", "bottom", "left", "left", "left", "right", "right",
         "right"])
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
    return Zombie(rect, 0, "left", speed, health)


def paint_bullets(bullets, zombies, dt):
    for bullet in bullets:
        deleted = False
        if bullet.rect.centerx < 0 or bullet.rect.centerx > screen_width:
            bullets.remove(bullet)
            del bullet
            continue
        if bullet.rect.centery < 0 or bullet.rect.centery > screen_height:
            bullets.remove(bullet)
            del bullet
            continue
        for zombie in zombies:
            if bullet.rect.colliderect(zombie.rect):
                zombie.health -= 1
                if zombie.health <= 0:
                    bullet.owner.kill_count += 1
                    zombies.remove(zombie)
                    del zombie
                bullets.remove(bullet)
                del bullet
                deleted = True
                break
        if not deleted:
            bullet.rect = bullet.rect.move([v * dt * bullet.speed for v in bullet.velocity])
            bullet.paint()
    return bullets, zombies


def paint_revive(index, num_players, bob):
    pygame.draw.rect(screen, (0, 255, 0), (
        index * int(screen_width / num_players), screen_height - int(screen_height / 20),
        int((bob.revive_count * (screen_width / num_players)) / 1000), int(screen_height / 20)))

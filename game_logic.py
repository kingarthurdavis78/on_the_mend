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
fonts = Path(__file__).parent / "fonts"
gifs = Path(__file__).parent / "gifs"
audio = Path(__file__).parent / "audio"



# Square Root of 2
root_two = math.sqrt(2)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
unit_length = int(screen_width / 40)

# Health Kit
health_kit_image = pygame.transform.scale(pygame.image.load(item_images / "first-aid-kit.gif").convert_alpha(),
                                            (5 * unit_length / 6, 5 * unit_length / 6))

# Guns
pistol_right = pygame.image.load(gun_images / "pistol-right.gif").convert_alpha()
pistol_right = pygame.transform.scale(pistol_right, (2 * unit_length, 2 * unit_length))

pistol_left = pygame.image.load(gun_images / "pistol-left.gif").convert_alpha()
pistol_left = pygame.transform.scale(pistol_left, (2 * unit_length, 2 * unit_length))

shotgun_right = pygame.image.load(gun_images / "shotgun-right.gif").convert_alpha()
shotgun_right = pygame.transform.scale(shotgun_right, (2 * unit_length, 2 * unit_length))

shotgun_left = pygame.image.load(gun_images / "shotgun-left.gif").convert_alpha()
shotgun_left = pygame.transform.scale(shotgun_left, (2 * unit_length, 2 * unit_length))

minigun_right = pygame.image.load(gun_images / "minigun-right.gif").convert_alpha()
minigun_right = pygame.transform.scale(minigun_right, (2 * unit_length, 2 * unit_length))

minigun_left = pygame.image.load(gun_images / "minigun-left.gif").convert_alpha()
minigun_left = pygame.transform.scale(minigun_left, (2 * unit_length, 2 * unit_length))

# Load Zombie Pictures
zombie_facing_right_left_step = pygame.image.load(zombie_images / "zombie-facing-right-left-foot.gif").convert_alpha()
zombie_facing_right_left_step = pygame.transform.scale(zombie_facing_right_left_step, (unit_length, 2 * unit_length))

zombie_facing_right_right_step = pygame.image.load(zombie_images / "zombie-facing-right-right-foot.gif").convert_alpha()
zombie_facing_right_right_step = pygame.transform.scale(zombie_facing_right_right_step, (unit_length, 2 * unit_length))

zombie_facing_left_left_step = pygame.image.load(zombie_images / "zombie-facing-left-left-foot.gif").convert_alpha()
zombie_facing_left_left_step = pygame.transform.scale(zombie_facing_left_left_step, (unit_length, 2 * unit_length))

zombie_facing_left_right_step = pygame.image.load(zombie_images / "zombie-facing-left-right-foot.gif").convert_alpha()
zombie_facing_left_right_step = pygame.transform.scale(zombie_facing_left_right_step, (unit_length, 2 * unit_length))

pygame.font.init()
font = pygame.font.Font(str(fonts / "prstartk.ttf"), int(unit_length / 1.3))


# Create Color Dictionary
colors_to_rgb = {}
colors_to_rgb["red"] = (255, 0, 0)
colors_to_rgb["blue"] = (0, 0, 255)
colors_to_rgb["yellow"] = (255, 255, 0)
colors_to_rgb["pink"] = (255, 0, 255)
colors_to_rgb["turquoise"] = (0, 255, 255)
colors_to_rgb["orange"] = (255, 173, 0)
colors_to_rgb["black"] = (0, 0, 0)

standard_speed = 2.5
standard_reload_time = 600


# Calculate Magnitude of Vector
def norm(dy, dx):
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))


def get_controller(joystick):
    class Controller:
        if joystick == "keys":
            def sprinting(self):
                return pygame.key.get_pressed()[K_LSHIFT]
        elif "wireless" in joystick.get_name().lower():
            if "xbox" in joystick.get_name().lower():
                # Xbox Controller
                def move_x(self):
                    return joystick.get_axis(0)

                def move_y(self):
                    return joystick.get_axis(1)

                def aim_x(self):
                    return joystick.get_axis(3)

                def aim_y(self):
                    return joystick.get_axis(4)

                def trigger(self):
                    return joystick.get_axis(5)

                def revive_button(self):
                    return joystick.get_button(1)

                def sprinting(self):
                    return joystick.get_button(6)

            else:
                # Switch Pro Controller
                def move_x(self):
                    return 0.35 * joystick.get_axis(0)

                def move_y(self):
                    return 0.35 * joystick.get_axis(1)

                def aim_x(self):
                    return 0.4 * joystick.get_axis(2)

                def aim_y(self):
                    return 0.4 * joystick.get_axis(3)

                def trigger(self):
                    return joystick.get_button(7)

                def revive_button(self):
                    return joystick.get_button(1)

                def sprinting(self):
                    return joystick.get_button(10)

        else:
            # USB Controller
            def move_x(self):
                return joystick.get_axis(0)

            def move_y(self):
                return joystick.get_axis(1)

            def aim_x(self):
                return joystick.get_axis(2)

            def aim_y(self):
                return joystick.get_axis(3)

            def trigger(self):
                return joystick.get_axis(5)

            def revive_button(self):
                return joystick.get_button(0)
    return Controller()


# Controller Bob
class Controller_Bob:
    def __init__(self, player_name, color, x, y, count, step, speed, gun, joystick, crosshair):
        self.player_name = player_name
        self.controller = get_controller(joystick)
        self.color = color
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.image = pygame.transform.scale(pygame.image.load(bob_images / f"{color}-right-still.gif").convert_alpha(),
                                            (unit_length, 2 * unit_length))
        self.crosshair = crosshair
        self.cross_dx = 1
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0
        self.kill_count = 0
        self.on_fire = 0
        self.fire_gif = None

    def get_velocity(self, dt):
        dx = self.controller.move_x()
        dy = self.controller.move_y()
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
        dx = self.controller.aim_x()
        dy = self.controller.aim_y()
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
        if self.controller.trigger() > 0:
            return True
        return False

    def revive(self, dead_bob):
        dx = dead_bob.rect.centerx - self.rect.centerx
        dy = dead_bob.rect.centery - self.rect.centery
        if norm(dy, dx) < unit_length and self.controller.revive_button():
            return True
        return False


# Keyboard Bob
class Bob:
    def __init__(self, player_name, color, x, y, count, step, speed, gun, crosshair):
        self.player_name = player_name
        self.controller = get_controller(player_name)
        self.color = color
        self.rect = pygame.Rect((x, y), (unit_length, 2 * unit_length))
        self.count = count
        self.step = step
        self.speed = speed
        self.velocity = [0, 0]
        self.gun = gun
        self.direction = "right"
        self.image = pygame.transform.scale(pygame.image.load(bob_images / f"{color}-right-still.gif").convert_alpha(),
                                            (unit_length, 2 * unit_length))
        self.crosshair = crosshair
        self.cross_dx = 0
        self.cross_dy = 0
        self.health = 100
        self.is_alive = True
        self.revive_count = 0
        self.kill_count = 0
        self.on_fire = 0
        self.fire_gif = None

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


class Zombie:
    frequency = 400
    timer = 0

    speed_frequency = 2000
    speed_timer = 0

    color = None

    def __init__(self, rect, count, step, speed, health):
        self.on_fire = 0
        self.fire_gif = None
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
        if self.on_fire > 0:
            rect = self.fire_gif.image.get_rect()
            rect.centerx = self.rect.centerx
            rect.y = self.rect.y - 2 * unit_length
            screen.blit(self.fire_gif.image, rect)
        if bob_rect.centerx > self.rect.centerx:
            if self.step == "left":
                screen.blit(zombie_facing_right_left_step, self.rect)
            else:
                screen.blit(zombie_facing_right_right_step, self.rect)
            health_int = math.ceil(self.health)
            if health_int < 3:
                screen.blit(pygame.transform.scale(pygame.image.load(zombie_images / f"blood-right-{health_int}.gif").convert_alpha(), (unit_length, 2 * unit_length)), self.rect)
        else:
            if self.step == "left":
                screen.blit(zombie_facing_left_left_step, self.rect)
            else:
                screen.blit(zombie_facing_left_right_step, self.rect)
            health_int = math.ceil(self.health)
            if 0 < health_int < 3:
                screen.blit(pygame.transform.scale(pygame.image.load(zombie_images / f"blood-left-{health_int}.gif").convert_alpha(), (unit_length, 2 * unit_length)), self.rect)

    def find_closest_bob(self, bobs):
        closest_bob = None
        shortest_distance = 1000000000
        for bob in bobs:
            if bob.is_alive:
                distance = get_distance(self, bob)
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_bob = bob
        return closest_bob


class Bullet:
    def __init__(self, owner, gif, velocity, x, y):
        self.owner = owner
        self.velocity = velocity
        self.gif = gif
        self.time_on_screen = 0
        if self.owner.gun.name == "flamethrower":
            self.image = self.gif.image
            self.rect = self.image.get_rect()
            self.rect.center = x, y
        else:
            self.gif = None
            self.rect = pygame.Rect((x, y), (unit_length / 6, unit_length / 6))

    def paint(self):
        if self.gif is None:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)
        else:
            self.image = self.gif.image
            screen.blit(self.image, self.rect)


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
            self.damage = 1
        elif self.name == "shotgun":
            self.error = 20
            self.bullet_per_shot = 4
            self.speed = speed
            self.reload_time = 2 * reload_time
            self.image = shotgun_right
            self.images = [shotgun_left, shotgun_right]
            self.damage = 1
        elif self.name == "minigun":
            self.error = 10
            self.bullet_per_shot = 1
            self.speed = speed
            self.reload_time = reload_time / 5
            self.image = minigun_right
            self.images = [minigun_left, minigun_right]
            self.damage = 1
        elif self.name == "flamethrower":
            self.error = 15
            self.bullet_per_shot = 5
            self.speed = 0.5 * speed
            self.reload_time = reload_time / 15
            self.image = minigun_right
            self.images = [minigun_left, minigun_right]
            self.damage = 0.2
        self.rect = self.image.get_rect()


class Crosshair:

    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load(crosshair_images / f"{color}_crosshair.gif").convert_alpha(),
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
        self.image = pygame.transform.scale(pygame.image.load(item_images / f"{name}.gif").convert_alpha(),
                                            (5 * unit_length / 6, 5 * unit_length / 6))
        self.rect = self.image.get_rect()


class Gif:
    def __init__(self, name, frame_rate, num_frames, x_len, y_len):
        self.name = name
        self.frame_rate = frame_rate
        self.time_since_last_frame = 0
        self.frame_number = 0
        self.num_frames = num_frames
        self.images = [pygame.transform.scale(pygame.image.load(gifs / f"{name}-{i}.gif").convert_alpha(), (x_len, y_len)) for i in range(num_frames)]
        self.image = self.images[0]

    def update_frame(self, dt):
        self.time_since_last_frame += dt
        if self.frame_rate < self.time_since_last_frame:
            self.time_since_last_frame = 0
            self.frame_number += 1
            if self.frame_number == self.num_frames:
                self.frame_number = 0
        self.image = self.images[self.frame_number]


def play_sound(filename, channel):
    pygame.mixer.Channel(channel).play(pygame.mixer.Sound(audio / filename))


def set_on_fire(entity, intensity, gifs):
    entity.on_fire = intensity
    zombie_fire = Gif("on-fire", 120, 4, (4 * unit_length), (4 * unit_length))
    gifs.append(zombie_fire)
    entity.fire_gif = zombie_fire


def get_distance(entity1, entity2):
    x1 = entity1.rect.centerx
    x2 = entity2.rect.centerx
    dx = x1 - x2
    y1 = entity1.rect.centery
    y2 = entity2.rect.centery
    dy = y1 - y2
    return norm(dy, dx)


def spread_fire(entity, zombies, gifs):
    for zombie in zombies:
        distance = get_distance(entity, zombie)
        if distance < screen_width / 10 and random.random() < 0.01:
            if zombie.on_fire > 0:
                pass
            else:
                set_on_fire(zombie, 100, gifs)


def generate_item(items, account_for_lag):
    item = random.choice(items)
    x = random.randint(unit_length, screen_width - unit_length)
    y = random.randint(unit_length, screen_height - unit_length)
    if item in "shotgun pistol minigun flamethrower":
        return Item(Gun(None, item, standard_speed * account_for_lag, standard_reload_time), "gun", x, y)
    elif item == "first-aid-kit":
        return Item(Health_Item(item, 25), "heal", x, y)


def paint_bob(self):
    if self.on_fire > 0:
        rect = self.fire_gif.image.get_rect()
        rect.centerx = self.rect.centerx
        rect.y = self.rect.y - 2 * unit_length
        screen.blit(self.fire_gif.image, rect)
    if self.velocity == [0, 0]:
        self.image = pygame.transform.scale(
            pygame.image.load(bob_images / f"{self.color}-{self.direction}-still.gif").convert_alpha(),
            (unit_length, 2 * unit_length))
    else:
        self.image = pygame.transform.scale(
            pygame.image.load(bob_images / f"{self.color}-{self.direction}-{self.step}.gif").convert_alpha(),
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
        difficulty = win_level
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
    text = font.render(f'Player {index + 1} Kills: {bob.kill_count}', True, (255, 255, 255), (150, 150, 150))
    text_rect = text.get_rect()
    text_rect.x = health_bar.x
    text_rect.y = health_bar.y - unit_length
    screen.blit(text, text_rect)


def new_bullet(bob, gifs):
    if bob.gun.name != "flamethrower":
        play_sound("pew.mp3", 1)
    bob.reload = 0
    bullet_error_x = random.randint(-bob.gun.error, bob.gun.error) / 100
    bullet_error_y = random.randint(-bob.gun.error, bob.gun.error) / 100
    dx = bob.crosshair.rect.centerx - bob.rect.centerx
    dy = bob.crosshair.rect.centery - bob.rect.centery
    new_dx = dx / norm(dy, dx) + bullet_error_x
    new_dy = dy / norm(dy, dx) + bullet_error_y
    bullet_vector = [bob.gun.speed * new_dx / norm(new_dy, new_dx), bob.gun.speed * new_dy / norm(new_dy, new_dx)]
    if bob.gun.name == "flamethrower":
        new_fire = Gif("fire", 60, 4, (5 * unit_length / 6), (5 * unit_length / 6))
        gifs.append(new_fire)
        return Bullet(bob, new_fire, bullet_vector, bob.rect.centerx, bob.rect.centery)

    else:
        return Bullet(bob, None, bullet_vector, bob.rect.centerx, bob.rect.centery)


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


def paint_bullets(bullets, zombies, bobs, dt, gifs):
    opponents = zombies + bobs
    for bullet in bullets:
        bullet.time_on_screen += dt
        if bullet.owner.gun.name == "flamethrower":
            bullet.velocity = [(0.99) * v for v in bullet.velocity]
            if bullet.time_on_screen > 1000:
                if bullet.gif in gifs:
                    gifs.remove(bullet.gif)
                del bullet.gif
                bullets.remove(bullet)
                del bullet
                continue
        deleted = False
        if bullet.rect.centerx < 0 or bullet.rect.centerx > screen_width:
            bullets.remove(bullet)
            if bullet.gif:
                gifs.remove(bullet.gif)
                del bullet.gif
            del bullet
            continue
        if bullet.rect.centery < 0 or bullet.rect.centery > screen_height:
            bullets.remove(bullet)
            if bullet.gif:
                gifs.remove(bullet.gif)
                del bullet.gif
            del bullet
            continue
        for opponent in opponents:
            if bullet.rect.colliderect(opponent.rect) and bullet.owner.color != opponent.color:
                if bullet.gif and bullet.gif.name == "fire":
                    gifs.remove(bullet.gif)
                    del bullet.gif
                    if opponent.on_fire > 0:
                        pass
                    else:
                        set_on_fire(opponent, 100, gifs)

                opponent.health -= bullet.owner.gun.damage
                if opponent.health <= 0:
                    bullet.owner.kill_count += 1
                    if opponent in zombies:
                        zombies.remove(opponent)
                        del opponent
                bullets.remove(bullet)
                del bullet
                deleted = True
                break
        if not deleted:
            bullet.rect = bullet.rect.move([0.4 * v * dt for v in bullet.velocity])
            bullet.paint()


def paint_revive(index, num_players, bob):
    pygame.draw.rect(screen, (0, 255, 0), (
        index * int(screen_width / num_players), screen_height - int(screen_height / 20),
        int((bob.revive_count * (screen_width / num_players)) / 1000), int(screen_height / 20)))


def team_alive(team):
    for player in team:
        if player.is_alive:
            return True
    return False


def winning_team(*args):
    teams_alive = 0
    the_winning_team = None
    for team in args:
        if team_alive(team):
            the_winning_team = team
            teams_alive += 1
    if teams_alive == 0:
        return "tie"
    if teams_alive > 1:
        return []
    else:
        return the_winning_team[0].color


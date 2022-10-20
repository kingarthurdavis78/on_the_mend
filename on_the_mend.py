import random
import sys
import pygame
from pygame.locals import *
from game_logic import Bob, Bob_Joystick_USB, Bob_Joystick_XboxOne, Bob_Joystick_ProController, screen, screen_width, screen_height, new_bullet, Gun, paint_gun, generate_new_zombie, Crosshair, paint_bullets, set_on_fire, get_step, get_direction, paint_bob, paint_health, paint_revive, paint_level, standard_speed, generate_item, norm, unit_length, spread_fire, play_sound

pygame.init()

pygame.mixer.init()
pygame.mixer.Channel(0).set_volume(0.7)
pygame.mixer.Channel(1).set_volume(0.2)
play_sound("bleak.mp3", 0)

difficulty = 1
clock = pygame.time.Clock()

pygame.joystick.init()

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

mainLoop = True
background = 150, 150, 150

# System input
keyboard_count = int(sys.argv[1])
controller_count = int(sys.argv[2])


num_players = keyboard_count + controller_count
players_alive = num_players


colors = ["red", "blue", "yellow", "pink", "turquoise", "orange", "black"]
crosshairs = []
guns = []
for i in range(num_players):
    guns.append(Gun(i, "pistol", standard_speed, 600))
    crosshairs.append(Crosshair(i, colors[i]))

bobs = []
dead_bobs = []


if keyboard_count:
    bobs.append(Bob("keys", colors.pop(0), screen_width / 2, screen_height / 2, 0, "left", 0.3, guns.pop(0), crosshairs.pop(0)))


bullets = []
zombies = []

items = ["first-aid-kit"]
gun_names = ["pistol", "minigun"]
items_on_ground = []
last_spawn_time = 0

gifs = []

endgame = 0
win_level = 400
win = False
connected = False
died = False
while mainLoop:
    # Initialize controllers
    if controller_count > 0 and len(bobs) <= num_players and not connected:
        if pygame.joystick.get_count() + keyboard_count >= num_players:
            joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

            for i in range(len(joysticks)):
                if len(bobs) == num_players:
                    break
                if "wireless" in joysticks[i].get_name().lower():
                    if "xbox" in joysticks[i].get_name().lower():
                        bobs.append(Bob_Joystick_XboxOne(f"Xbox One Controller {i}", colors[i], screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))
                    else:
                        bobs.append(Bob_Joystick_ProController(f"Pro Controller {i}", colors[i], screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))

                else:
                    bobs.append(Bob_Joystick_USB(f"USB Controller {i}", colors[i], screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))

        if len(bobs) == num_players:
            connected = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

    # Time elapsed since last iteration
    dt = clock.tick(60)

    # Erase previous frame
    screen.fill(background)

    # Display Level
    paint_level(int(difficulty), win_level)

    for gif in gifs:
        gif.update_frame(dt)

    # Zombies
    for zombie in zombies:
        if zombie.on_fire > 0:
            spread_fire(zombie, zombies, gifs)
            if zombie.health > 1:
                zombie.on_fire -= random.random()
                zombie.health -= 0.02 * random.random()
            else:
                zombie.on_fire -= 1.2 * random.random()
                zombie.health -= 0.01 * random.random()
            if zombie.health <= 0:
                zombies.remove(zombie)
                gifs.remove(zombie.fire_gif)
                del zombie.fire_gif
                del zombie
                continue
        close_bob = zombie.find_closest_bob(bobs)
        zombie.rect = zombie.rect.move([t * dt for t in zombie.get_speed(close_bob.rect)])
        # Walking Animation
        zombie.count += 1
        if zombie.count > 15:
            zombie.get_step()
        # Paint Zombie
        zombie.paint(close_bob.rect)

    for gif in gifs:
        gif.update_frame(dt)

    # Increase Difficulty
    if random.randint(0, int(100 + difficulty)) < 5 and not win:
        difficulty *= 1.02
        if difficulty >= win_level - 30 and not win:
            difficulty = 380
            endgame += 1
            print(endgame)
        if endgame > 50:
            difficulty = 0
            win = True

    # Generate Zombie
    if difficulty and random.randint(0, 400 - int(difficulty)) < 5:
        zombies.append(generate_new_zombie(0.1, 3))

    # Generate Zoombie
    if difficulty and random.randint(0, 4000 - 10 * int(difficulty)) < 5:
        zombies.append(generate_new_zombie(0.3, 1))

    # Bobs
    for bob in bobs:
        if bob.is_alive:
            player_number = bobs.index(bob)

            # Spawn New Item
            if bob.kill_count == 20 and pygame.time.get_ticks() - last_spawn_time > 10000:
                last_spawn_time = pygame.time.get_ticks()
                items_on_ground.append(generate_item(["shotgun"], num_players))
            if bob.kill_count == 80 and pygame.time.get_ticks() - last_spawn_time > 10000:
                last_spawn_time = pygame.time.get_ticks()
                items_on_ground.append(generate_item(["minigun"], num_players))
            if bob.kill_count == 120 and pygame.time.get_ticks() - last_spawn_time > 10000:
                last_spawn_time = pygame.time.get_ticks()
                items_on_ground.append(generate_item(["flamethrower"], num_players))
            if bob.kill_count > 0 and bob.kill_count % 47 == 0 and pygame.time.get_ticks() - last_spawn_time > 10000:
                last_spawn_time = pygame.time.get_ticks()
                items_on_ground.append(generate_item(items, num_players))


            # Items on ground
            for item in items_on_ground:
                item.paint()
                if bob.rect.colliderect(item.get.rect):
                    if item.type == "gun":
                        item.get.player_number = player_number
                        bob.gun = item.get
                        if bob.direction == "left":
                            bob.gun.image = bob.gun.images[0]
                    elif item.type == "heal":
                        bob.health += item.get.power
                        if bob.health > 100:
                            bob.health = 100
                    items_on_ground.remove(item)


            # Check if bob loses health
            for zombie in zombies:
                if bob.rect.colliderect(zombie.rect):
                    bob.health -= 1
                    if zombie.on_fire:
                        set_on_fire(bob, 1000, gifs)
            if bob.on_fire > 0:
                bob.health -= 0.1
                bob.on_fire -= norm(dt * bob.velocity[1], dt * bob.velocity[0])
            else:
                bob.on_fire = 0
                if bob.fire_gif != None:
                    gifs.remove(bob.fire_gif)
                    del bob.fire_gif
                    bob.fire_gif = None


            # Paint health bar
            paint_health(bob, player_number, num_players)

            # Update Bob
            bob.get_velocity(dt)
            get_direction(bob)
            # Walking Animation
            if bob.count > 200:
                get_step(bob)
            bob.rect = bob.rect.move([v * dt for v in bob.velocity])

            # Paint bob
            paint_bob(bob)

            # Paint Gun
            paint_gun(bob)

            # Bobs' Bullets
            bob.gun.reload_counter += dt
            if bob.shoot() and bob.gun.reload_counter > bob.gun.reload_time:
                bob.gun.reload_counter = 0
                for i in range(bob.gun.bullet_per_shot):
                    bullets.append(new_bullet(bob, gifs))
            bullets, zombies = paint_bullets(bullets, zombies, dt, gifs)

            # Bob's Crosshair
            bob.cross_dx, bob.cross_dy = bob.update_crosshair(bob.cross_dx, bob.cross_dy)
            bob.crosshair.paint()

            # Revive Teammate
            if num_players - players_alive > 0:
                revived_bob = False
                for dead_bob in dead_bobs:
                    if bob.revive(dead_bob):
                        player_number = bobs.index(dead_bob)
                        paint_revive(player_number, num_players, bob)
                        if bob.revive_count >= 1000:
                            dead_bob.is_alive = True
                            dead_bob.health = 100
                            dead_bobs.remove(dead_bob)
                            players_alive += 1
                        if not revived_bob:
                            bob.revive_count += dt
                        revived_bob = True
                if not revived_bob:
                    bob.revive_count = 0

            # Check if died
            if bob.health <= 0:
                bob.is_alive = False
                players_alive -= 1
                dead_bobs.append(bob)
                print(f"Kills: {bob.kill_count}")

        else:
            paint_bob(bob)

    if players_alive == 0:
        died = True

    pygame.display.update()

    if pygame.key.get_pressed()[K_ESCAPE] or died or (len(zombies) == 0 and win):
        break

if win and len(zombies) == 0:
    print('YOU WIN!!!')
pygame.quit()

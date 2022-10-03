import random
import sys
import pygame
from pygame.locals import *
from game_logic import Bob, Bob_Joystick_USB, Bob_Joystick_XboxOne, Bob_Joystick_ProController, screen, screen_width, screen_height, new_bullet, Gun, paint_gun, generate_new_zombie, Crosshair, paint_bullets, get_step, get_direction, paint_bob, paint_health, paint_revive

pygame.init()

difficulty = 0
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
items = ["shotgun"]
items_on_ground = []
crosshairs = []
guns = []
for i in range(num_players):
    guns.append(Gun(i, "pistol", 1 / num_players, 500))
    crosshairs.append(Crosshair(i, colors[i]))

bobs = []
dead_bobs = []

if keyboard_count:
    bobs.append(Bob("keys", colors.pop(0), screen_width / 2, screen_height / 2, 0, "left", 0.3, guns.pop(0), crosshairs.pop(0)))


bullets = []
zombies = []

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
                    print(joysticks[i].get_name())
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

    # Zombies
    for zombie in zombies:
        close_bob = zombie.find_closest_bob(bobs)
        zombie.rect = zombie.rect.move([t * dt for t in zombie.get_speed(close_bob.rect)])
        # Walking Animation
        zombie.count += 1
        if zombie.count > 15:
            zombie.get_step()
        # Paint Zombie
        zombie.paint(close_bob.rect)

    # Increase Difficulty
    if random.randint(0, 1000) < 5:
        difficulty += 1
        print(difficulty)

    # Generate Zombie
    if random.randint(0, int(250 / num_players) - difficulty) < 5:
        zombies.append(generate_new_zombie(0.1))

    # Generate Speed Zombie
    if random.randint(0, int(2500 / num_players) - 10 * difficulty) < 5:
        zombies.append(generate_new_zombie(0.3))

    # Bobs
    for bob in bobs:
        if bob.is_alive:

            # Check if bob loses health
            for zombie in zombies:
                if bob.rect.colliderect(zombie.rect):
                    bob.health -= 1

            # Paint health bar
            player_number = bobs.index(bob)
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
            bob.gun.speed = 1 / players_alive
            bob.gun.reload_counter += dt
            if bob.shoot() and bob.gun.reload_counter > bob.gun.reload_time:
                bob.gun.reload_counter = 0
                for i in range(bob.gun.bullet_per_shot):
                    bullets.append(new_bullet(bob, bob.gun.speed))
            bullets, zombies = paint_bullets(bullets, zombies, dt)

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
            bob.paint()

    if players_alive == 0:
        died = True

    pygame.display.update()

    if pygame.key.get_pressed()[K_ESCAPE] or died:
        break

pygame.quit()

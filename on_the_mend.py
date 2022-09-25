import random
import sys
import pygame
from pygame.locals import *
import platform
from game_logic import Bob, Bob_Joystick_USB, Bob_Joystick_Bluetooth, screen, screen_width, screen_height, new_bullet, Gun, Zombie, generate_new_zombie, zombie_timer, zombie_frequency, Crosshair, paint_bullets

pygame.init()

clock = pygame.time.Clock()

pygame.joystick.init()

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

mainLoop = True
background = 150, 150, 150

num_players = int(sys.argv[1])
players_alive = num_players


keyboard_controls = False
if sys.argv[2].lower() == "true":
    keyboard_controls = True


colors = ["red", "blue", "yellow", "pink", "green"]
crosshairs = []
guns = []
for i in range(num_players):
    guns.append(Gun(i, 1 / num_players, 100))
    crosshairs.append(Crosshair(i, colors[i]))

bobs = []
dead_bobs = []

if keyboard_controls:
    bobs.append(Bob("keys", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns.pop(0), crosshairs.pop(0)))
    controller_count = num_players - 1
else:
    controller_count = num_players

bullets = []
zombies = []


connected = False
died = False
while mainLoop:

    # Initialize controllers
    if len(bobs) <= num_players and not connected:
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        try:
            bt = 0
            for joystick in joysticks:
                if "wireless" in joystick.get_name().lower():
                    bt += 1
            usb = controller_count - bt
            for i in range(bt):
                bobs.append(Bob_Joystick_Bluetooth(f"Wireless Controller {i}", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))
            for i in range(usb):
                bobs.append(Bob_Joystick_USB(f"USB Controller {i}", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))
        except IndexError:
            pass
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
        zombie.count += 1
        if zombie.count > 15:
            zombie.get_step()
        zombie.paint(bobs[0].rect)

    # Generate Zombie
    if random.randint(0, 100) < 5:
        zombies.append(generate_new_zombie(0.1))

    # # Generate Zombie
    if random.randint(0, 1000) < 5:
        zombies.append(generate_new_zombie(0.3))

    # Bobs
    for bob in bobs:
        if bob.is_alive:
            # Check if bob loses health
            for zombie in zombies:
                if bob.rect.colliderect(zombie.rect):
                    bob.health -= 1

            # Paint healthbar
            player_number = bobs.index(bob)
            bob.paint_health(player_number, num_players)

            # Update Bob
            bob.get_velocity(dt)
            bob.get_direction()
            if bob.count > 200:
                bob.get_step()
            bob.rect = bob.rect.move([v * dt for v in bob.velocity])

            # Paint bob
            bob.paint()

            # Bobs' Bullets
            bob.gun.speed = 1 / players_alive
            bob.gun.reload_counter += dt
            if bob.shoot() and bob.gun.reload_counter > bob.gun.reload_time:
                bob.gun.reload_counter = 0
                bullets.append(new_bullet(bob, bob.gun.speed))
            bullets, zombies = paint_bullets(bullets, zombies, dt)

            # Bob's Crosshair
            bob.cross_dx, bob.cross_dy = bob.update_crosshair(bob.cross_dx, bob.cross_dy)
            bob.crosshair.paint()

            # Revive Teamate
            # if num_players - players_alive > 0:
            #     for dead_bob in dead_bobs:
            #         if bob.revive():
            #             revive_count += dt
            #             if revive_count > revive_time:
            #
            #         else:
            #             revive_count = 0

            # Check if died
            if bob.health <= 0:
                bob.is_alive = False
                players_alive -= 1
                dead_bobs.append(bob)

        else:
            bob.paint()

    if players_alive == 0:
        died = True

    pygame.display.update()

    if pygame.key.get_pressed()[K_ESCAPE] or died:
        break

pygame.quit()

import random
import sys
import pygame
from pygame.locals import *
from game_logic import Bob, Bob_Joystick_USB, Bob_Joystick_XboxOne, Bob_Joystick_ProController, screen, screen_width, screen_height, new_bullet, Gun, generate_new_zombie, Crosshair, paint_bullets, paint_revive

pygame.init()

difficulty = 0
clock = pygame.time.Clock()

pygame.joystick.init()

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

mainLoop = True
background = 150, 150, 150

# System input
keyboard_controls = int(sys.argv[1])
controller_count = int(sys.argv[2])


num_players = keyboard_controls + controller_count
players_alive = num_players


colors = ["red", "blue", "yellow", "pink", "turquoise", "orange", "black"]
crosshairs = []
guns = []
for i in range(num_players):
    guns.append(Gun(i, 1 / num_players, 500))
    crosshairs.append(Crosshair(i, colors[i]))

bobs = []
dead_bobs = []

if keyboard_controls:
    bobs.append(Bob("keys", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns.pop(0), crosshairs.pop(0)))


bullets = []
zombies = []

connected = False
died = False
while mainLoop:

    # Initialize controllers
    if controller_count > 0 and len(bobs) <= num_players and not connected:
        if pygame.joystick.get_count() + keyboard_controls >= num_players:
            joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            for i in range(len(joysticks)):
                if "wireless" in joysticks[i].get_name().lower():
                    if "xbox" in joysticks[i].get_name().lower():
                        bobs.append(Bob_Joystick_XboxOne(f"Xbox One Controller {i}", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))
                    else:
                        bobs.append(Bob_Joystick_ProController(f"Pro Controller {i}", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))

                else:
                    bobs.append(Bob_Joystick_USB(f"USB Controller {i}", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))

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
    if random.randint(0, int(325 / num_players) - difficulty) < 5:
        zombies.append(generate_new_zombie(0.1))

    # Generate Speed Zombie
    if random.randint(0, int(3250 / num_players) - 10 * difficulty) < 5:
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
            bob.paint_health(player_number, num_players)

            # Update Bob
            bob.get_velocity(dt)
            bob.get_direction()
            # Walking Animation
            if bob.count > 200:
                bob.get_step()
            bob.rect = bob.rect.move([v * dt for v in bob.velocity])

            # Paint bob
            bob.paint()

            # Paint Gun
            bob.paint_gun()

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

        else:
            bob.paint()

    if players_alive == 0:
        died = True

    pygame.display.update()

    if pygame.key.get_pressed()[K_ESCAPE] or died:
        break

pygame.quit()

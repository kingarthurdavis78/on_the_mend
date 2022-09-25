import sys
import pygame
from pygame.locals import *
import platform
from game_logic import Bob, Bob_Joystick_USB, Bob_Joystick_Bluetooth, screen, screen_width, screen_height, new_bullet, Gun, generate_new_zombie, zombie_timer, zombie_frequency, Crosshair, paint_bullets

# Detect what type of controllers to expect
if int(platform.release()[:2]) < 20:
    Controller = Bob_Joystick_USB
else:
    Controller = Bob_Joystick_Bluetooth

pygame.init()

clock = pygame.time.Clock()

pygame.joystick.init()

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

mainLoop = True
background = 150, 150, 150

num_players = int(sys.argv[1])


keyboard_controls = False
if sys.argv[2].lower() == "true":
    keyboard_controls = True


colors = ["red", "blue", "yellow", "pink", "green"]
crosshairs = []
guns = []
for i in range(num_players):
    guns.append(Gun(i, 1, 300))
    crosshairs.append(Crosshair(i, colors[i]))

bobs = []

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
    if len(bobs) <= num_players and not connected:
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        try:
            for i in range(controller_count):
                bobs.append(Controller(i, screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i], joysticks[i], crosshairs[i]))
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

    # # Generate Zombie
    # if pygame.time.get_ticks() > zombie_timer:
    #     zombie_timer += zombie_frequency
    #     zombies.append(generate_new_zombie(0.14))
    #
    # # Generate Speed Zombie
    # if pygame.time.get_ticks() > zombie_timer:
    #     zombie_timer += zombie_frequency
    #     zombies.append(generate_new_zombie(0.5))

    # Bobs
    for bob in bobs:

        # Check if bob died
        for zombie in zombies:
            if bob.rect.colliderect(zombie.rect):
                died = True

        # Update Bob
        bob.get_velocity(dt)
        bob.get_direction()
        if bob.count > 200:
            bob.get_step()
        bob.rect = bob.rect.move([v * dt for v in bob.velocity])

        # Paint bob
        bob.paint()

        # Bobs' Bullets
        bob.gun.reload_counter += dt
        if bob.shoot() and bob.gun.reload_counter > bob.gun.reload_time:
            bob.gun.reload_counter = 0
            bullets.append(new_bullet(bob, bob.gun.speed))
        bullets, zombies = paint_bullets(bullets, zombies, dt)

        # Bob's Crosshair
        bob.cross_dx, bob.cross_dy = bob.update_crosshair(bob.cross_dx, bob.cross_dy)
        bob.crosshair.paint()

    pygame.display.update()

    if pygame.key.get_pressed()[K_ESCAPE] or died:
        break

pygame.quit()

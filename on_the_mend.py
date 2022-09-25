import pygame
from pygame.locals import *
from game_logic import Bob, Bob_M1, Bob_Joystick2, screen, screen_width, screen_height, new_bullet, Gun, \
    generate_new_zombie, zombie_timer, zombie_frequency, Crosshair, paint_bullets

pygame.init()

clock = pygame.time.Clock()

pygame.joystick.init()

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

mainLoop = True
background = 150, 150, 150

num_players = 3

crosshairs = []
guns = []
for i in range(num_players + 1):
    guns.append(Gun(i, 1, 300))
    crosshairs.append(Crosshair(i, Crosshair.image))


bobs = [Bob("base", screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[0], crosshairs[0])]
bullets = []

zombies = []


connected = False
died = False
while mainLoop:
    if len(bobs) <= num_players and not connected:
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        try:
            for i in range(1, num_players + 1):
                bobs.append(Bob_Joystick2(i, screen_width / 2, screen_height / 2, 0, "left", 0.3, guns[i - 1], joysticks[i - 2], crosshairs[i - 1]))
        except IndexError:
            pass
        if len(bobs) == num_players + 1 and bobs[0].player_name == "base":
            del bobs[0]
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
        if bobs[0].rect.colliderect(zombie.rect):
            died = True
        zombie.rect = zombie.rect.move([t * dt for t in zombie.get_speed(bobs[0].rect)])
        zombie.count += 1
        if zombie.count > 15:
            zombie.get_step()
        zombie.paint(bobs[0].rect)

    # Generate New Zombie
    if pygame.time.get_ticks() > zombie_timer:
        zombie_timer += zombie_frequency
        zombies.append(generate_new_zombie(0.14))

    # Bob
    for bob in bobs:
        bob.get_velocity(dt)
        bob.get_direction()
        if bob.count > 200:
            bob.get_step()
        bob.rect = bob.rect.move([v * dt for v in bob.velocity])
        bob.paint()

        # Bullets
        bob.gun.reload_counter += dt
        if bob.shoot() and bob.gun.reload_counter > bob.gun.reload_time:
            bob.gun.reload_counter = 0
            bullets.append(new_bullet(bob, bob.gun.speed))
        bullets, zombies = paint_bullets(bullets, zombies, dt)

        # Crosshair
        bob.cross_dx, bob.cross_dy = bob.update_crosshair(bob.cross_dx, bob.cross_dy)
        bob.crosshair.paint()

    pygame.display.update()

    if pygame.key.get_pressed()[K_ESCAPE] or died:
        break

pygame.quit()

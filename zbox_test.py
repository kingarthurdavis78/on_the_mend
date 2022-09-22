import pygame
from pygame.locals import *
from game_logic import Bob, screen, unit_length, Bob_Joystick, screen_width, screen_height, new_bullet, Gun, generate_new_zombie, zombie_timer, zombie_frequency, Crosshair


# screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
pygame.init()

clock = pygame.time.Clock()


pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

mainLoop = True
background = 150, 150, 150

gun1 = Gun("pistol", 1, 600)
gun2 = Gun("pistol", 1, 600)
bobs = []
bullets = []

cross1 = Crosshair(Crosshair.image)
cross2 = Crosshair(Crosshair.image)

zombies = []
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
bobs.append(Bob_Joystick(screen_width / 2, screen_height / 2, 0, "left", 0.3, gun1, joysticks[0], cross1))
bobs.append(Bob_Joystick(screen_width / 2, screen_height / 2, 0, "left", 0.3, gun2, joysticks[1], cross2))

died = False
while mainLoop:
    for event in pygame.event.get():
        if event.type == JOYDEVICEADDED:
            pass
        # if event.type == JOYDEVICEREMOVED:
        #     joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        #     if len(joysticks) == 0:
        #         bob = Bob(bob.rect.centerx - unit_length / 2, bob.rect.centery - unit_length, 0 ,"left", 0.3, gun, Crosshair(Crosshair.image))
        if event.type == pygame.QUIT:
            mainLoop = False

    # Time elapsed since last iteration
    dt = clock.tick(60)

    screen.fill(background)

    # Bob
    for bob in bobs:
        bob.get_velocity(dt)
        bob.get_direction()
        if bob.count > 200:
            bob.get_step()
        bob.rect = bob.rect.move([v * dt for v in bob.velocity])
        bob.paint()

        # Crosshair

        bob.cross_dx, bob.cross_dy = bob.update_crosshair(bob.cross_dx, bob.cross_dy)
        bob.crosshair.paint()

        # Bullets
        bob.gun.reload_counter += dt
        if bob.shoot() and bob.gun.reload_counter > bob.gun.reload_time:
            bob.gun.reload_counter = 0
            bullets.append(new_bullet(bob, bob.gun.speed))

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

    # Zombies
    for zombie in zombies:
        if bobs[0].rect.colliderect(zombie.rect) or bobs[1].rect.colliderect(zombie.rect):
            died = True
        zombie.rect = zombie.rect.move([t * dt for t in zombie.get_speed(bobs[0].rect)])
        zombie.count += 1
        if zombie.count > 15:
            zombie.get_step()
        zombie.paint(bobs[0].rect)

    if pygame.time.get_ticks() > zombie_timer:
        zombie_timer += zombie_frequency
        zombies.append(generate_new_zombie(0.14))


    pygame.display.update()
    if pygame.key.get_pressed()[K_ESCAPE] or died:
        break

pygame.quit()
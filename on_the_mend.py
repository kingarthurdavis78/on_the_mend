import pygame
from pygame.locals import *
from game_logic import Bob, screen, screen_width, screen_height, unit_length, new_bullet, Gun, generate_new_zombie, zombie_timer, zombie_frequency, Crosshair

pygame.init()

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
mainLoop = True
background = 150, 150, 150

gun = Gun("pistol", 1, 100)
bob = bob = Bob(screen_width / 2, screen_height /2, 0 ,"left", 0.3, gun, Crosshair(Crosshair.image))
zombies = [generate_new_zombie(0.14)]
bullets = []
crosshair = Crosshair(Crosshair.image)

died = False
while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

    # Time elapsed since last iteration
    dt = clock.tick(60)

    screen.fill(background)


    # Zombies
    for zombie in zombies:
        if bob.rect.colliderect(zombie.rect):
            died = True
        zombie.rect = zombie.rect.move([t * dt for t in zombie.get_speed(bob.rect)])
        zombie.count += 1
        if zombie.count > 15:
            zombie.get_step()
        zombie.paint(bob.rect)



    # Bob
    bob.get_velocity(dt)
    bob.get_direction()
    if bob.count > 200:
        bob.get_step()
    bob.rect = bob.rect.move([v * dt for v in bob.velocity])
    bob.paint()

    # Crosshair
    bob.update_crosshair(0, 0)
    # bob.cross_dx, bob.cross_dy = bob.update_crosshair(bob.cross_dx, bob.cross_dy)
    bob.crosshair.paint()

    # Bullets
    bob.gun.reload_counter += dt
    if pygame.mouse.get_pressed()[0] and bob.gun.reload_counter > bob.gun.reload_time:
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

    if pygame.time.get_ticks() > zombie_timer:
        zombie_timer += zombie_frequency
        zombies.append(generate_new_zombie(0.14))


    pygame.display.update()
    if pygame.key.get_pressed()[K_ESCAPE] or died:
        break

pygame.quit()
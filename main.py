# Import the pygame module
import pygame
import sys
# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    K_SPACE,
    QUIT,
)
clock = pygame.time.Clock()
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
# - enemies is used for collision detection and position updates
# - bullets is for the bullet shots by fly
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('backgroundEmpty.png')

class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super(Bullet, self).__init__()
        #self.surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        #self.surf.fill((255, 255, 255))
        plane = pygame.image.load("tank_bulletFly3.png").convert_alpha()
        self.image = pygame.transform.scale(plane, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.speed = 10
        #self.life = 50
        #self.gun = pygame.mixer.Sound("impactPlank_medium_002.ogg")
    def update(self):
        self.rect.x += 5
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

                

# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super(Player, self).__init__()
        self.attack_animation = False
        self.sprites = []
        width = 50
        height = 50
        plane1 = pygame.image.load('planeRed1.png').convert_alpha()
        plane2 = pygame.image.load('planeRed2.png').convert_alpha()
        plane3 = pygame.image.load('planeRed3.png').convert_alpha()

        plane1 = pygame.transform.scale(plane1, (width, height))
        plane2 = pygame.transform.scale(plane2, (width, height))
        plane3 = pygame.transform.scale(plane3, (width, height))
        self.sprites.append(plane1)
        self.sprites.append(plane2)
        self.sprites.append(plane3)

        #self.surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        #self.surf.fill((255, 255, 255))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        #plane = pygame.image.load("planeRed3.png").convert_alpha()
        #self.surf = pygame.transform.scale(plane, (width, height))
        #self.rect = self.surf.get_rect()
        #self.image = pygame.transform.scale(image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        #self.rect.center = (pos_x, pos_y)
        self.life = 50
        self.gun = pygame.mixer.Sound("impactPlank_medium_002.ogg")
        self.shot = 0

    def shoot(self):
        bullet = Bullet(10, 10, self.rect.x, self.rect.y)
        bullets.add(bullet)
        all_sprites.add(bullet)
        #self.bullets.append(bullet)
        self.gun.play()
        self.shot = 0

    # Move the sprite based on keypresses
    def update(self, pressed_keys, shot):
        self.current_sprite += 0.25
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.attack_animation = False
        self.image = self.sprites[int(self.current_sprite)]
        if shot == 1:
            self.shoot()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -4)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 4)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-4, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(4, 0)
        #if pressed_keys[K_SPACE]:
        #    if self.shot == 0 :
        #        self.shot = 1
        #        self.shoot()

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        #self.surf = pygame.Surface((50, 50))
        #ufo = pygame.image.load("shipBlue.png").convert_alpha()
        #self.surf = pygame.transform.scale(ufo, (50, 50))
        #self.surf.fill((255, 0, 255))
        width = 50
        height = 50
        self.sprites = []
        
        ship1 = pygame.image.load('shipGreen.png')
        ship2 = pygame.image.load('shipYellow.png')
        ship3 = pygame.image.load('shipBlue.png')
        ship4 = pygame.image.load('shipPink.png')
        
        ship1 = pygame.transform.scale(ship1, (width, height))
        ship2 = pygame.transform.scale(ship2, (width, height))
        ship3 = pygame.transform.scale(ship3, (width, height))
        ship4 = pygame.transform.scale(ship4, (width, height))
        
        self.sprites.append(ship1)
        self.sprites.append(ship2)
        self.sprites.append(ship3)
        self.sprites.append(ship4)

        self.current_sprite = random.randint(0, 3)
        #print(self.current_sprite)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        pos_x = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)
        pos_y = random.randint(0, SCREEN_HEIGHT)
        self.rect.topleft = [pos_x,pos_y]
        #self.rect = self.surf.get_rect(
        #    center=(
        #        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        #        random.randint(0, SCREEN_HEIGHT),
        #    )
        #)

        self.speed = random.randint(5, 10)

    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Create our 'player'
player = Player(50,50, SCREEN_HEIGHT/2, SCREEN_WIDTH/2)

# Create groups to hold enemy sprites, and every sprite

all_sprites.add(player)

# Variable to keep our main loop running
running = True

# Our main loop
while running:
    shot = 0
    all_sprites.draw(screen)

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                shot = 1
                player.update(pressed_keys, shot)
                shot = 0
        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False
        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, shot)
    # Update bullet pos 
    bullets.update()
    # Update the position of our enemies
    enemies.update()
    
    # Fill the screen with black
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))
    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the loop
        #player.kill()
        pygame.quit()
        #running = False
        #print(enemies)
        #print("collision")
    #if pygame.sprite.spritecollideany(bullets, enemies):
    #    print(enemies)
    #    #enemies.kill()
    
    for bullet in bullets:
        #print(bullet)
        for enemy in enemies :
            if pygame.sprite.collide_rect(bullet, enemy) :
                bullet.kill()
                enemy.kill()
            
        #for bullet in bullets:
        #    if pygame.sprite.spritecollideany(bullet, enemie):
        #        print("touché") 
    # Flip everything to the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
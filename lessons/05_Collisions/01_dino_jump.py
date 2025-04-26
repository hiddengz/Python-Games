"""
Spaceship Asteroid Shooter (Fixed)

Arrow keys = thrust up/down
Spacebar = shoot bullets
Avoid the asteroids!
"""

import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Asteroid Shooter")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images (or make fake ones if missing)
images_dir = Path(__file__).parent / "images"
try:
    spaceship_img = pygame.image.load(images_dir / "ship.png")
except:
    spaceship_img = pygame.Surface((40, 30))
    spaceship_img.fill((0, 0, 255))

try:
    asteroid_img = pygame.image.load(images_dir / "asteroid.png")
except:
    asteroid_img = pygame.Surface((40, 40))
    asteroid_img.fill((150, 150, 150))

spaceship_img = pygame.transform.scale(spaceship_img, (60, 40))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.centery = HEIGHT // 2
        self.velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.velocity -= 0.5
        if keys[pygame.K_DOWN]:
            self.velocity += 0.5

        self.velocity += 0.3  # Gravity
        self.rect.y += self.velocity

        # Stay on screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += 8
        if self.rect.left > WIDTH:
            self.kill()

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = asteroid_img
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(0, HEIGHT - 50)
        self.rotation = 0
        self.rotation_speed = random.choice([-2, -1, 1, 2])

    def update(self):
        self.rect.x -= 5
        self.rotation += self.rotation_speed
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=old_center)

        if self.rect.right < 0:
            self.kill()

# Groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Asteroid timer
ASTEROID_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ASTEROID_EVENT, 1000)  # Spawn every 1 second

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == ASTEROID_EVENT:
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Bullet hits asteroid
    hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)

    # Player hits asteroid
    if pygame.sprite.spritecollide(player, asteroids, False):
        running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()

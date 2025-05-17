import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Load images
rocket_img = pygame.image.load('images/rocket.png')
alien_img = pygame.image.load('images/alien.png')
projectile_img = pygame.image.load('images/projectile.png')
bomb_img = pygame.image.load('images/bomb.gif')
explosion_img = pygame.image.load('images/explosion1.gif')
background_img = pygame.image.load('images/space.png')

# Classes
class Rocket:
    def __init__(self):
        self.image = rocket_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed = 5

    def move(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == 'right' and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Alien:
    def __init__(self):
        self.image = alien_img
        self.rect = self.image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH - 64), 0))
        self.speed = random.randint(1, 3)

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Projectile:
    def __init__(self, x, y):
        self.image = projectile_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("League Invaders")
clock = pygame.time.Clock()

# Game loop
def main():
    rocket = Rocket()
    aliens = [Alien() for _ in range(5)]
    projectiles = []
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectiles.append(Projectile(rocket.rect.centerx, rocket.rect.top))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rocket.move('left')
        if keys[pygame.K_RIGHT]:
            rocket.move('right')

        # Update
        for alien in aliens:
            alien.move()
            if alien.rect.top > SCREEN_HEIGHT:
                aliens.remove(alien)
                aliens.append(Alien())

        for projectile in projectiles:
            projectile.move()
            if projectile.rect.bottom < 0:
                projectiles.remove(projectile)

        # Draw
        screen.blit(background_img, (0, 0))
        rocket.draw(screen)
        for alien in aliens:
            alien.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
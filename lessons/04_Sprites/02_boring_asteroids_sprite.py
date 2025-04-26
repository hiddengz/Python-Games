import pygame
import math
from pathlib import Path  # ADD THIS

# SET THE ASSETS DIRECTORY
assets = Path(__file__).parent / "images"  # ADD THIS

class Settings:
    """Class to store game configuration."""
    width = 800
    height = 600
    fps = 60
    triangle_size = 20
    projectile_speed = 5
    projectile_size = 11
    shoot_delay = 250
    colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0)}

class Spaceship(pygame.sprite.Sprite):
    """Class representing the spaceship."""
    def __init__(self, settings, position):
        super().__init__()
        self.game = None
        self.settings = settings
        self.angle = 0
        self.original_image = self.create_spaceship_image()
        self.velocity = pygame.Vector2(0, 0)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=position)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = self.settings.shoot_delay  

    def create_spaceship_image(self):
        """Creates the spaceship shape as a surface."""
        image = pygame.Surface((self.settings.triangle_size * 2, self.settings.triangle_size * 2), pygame.SRCALPHA)
        points = [
            (self.settings.triangle_size, 0),
            (0, self.settings.triangle_size * 2),
            (self.settings.triangle_size * 2, self.settings.triangle_size * 2),
        ]
        pygame.draw.polygon(image, self.settings.colors["white"], points)
        return image

    def ready_to_shoot(self):
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            return True
        return False

    def fire_projectile(self):
        new_projectile = Projectile(
            self.settings,
            position=self.rect.center,
            angle=self.angle,
            velocity=self.settings.projectile_speed,
        )
        self.game.add(new_projectile)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= 5
        if keys[pygame.K_RIGHT]:
            self.angle += 5
        if keys[pygame.K_SPACE] and self.ready_to_shoot():
            self.fire_projectile()
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center += self.velocity
        super().update()

class Projectile(pygame.sprite.Sprite):
    """Class to handle projectile movement and drawing."""
    def __init__(self, settings, position, velocity, angle):
        super().__init__()
        self.game = None
        self.settings = settings
        self.velocity = pygame.Vector2(0, -1).rotate(angle) * velocity
        self.image = pygame.Surface(
            (self.settings.projectile_size, self.settings.projectile_size),
            pygame.SRCALPHA,
        )
        half_size = self.settings.projectile_size // 2
        pygame.draw.circle(
            self.image,
            self.settings.colors["red"],
            center=(half_size + 1, half_size + 1),
            radius=half_size,
        )
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center += self.velocity

class Game:
    """Class to manage the game loop and objects."""
    def __init__(self, settings):
        pygame.init()
        pygame.key.set_repeat(1250, 1250)
        self.settings = settings
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption("Really Boring Asteroids")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()

    def add(self, sprite):
        sprite.game = self
        self.all_sprites.add(sprite)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(self.settings.colors["black"])
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.fps)
        pygame.quit()

# === NEW CLASS for AlienSpaceship ===
class AlienSpaceship(Spaceship):
    def create_spaceship_image(self):
        """Override to load a spaceship image instead of a triangle."""
        return pygame.image.load(assets / 'alien1.gif')  # Make sure 'alien1.gif' exists in 'images' folder

# === MAIN PROGRAM ===
if __name__ == "__main__":
    settings = Settings()
    game = Game(settings)

    # USE AlienSpaceship instead of Spaceship
    spaceship = AlienSpaceship(
        settings, position=(settings.width // 2, settings.height // 2)
    )

    game.add(spaceship)
    game.run()

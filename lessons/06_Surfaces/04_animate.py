import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path
import sys

images = Path(__file__).parent / 'images'

def scale_sprites(sprites, scale):
    return [pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale)) for sprite in sprites]

class Frog(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.sprites = sprites
        self.index = 0
        self.image = self.sprites[self.index]
        self.rect = self.image.get_rect(center=(320, 400))
        self.vector = pygame.math.Vector2(0, -1)
        self.speed = 10
        self.is_jumping = False
        self.velocity = pygame.math.Vector2(0, 0)
        self.frames_per_image = 6
        self.frame_count = 0

    def update(self):
        if self.is_jumping:
            self.rect.center += self.velocity
        else:
            self.frame_count += 1
            if self.frame_count % self.frames_per_image == 0:
                self.index = (self.index + 1) % len(self.sprites)
                self.image = self.sprites[self.index]

    def start_jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.index = 0
            self.image = self.sprites[self.index]
            self.velocity = self.vector * self.speed

    def stop_jump(self):
        self.is_jumping = False
        self.velocity = pygame.math.Vector2(0, 0)
        self.index = 0
        self.image = self.sprites[self.index]

class Alligator(pygame.sprite.Sprite):
    def __init__(self, sprites, target):
        super().__init__()
        self.sprites = sprites
        self.target = target
        self.index = 0
        self.image = self.draw_alligator()
        self.rect = self.image.get_rect(center=(320, 100))
        self.speed = 2
        self.frames_per_image = 6
        self.frame_count = 0

    def update(self):
        # Move towards frog
        direction = pygame.math.Vector2(self.target.rect.center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 1:
            direction = direction.normalize()
            self.rect.center += direction * self.speed
        
        # Animate
        self.frame_count += 1
        if self.frame_count % self.frames_per_image == 0:
            self.index = (self.index + 1) % (len(self.sprites) - 2)
            self.image = self.draw_alligator()

    def draw_alligator(self):
        width = self.sprites[0].get_width()
        height = self.sprites[0].get_height()
        composed_image = pygame.Surface((width * 3, height), pygame.SRCALPHA)
        composed_image.blit(self.sprites[0], (0, 0))
        composed_image.blit(self.sprites[1], (width, 0))
        composed_image.blit(self.sprites[(self.index + 2) % len(self.sprites)], (width * 2, 0))
        return composed_image

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Frog vs Alligator")
    clock = pygame.time.Clock()

    # Load sprites
    spritesheet = SpriteSheet(images / 'spritesheet.png', (16, 16))
    frog_sprites = scale_sprites(spritesheet.load_strip(0, 4, colorkey=-1), 4)
    allig_sprites = scale_sprites(spritesheet.load_strip((0, 4), 7, colorkey=-1), 4)

    frog = Frog(frog_sprites)
    alligator = Alligator(allig_sprites, frog)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(frog)
    all_sprites.add(alligator)

    font = pygame.font.SysFont(None, 60)
    game_over = False

    running = True
    while running:
        screen.fill((0, 0, 139))  # Dark blue background
        keys = pygame.key.get_pressed()

        # Handle input for frog direction
        if keys[pygame.K_LEFT]:
            frog.vector = pygame.math.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            frog.vector = pygame.math.Vector2(1, 0)
        elif keys[pygame.K_UP]:
            frog.vector = pygame.math.Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            frog.vector = pygame.math.Vector2(0, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    frog.start_jump()

        if not game_over:
            all_sprites.update()

            if frog.is_jumping:
                # Stop jump after distance
                frog.speed -= 0.5
                if frog.speed <= 0:
                    frog.stop_jump()
                    frog.speed = 10

            # Check collision
            if pygame.sprite.collide_rect(frog, alligator):
                game_over = True

        all_sprites.draw(screen)

        if game_over:
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, (200, 220))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

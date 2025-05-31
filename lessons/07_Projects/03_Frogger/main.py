import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 448  # 14 tiles * 32px
SCREEN_HEIGHT = 512  # 16 tiles * 32px
TILE_SIZE = 32
FPS = 30
CAR_COUNT_PER_LANE = 1  # Reduced number of cars per lane

# Colors
GREEN = (34, 177, 76)
BLUE = (0, 162, 232)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROAD_GRAY = (50, 50, 50)
RIVER_BLUE = (30, 144, 255)
SAFE_ZONE = (0, 200, 0)
FROG_COLOR = (0, 255, 0)
CAR_COLOR = (200, 0, 0)
LOG_COLOR = (139, 69, 19)
TURTLE_COLOR = (0, 128, 255)

# Game settings
LIVES = 3
TIME_LIMIT = 30  # seconds
SAFE_ZONES = 5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Classes
class Frog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(FROG_COLOR)
        self.rect = self.image.get_rect()
        self.start_pos = (SCREEN_WIDTH // 2 - TILE_SIZE // 2, SCREEN_HEIGHT - TILE_SIZE)
        self.rect.topleft = self.start_pos
        self.on_log = None

    def move(self, dx, dy):
        new_rect = self.rect.move(dx * TILE_SIZE, dy * TILE_SIZE)
        if 0 <= new_rect.left < SCREEN_WIDTH and 0 <= new_rect.top < SCREEN_HEIGHT:
            self.rect = new_rect

    def reset(self):
        self.rect.topleft = self.start_pos
        self.on_log = None

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, length=1):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE * length, TILE_SIZE))
        self.image.fill(CAR_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

class Log(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, length=2):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE * length, TILE_SIZE))
        self.image.fill(LOG_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

class Turtle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, length=2):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE * length, TILE_SIZE))
        self.image.fill(TURTLE_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.dive_timer = random.randint(120, 240)
        self.diving = False

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

        self.dive_timer -= 1
        if self.dive_timer <= 0:
            self.diving = not self.diving
            self.dive_timer = random.randint(120, 240)

    def is_safe(self):
        return not self.diving

# Helper functions
def draw_background():
    # Draw safe zones
    screen.fill(SAFE_ZONE)
    # Draw river
    pygame.draw.rect(screen, RIVER_BLUE, (0, TILE_SIZE * 2, SCREEN_WIDTH, TILE_SIZE * 5))
    # Draw road
    pygame.draw.rect(screen, ROAD_GRAY, (0, TILE_SIZE * 7, SCREEN_WIDTH, TILE_SIZE * 5))
    # Draw starting area
    pygame.draw.rect(screen, GREEN, (0, TILE_SIZE * 12, SCREEN_WIDTH, TILE_SIZE * 4))
    # Draw safe zone homes
    for i in range(SAFE_ZONES):
        x = i * (SCREEN_WIDTH // SAFE_ZONES) + (SCREEN_WIDTH // SAFE_ZONES - TILE_SIZE) // 2
        pygame.draw.rect(screen, BLACK, (x, 0, TILE_SIZE, TILE_SIZE))

def draw_ui(lives, score, timer):
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    timer_text = font.render(f"Time: {timer}", True, WHITE)
    screen.blit(lives_text, (10, SCREEN_HEIGHT - 30))
    screen.blit(score_text, (180, SCREEN_HEIGHT - 30))
    screen.blit(timer_text, (350, SCREEN_HEIGHT - 30))

def check_safe_zone(frog, filled_zones):
    for i in range(SAFE_ZONES):
        x = i * (SCREEN_WIDTH // SAFE_ZONES) + (SCREEN_WIDTH // SAFE_ZONES - TILE_SIZE) // 2
        zone_rect = pygame.Rect(x, 0, TILE_SIZE, TILE_SIZE)
        if frog.rect.colliderect(zone_rect) and not filled_zones[i]:
            filled_zones[i] = True
            return True, i
    return False, -1

def main():
    frog = Frog()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(frog)

    # Cars: y positions for road lanes
    car_lanes = [TILE_SIZE * i for i in range(7, 12)]
    cars = pygame.sprite.Group()
    for i, y in enumerate(car_lanes):
        x = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
        speed = random.choice([-4, 4]) if i % 2 == 0 else random.choice([-3, 3])
        car = Car(x, y, speed, length=random.choice([1, 2]))
        cars.add(car)
        all_sprites.add(car)

    # Logs and turtles: y positions for river lanes
    river_lanes = [TILE_SIZE * i for i in range(2, 7)]
    logs = pygame.sprite.Group()
    turtles = pygame.sprite.Group()
    for i, y in enumerate(river_lanes):
        for j in range(2):
         x = random.randint(0, SCREEN_WIDTH - TILE_SIZE * 2)
        speed = random.choice([-2, 2])
        if i % 2 == 0:
            log = Log(x, y, speed=speed, length=random.choice([2, 3]))
            logs.add(log)
            all_sprites.add(log)
        else:
            turtle = Turtle(x, y, speed=speed, length=2)
            turtles.add(turtle)
            all_sprites.add(turtle)

    lives = LIVES
    score = 0
    timer = TIME_LIMIT * FPS
    filled_zones = [False] * SAFE_ZONES
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    frog.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    frog.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    frog.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    frog.move(1, 0)

        # Update
        all_sprites.update()

        # Move frog with log/turtle if standing on one
        frog.on_log = None
        on_river = TILE_SIZE * 2 <= frog.rect.top < TILE_SIZE * 7
        if on_river:
            on_object = False
            for log in logs:
                if frog.rect.colliderect(log.rect):
                    frog.rect.x += log.speed
                    frog.on_log = log
                    on_object = True
                    break
            for turtle in turtles:
                if frog.rect.colliderect(turtle.rect) and turtle.is_safe():
                    frog.rect.x += turtle.speed
                    frog.on_log = turtle
                    on_object = True
                    break
            if not on_object:
                lives -= 1
                frog.reset()
                timer = TIME_LIMIT * FPS
                continue
            # If on a diving turtle
            for turtle in turtles:
                if frog.rect.colliderect(turtle.rect) and not turtle.is_safe():
                    lives -= 1
                    frog.reset()
                    timer = TIME_LIMIT * FPS
                    break

        # Collision with cars
        if pygame.sprite.spritecollideany(frog, cars):
            lives -= 1
            frog.reset()
            timer = TIME_LIMIT * FPS
            continue

        # Check for safe zone
        reached, zone = check_safe_zone(frog, filled_zones)
        if reached:
            score += 100
            frog.reset()
            timer = TIME_LIMIT * FPS
            if all(filled_zones):
                # Next level
                filled_zones = [False] * SAFE_ZONES
                score += 500

        # Timer
        timer -= 1
        if timer <= 0:
            lives -= 1
            frog.reset()
            timer = TIME_LIMIT * FPS

        # Game over
        if lives <= 0:
            screen.fill(BLACK)
            over_text = font.render("GAME OVER", True, WHITE)
            screen.blit(over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 16))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            continue

        # Draw
        draw_background()
        all_sprites.draw(screen)
        # Draw filled safe zones
        for i, filled in enumerate(filled_zones):
            if filled:
                x = i * (SCREEN_WIDTH // SAFE_ZONES) + (SCREEN_WIDTH // SAFE_ZONES - TILE_SIZE) // 2
                pygame.draw.rect(screen, FROG_COLOR, (x, 0, TILE_SIZE, TILE_SIZE))
        draw_ui(lives, score, timer // FPS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
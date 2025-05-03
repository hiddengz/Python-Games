import pygame
import sys
import random
from pathlib import Path

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
assets = Path(__file__).parent / 'images'  # Updated path to the 'images' folder
bg_img = pygame.image.load(assets / 'background.png')
base_img = pygame.image.load(assets / 'base.png')

bird_imgs = [
    pygame.image.load(assets / 'bluebird-downflap.png'),
    pygame.image.load(assets / 'bluebird-midflap.png'),
    pygame.image.load(assets / 'bluebird-upflap.png')
]

pipe_img = pygame.image.load(assets / 'pipe-green.png')
pipe_top_img = pygame.transform.flip(pipe_img, False, True)

# Game variables
gravity = 0.25
bird_movement = 0
bird_index = 0
bird_img = bird_imgs[bird_index]
bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT//2))

def draw_background():
    screen.blit(bg_img, (0, 0))
    screen.blit(bg_img, (bg_img.get_width(), 0))

def draw_base(x):
    screen.blit(base_img, (x, SCREEN_HEIGHT - base_img.get_height()))
    screen.blit(base_img, (x + base_img.get_width(), SCREEN_HEIGHT - base_img.get_height()))

def create_pipe():
    gap = 150
    height = random.randint(150, 400)
    bottom = pipe_img.get_rect(midtop=(SCREEN_WIDTH + 100, height))
    top = pipe_top_img.get_rect(midbottom=(SCREEN_WIDTH + 100, height - gap))
    return top, bottom

def move_pipes(pipes):
    return [(p[0].move(-5, 0), p[1].move(-5, 0)) for p in pipes]

def draw_pipes(pipes):
    for top, bottom in pipes:
        screen.blit(pipe_top_img, top)
        screen.blit(pipe_img, bottom)

def check_collision(pipes):
    for top, bottom in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= SCREEN_HEIGHT - base_img.get_height():
        return False
    return True

# Timer for pipe spawning
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# Game loop
pipes = []
score = 0
base_x = 0
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                bird_rect.center = (100, SCREEN_HEIGHT//2)
                bird_movement = 0
                pipes.clear()
                game_active = True
                score = 0

        if event.type == SPAWNPIPE:
            pipes.append(create_pipe())

    draw_background()

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        bird_index = (bird_index + 1) % 3
        bird_img = bird_imgs[bird_index]
        screen.blit(bird_img, bird_rect)

        # Pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Collision
        game_active = check_collision(pipes)

        # Score
        for pipe in pipes:
            if pipe[0].centerx == bird_rect.centerx:
                score += 1

    else:
        font = pygame.font.SysFont(None, 48)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (100, 250))

    # Base
    base_x -= 5
    if base_x <= -base_img.get_width():
        base_x = 0
    draw_base(base_x)

    pygame.display.update()
    clock.tick(60)

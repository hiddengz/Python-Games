"""
Jump with Space

This program demonstrates gravity and lets the player jump by pressing the spacebar.
"""
import pygame
from dataclasses import dataclass

# Initialize Pygame
pygame.init()

@dataclass
class GameSettings:
    screen_width: int = 500
    screen_height: int = 500
    player_size: int = 10
    player_x: int = 100
    gravity: float = 0.3
    jump_velocity: int = 10
    white: tuple = (255, 255, 255)
    black: tuple = (0, 0, 0)
    tick_rate: int = 60

# Initialize game settings
settings = GameSettings()

# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Jump with Space")

# Define player
player = pygame.Rect(
    settings.player_x,
    settings.screen_height - settings.player_size,
    settings.player_size,
    settings.player_size
)

player_y_velocity = 0
is_jumping = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check key press for da jump hopefully
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        player_y_velocity = -settings.jump_velocity
        is_jumping = True

    # Apply the gravity
    player_y_velocity += settings.gravity
    player.y += player_y_velocity

    # Collision with the ground
    if player.bottom >= settings.screen_height:
        player.bottom = settings.screen_height
        player_y_velocity = 0
        is_jumping = False

    # Drawing
    screen.fill(settings.white)
    pygame.draw.rect(screen, settings.black, player)
    pygame.display.flip()
    clock.tick(settings.tick_rate)

pygame.quit()

import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path
import random

# Set up image directory
images = Path(__file__).parent / 'images'

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame Transformations")

# Build a grid of positions
grid = []
for y in range(0, screen.get_height(), 48):
    for x in range(0, screen.get_width(), 48):
        grid.append((x, y))
print(len(grid))
print(grid[51], grid[100])

# Load the sprite sheet
filename = images / 'spritesheet.png'  # Make sure this file exists
cellsize = (16, 16)
ss = SpriteSheet(filename, cellsize)

# Get images from the sprite sheet
log = ss.compose_horiz([24, 25, 26])
alig = ss.compose_horiz([32, 33, 15])
frog_g = ss.image_at(4)
frog_p = ss.image_at(76)
fly = ss.image_at(57)

# Original image
screen.blit(alig, grid[14])

# Scale up 3x
alig3x = pygame.transform.scale(alig, (alig.get_width() * 3, alig.get_height() * 3))
screen.blit(alig3x, grid[15])

# Flip horizontally
alig3x_hflip = pygame.transform.flip(alig3x, True, False)
screen.blit(alig3x_hflip, grid[19])

# Flip vertically
alig3x_vflip = pygame.transform.flip(alig3x, False, True)
screen.blit(alig3x_vflip, grid[23])

# 2x increase using scale2x
frog2x = pygame.transform.scale2x(frog_g)
screen.blit(frog2x, grid[42])

# Scale up by a factor of 3
frog4x = pygame.transform.scale_by(frog2x, 3)
screen.blit(frog4x, grid[43])

# Scale non-uniformly (wide frog)
frog_w = pygame.transform.scale(frog_g, (frog_g.get_width() * 6, frog_g.get_height() * 2))
screen.blit(frog_w, grid[45])

# Repeatedly rotate transformed image (compounding distortion)
frog_p2x = pygame.transform.scale2x(frog_p)
for i in range(5):
    frog_p2x = pygame.transform.rotate(frog_p2x, 30)
    screen.blit(frog_p2x, grid[70 + (i * 2)])

# Rotate from original each time (no distortion buildup)
frog_p2x = pygame.transform.scale2x(frog_p)
for i in range(5):
    frog_rot = pygame.transform.rotate(frog_p2x, 30 * i)
    screen.blit(frog_rot, grid[112 + (i * 2)])

# Show everything
pygame.display.flip()

# Event loop
while True:
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
        break
    pygame.time.Clock().tick(60)

pygame.quit()

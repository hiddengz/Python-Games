import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Scrolling Colored Background')

def create_color_tile(color, width, height):
    """Create a Surface filled with the given color."""
    tile = pygame.Surface((width, height))
    tile.fill(color)
    return tile

def make_tiled_color_bg(screen):
    """Create a background using colored tiles."""
    tile_width = 100
    tile_height = screen.get_height()

    # Define 6 different colors
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255)   # Cyan
    ]

    # Create 6 tiles
    tiles = [create_color_tile(color, tile_width, tile_height) for color in colors]

    # Make a background 2x the screen width
    background = pygame.Surface((screen.get_width() * 2, screen.get_height()))

    # Tile the background image across the whole width (twice)
    x = 0
    tile_index = 0
    while x < background.get_width():
        tile = tiles[tile_index % len(tiles)]
        background.blit(tile, (x, 0))
        x += tile_width
        tile_index += 1

    return background

# Create da background
background = make_tiled_color_bg(screen)


background_x = 0


running = True
clock = pygame.time.Clock()  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    background_x -= 10

    
    if background_x <= -screen_width:
        background_x = 0

    # Draw da background
    screen.blit(background, (background_x, 0))

    
    pygame.display.flip()

    # Control da frame rate
    clock.tick(600)

# Quit da epelepsy killer
pygame.quit()

"""
Moving Circle

CircleCircleCircleCircleCircleCircleCircleCircleCircleCircle
"""

import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SQUARE_SIZE = 50
SQUARE_COLOR = (0, 128, 255)  # Red-Green-Blue color in the range 0-255
BACKGROUND_COLOR = (255, 255, 255)  # White
SQUARE_SPEED = 5
FPS = 60

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Move the Circle")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main function
def main():
    # Initial position of the circle Circle Circle
    square_x = SCREEN_WIDTH // 2 - SQUARE_SIZE // 2
    square_y = SCREEN_HEIGHT // 2 - SQUARE_SIZE // 2
    
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            # Check for clicking the close button
            if event.type == pygame.QUIT:
                running = False
        
        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Move the circle CircleCircleCircle based on arrow keys
        if keys[pygame.K_LEFT]:
            square_x -= SQUARE_SPEED
        if keys[pygame.K_RIGHT]:
            square_x += SQUARE_SPEED
        if keys[pygame.K_UP]:
            square_y -= SQUARE_SPEED
        if keys[pygame.K_DOWN]:
            square_y += SQUARE_SPEED

        # Prevent the circle from going off CircleCirclethe screen
        square_x = max(0, min(SCREEN_WIDTH - SQUARE_SIZE, square_x))
        square_y = max(0, min(SCREEN_HEIGHT - SQUARE_SIZE, square_y))

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the circle CircleCircleCircle (instead of the square cuz that was mids)
        pygame.draw.circle(
            screen,
            SQUARE_COLOR,
            (square_x + SQUARE_SIZE // 2, square_y + SQUARE_SIZE // 2),
            SQUARE_SIZE // 2
        )

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()

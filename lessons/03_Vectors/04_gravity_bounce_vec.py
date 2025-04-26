"""
Gravity bounce using Vectors with Drag added.

This version of the Gravity Bounce program uses Pygame's Vector2 class to handle
the player's position and velocity. Now includes drag to slow down the player.
"""

import pygame
from dataclasses import dataclass


class Colors:
    """Constants for Colors"""
    WHITE = (0, 0, 170)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PLAYER_COLOR = (255, 0, 0)
    BACKGROUND_COLOR = (0, 200, 230)


@dataclass
class GameSettings:
    """Settings for the game"""
    width: int = 500
    height: int = 500
    gravity: float = 0.4
    player_start_x: int = 100
    player_start_y: int = None
    player_v_y: float = 0  # Initial y velocity
    player_v_x: float = 4  # Initial x velocity
    player_width: int = 20
    player_height: int = 20
    player_jump_velocity: float = 20
    frame_rate: int = 15
    drag_strength: float = 0.05  # <-- Added drag strength setting!


class Game:
    """Main object for the top level of the game. Holds the main loop and other
    update, drawing and collision methods that operate on multiple other
    objects, like the player and obstacles."""
    
    def __init__(self, settings: GameSettings):
        pygame.init()

        self.settings = settings
        self.running = True

        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.clock = pygame.time.Clock()

        # Turn Gravity into a vector
        self.gravity = pygame.Vector2(0, self.settings.gravity)

    def run(self):
        """Main game loop"""
        player = Player(self)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            player.update()

            self.screen.fill(Colors.BACKGROUND_COLOR)
            player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.settings.frame_rate)

        pygame.quit()


class Player:
    """Player class, just a bouncing rectangle"""

    def __init__(self, game: Game):
        self.game = game
        settings = self.game.settings

        self.width = settings.player_width
        self.height = settings.player_height
    
        # Vector for our jump velocity, which is just up
        self.v_jump = pygame.Vector2(0, -settings.player_jump_velocity)

        # Player position
        self.pos = pygame.Vector2(
            settings.player_start_x, 
            settings.player_start_y if settings.player_start_y is not None else settings.height - self.height
        )
        
        # Player's velocity
        self.vel = pygame.Vector2(settings.player_v_x, settings.player_v_y)

        # Drag scalar (how strong drag is)
        self.drag_scalar = settings.drag_strength


    # Direction functions
    
    def going_up(self):
        """Check if the player is going up"""
        return self.vel.y < 0
    
    def going_down(self):
        """Check if the player is going down"""
        return self.vel.y > 0
    
    def going_left(self):
        """Check if the player is going left"""
        return self.vel.x < 0
    
    def going_right(self):
        """Check if the player is going right"""
        return self.vel.x > 0
    
    
    # Location Functions
    
    def at_top(self):
        """Check if the player is at the top of the screen"""
        return self.pos.y <= 0
    
    def at_bottom(self):
        """Check if the player is at the bottom of the screen"""
        return self.pos.y >= self.game.settings.height - self.height

    def at_left(self):
        """Check if the player is at the left of the screen"""
        return self.pos.x <= 0
    
    def at_right(self):
        """Check if the player is at the right of the screen"""
        return self.pos.x >= self.game.settings.width - self.width
    
    # Updates
    
    def update(self):
        """Update player position, continuously jumping"""
        self.update_jump()
        self.update_v()
        self.update_pos()
        
    def update_v(self):
        """Update the player's velocity based on gravity, drag, and bounce"""

        self.vel += self.game.gravity  # Add gravity to the velocity

        # --- Apply drag ---
        if self.vel.length() > 0:
            drag = self.vel * -self.drag_scalar
            self.vel += drag

        # Bounce logic
        if self.at_bottom() and self.going_down():
            self.vel.y = 0

        if self.at_top() and self.going_up():
            self.vel.y = -self.vel.y

        if (self.at_left() and self.going_left()) or (self.at_right() and self.going_right()):
            self.vel.x = -self.vel.x
            
    def update_pos(self):
        """Update the player's position based on velocity"""
        self.pos += self.vel  # Update the player's position based on the current velocity

        if self.at_bottom():
            self.pos.y = self.game.settings.height - self.height

        if self.at_top():
            self.pos.y = 0

        if self.at_left():
            self.pos.x = 0
  
        elif self.at_right():
            self.pos.x = self.game.settings.width - self.width

    def update_jump(self):
        """Handle the player's jumping logic"""
        if self.at_bottom():
            self.vel += self.v_jump

    def draw(self, screen):
        pygame.draw.rect(screen, Colors.PLAYER_COLOR, (self.pos.x, self.pos.y, self.width, self.height))


# Main program
settings = GameSettings()
game = Game(settings)
game.run()

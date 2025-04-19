import pygame

class Colors:
    """Constants for Colors""" #COOLORS COLORS COOLARES!!!!
    WHITE = (0, 0, 100)
    BLACK = (0, 0, 0)
    RED = (255, 0, 100)
    BLUE = (0, 255, 255)
    GREEN = (0, 255, 0)

class GameSettings:
    """Settings for the game"""
    width: int = 500
    height: int = 500
    gravity: float = 0.3
    player_width: int = 20
    player_height: int = 20
    player_jump_velocity: float = 15

class Game:
    """Main game class that runs the loop and holds game objects"""
    
    def __init__(self, settings: GameSettings):
        pygame.init()
        self.settings = settings
        self.running = True
        self.screen = pygame.display.set_mode((settings.width, settings.height))
        self.clock = pygame.time.Clock()
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def run(self):
        """Main game loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            self.screen.fill(Colors.WHITE)

            for player in self.players:
                player.update()
                player.draw(self.screen)
                
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

class Player:
    """Player class, a bouncing rectangle"""

    def __init__(self, game: Game, x: int, y: int, v_x: float, v_y: float, color):
        self.game = game
        settings = game.settings

        self.width = settings.player_width
        self.height = settings.player_height
        self.color = color

        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y

        self.is_jumping = False
        self.v_jump = settings.player_jump_velocity

    def update(self):
        self.update_jump()
        self.update_y()
        self.update_x()

    def update_y(self):
        self.v_y += self.game.settings.gravity
        self.y += self.v_y

        if self.y >= self.game.settings.height - self.height:
            self.y = self.game.settings.height - self.height
            self.v_y = 0
            self.is_jumping = False

    def update_x(self):
        self.x += self.v_x

        if self.x <= 0:
            self.x = 0
            self.v_x = -self.v_x
        elif self.x >= self.game.settings.width - self.width:
            self.x = self.game.settings.width - self.width
            self.v_x = -self.v_x

    def update_jump(self):
        if not self.is_jumping:
            self.v_y = -self.v_jump
            self.is_jumping = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Set up game
settings = GameSettings()
game = Game(settings)

# da story of the 2 tick tac colored players
p1 = Player(game, x=100, y=400, v_x=6, v_y=0, color=Colors.RED)
p2 = Player(game, x=300, y=100, v_x=4, v_y=1, color=Colors.BLUE)

game.add_player(p1)
game.add_player(p2)

# Run the game
game.run()

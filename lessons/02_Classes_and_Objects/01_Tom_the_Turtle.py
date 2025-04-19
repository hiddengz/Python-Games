import math
import pygame

def event_loop():
    """Wait until user closes the window"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

class Turtle:
    def __init__(self, screen, x: int, y: int):
        self.x = x
        self.y = y
        self.screen = screen
        self.angle = 0  # Angle in degrees, starting facing right
        self.pen_down = True  # Default is the pen is down (drawing)

    def forward(self, distance):
        # Calculate new position based on current angle
        radian_angle = math.radians(self.angle)

        start_x = self.x  # Save the starting position
        start_y = self.y

        # Calculate the new position displacement
        dx = math.cos(radian_angle) * distance
        dy = math.sin(radian_angle) * distance

        # Update the turtle's position
        self.x += dx
        self.y -= dy

        # Draw line to the new position if the pen is down
        if self.pen_down:
            pygame.draw.line(self.screen, black, (start_x, start_y), (self.x, self.y), 2)

    def left(self, angle):
        # Turn left by adjusting the angle counterclockwise
        self.angle = (self.angle + angle) % 360

    def right(self, angle):
        # Turn right by adjusting the angle clockwise
        self.left(-angle)

    def raise_pen(self):
        self.pen_down = False

    def lower_pen(self):
        self.pen_down = True

    def set_color(self, color):
        self.color = color

class ColoredTurtle(Turtle):
    def __init__(self, screen, x: int, y: int, color=(0, 0, 0)):
        super().__init__(screen, x, y)
        self.color = color  # Default color is black

    def forward(self, distance):
        # Override the forward method to draw with the turtle's current color
        radian_angle = math.radians(self.angle)

        start_x = self.x
        start_y = self.y

        dx = math.cos(radian_angle) * distance
        dy = math.sin(radian_angle) * distance

        self.x += dx
        self.y -= dy

        if self.pen_down:
            pygame.draw.line(self.screen, self.color, (start_x, start_y), (self.x, self.y), 2)

# Main loop
pygame.init()

# Screen dimensions and setup
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Colored Turtle Drawing")


white = (255, 255, 255)
black = (0, 0, 0)

screen.fill(white)


turtle = ColoredTurtle(screen, screen.get_width() // 2, screen.get_height() // 2, color=(0, 0, 255))

# Draw a square with the *NEW AMAZING TOM* colored turtle
for _ in range(4):
    turtle.forward(100)  # Move forward by 100 pixels
    turtle.left(90)  # Turn left by 90 degrees


turtle.raise_pen()  # Lift the pen so no drawing occurs
turtle.right(45)  # Turn right 45 degrees
turtle.forward(50)  # Move forward without drawing
turtle.lower_pen()  # Put the pen down again

# new shape and new color cuz yes!
turtle.set_color((255, 0, 0))  # Change the turtle's color to red
for _ in range(4):
    turtle.forward(50)
    turtle.left(90)

# Display the drawing
pygame.display.flip()

# Wait to quit
event_loop()

# Quit Pygame
pygame.quit()

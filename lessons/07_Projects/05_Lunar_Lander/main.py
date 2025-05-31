import pygame
import math
import random


# --- Constants ---
WIDTH, HEIGHT = 600, 600
FPS = 60

GRAVITY = 0.01
THRUST = 0.15
ROTATE_SPEED = 2  # degrees per frame
FUEL_CONSUMPTION = 0.2

SAFE_LANDING_VSPEED = 5.0
SAFE_LANDING_HSPEED = 5.0
SAFE_LANDING_ANGLE = 30  # degrees

START_FUEL = 100

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 10)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 128, 255)

# --- Classes ---
class LunarModule:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.angle = 0  # degrees
        self.fuel = START_FUEL
        self.alive = True
        self.landed = False

    def update(self, keys):
        if not self.alive or self.landed:
            return

        # Rotation
        if keys[pygame.K_LEFT]:
            self.angle -= ROTATE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle += ROTATE_SPEED

        # Thrust
        thrusting = keys[pygame.K_UP] and self.fuel > 0
        if thrusting:
            rad = math.radians(self.angle)
            ax = -math.sin(rad) * THRUST
            ay = -math.cos(rad) * THRUST
            self.vx += ax
            self.vy += ay
            self.fuel = max(0, self.fuel - FUEL_CONSUMPTION)

        # Gravity
        self.vy += GRAVITY

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Keep inside screen
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self, surf):
        # Draw as a triangle
        rad = math.radians(self.angle)
        points = []
        for dx, dy in [(0, -20), (-10, 10), (10, 10)]:
            px = self.x + dx * math.cos(rad) - dy * math.sin(rad)
            py = self.y + dx * math.sin(rad) + dy * math.cos(rad)
            points.append((px, py))
        pygame.draw.polygon(surf, WHITE, points)
        # Draw flame if thrusting
        if self.alive and self.fuel > 0 and pygame.key.get_pressed()[pygame.K_UP]:
            fx = self.x + 0 * math.cos(rad) - 18 * math.sin(rad)
            fy = self.y + 0 * math.sin(rad) + 18 * math.cos(rad)
            pygame.draw.line(surf, YELLOW, (self.x, self.y+15), (fx, fy+20), 4)

class LandingZone:
    def __init__(self, x, width, difficulty):
        self.x = x
        self.width = width
        self.difficulty = difficulty  # 1=easy, 2=medium, 3=hard

    def draw(self, surf, surface_y):
        color = GREEN if self.difficulty == 1 else YELLOW if self.difficulty == 2 else RED
        pygame.draw.rect(surf, color, (self.x, surface_y-5, self.width, 10))

def generate_surface():
    # Generate a rough surface with 3 landing zones
    points = []
    landing_zones = []
    surface_y = HEIGHT - 80
    x = 0
    while x < WIDTH:
        if len(landing_zones) < 3 and random.random() < 0.2:
            # Place a landing zone
            width = random.choice([80, 50, 30])
            difficulty = 1 if width == 80 else 2 if width == 50 else 3
            landing_zones.append(LandingZone(x, width, difficulty))
            for i in range(width):
                points.append((x+i, surface_y))
            x += width
        else:
            y = surface_y + random.randint(-20, 20)
            points.append((x, y))
            x += 10
    return points, landing_zones, surface_y

def draw_surface(surf, points):
    pygame.draw.lines(surf, GRAY, False, points, 3)

def get_surface_y_at_x(points, x):
    # Find the y value of the surface at a given x by linear interpolation
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= x <= x2 or x2 <= x <= x1:
            if x2 != x1:
                t = (x - x1) / (x2 - x1)
                return y1 + t * (y2 - y1)
            else:
                return y1
    return HEIGHT  # fallback

def check_landing(module, points, landing_zones, surface_y):
    # Get the surface y directly under the module
    surface_y_at_x = get_surface_y_at_x(points, module.x)
    # Check if module is touching the surface
    if module.y + 10 >= surface_y_at_x:
        # Check if over a landing zone and on the flat part
        for zone in landing_zones:
            if zone.x <= module.x <= zone.x + zone.width:
                # Check if the surface under the lander is flat (i.e., part of the pad)
                pad_y = get_surface_y_at_x(points, zone.x)
                pad_y2 = get_surface_y_at_x(points, zone.x + zone.width - 1)
                if abs(pad_y - pad_y2) < 1 and abs(surface_y_at_x - pad_y) < 1:
                    # Check landing conditions
                    angle = (module.angle + 360) % 360
                    angle_ok = (angle <= SAFE_LANDING_ANGLE or abs(angle - 360) <= SAFE_LANDING_ANGLE)
                    if (abs(module.vy) <= SAFE_LANDING_VSPEED and
                        abs(module.vx) <= SAFE_LANDING_HSPEED and
                        angle_ok):
                        module.landed = True
                        module.y = pad_y - 10  # snap to pad
                        return "landed", zone.difficulty
                    else:
                        module.alive = False
                        return "crashed", zone.difficulty
        # Not over a landing zone or not flat
        module.alive = False
        return "crashed", 0
    return None, 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lunar Lander")
    clock = pygame.time.Clock()

    module = LunarModule()
    surface_points, landing_zones, surface_y = generate_surface()
    score = 0
    font = pygame.font.SysFont(None, 28)
    status = ""
    running = True

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (module.landed or not module.alive) and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Restart
                module = LunarModule()
                surface_points, landing_zones, surface_y = generate_surface()
                status = ""

        if module.alive and not module.landed:
            module.update(keys)
            result, difficulty = check_landing(module, surface_points, landing_zones, surface_y)
            if result == "landed":
                pts = 100 * difficulty
                score += pts
                status = f"Successful landing! +{pts} points. Press R to restart."
            elif result == "crashed":
                status = "Crashed! Press R to restart."

        # Draw
        screen.fill(BLACK)
        draw_surface(screen, surface_points)
        for zone in landing_zones:
            zone.draw(screen, surface_y)
        module.draw(screen)

        # HUD
        fuel_text = font.render(f"Fuel: {int(module.fuel)}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(fuel_text, (10, 10))
        screen.blit(score_text, (10, 40))
        if module.alive and not module.landed:
            v_text = font.render(f"V Speed: {module.vy:.2f}", True, WHITE)
            h_text = font.render(f"H Speed: {module.vx:.2f}", True, WHITE)
            a_text = font.render(f"Angle: {module.angle%360:.1f}", True, WHITE)
            screen.blit(v_text, (10, 70))
            screen.blit(h_text, (10, 100))
            screen.blit(a_text, (10, 130))
        if status:
            msg = font.render(status, True, YELLOW if module.landed else RED)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
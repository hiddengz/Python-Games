import math
import random
import pygame

# --- Game Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

SHIP_SIZE = 30
SHIP_THRUST = 0.15
SHIP_ROTATE_SPEED = 5
SHIP_FRICTION = 0.99
BULLET_SPEED = 7
BULLET_LIFETIME = 60
MAX_BULLETS = 4
HYPERSPACE_COOLDOWN = 60
GOD_CUBE_SIZE = 50
GOD_CUBE_SPEED = 2
GOD_CUBE_POINTS = 5000
ASTEROID_SIZES = {'large': 60, 'medium': 40, 'small': 20}
ASTEROID_SPEEDS = {'large': 1.5, 'medium': 2.5, 'small': 3.5}
ASTEROID_POINTS = {'large': 20, 'medium': 50, 'small': 100}
GOD_CUBE_SPAWN_CHANCE = 100  # Chance per frame to spawn the God Cube
UFO_SIZES = {'large': 40, 'small': 25}
UFO_POINTS = {'large': 200, 'small': 1000}

# God Cube class
class GodCube:
    def __init__(self):
        self.size = GOD_CUBE_SIZE
        self.pos = (random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        angle = random.uniform(0, 360)
        vec = angle_to_vector(angle)
        self.vel = [vec[0] * GOD_CUBE_SPEED, vec[1] * GOD_CUBE_SPEED]
        self.radius = self.size / 2

    def update(self):
        self.pos = wrap_position((self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]))

    def draw(self, surf):
        pygame.draw.rect(
            surf,
            (0, 255, 255),
            (
                int(self.pos[0] - self.size / 2),
                int(self.pos[1] - self.size / 2),
                self.size,
                self.size
            ),
            3
        )

LIVES = 3

# --- Helper Functions ---
def wrap_position(pos):
    x, y = pos
    return x % WIDTH, y % HEIGHT

def angle_to_vector(angle_deg):
    rad = math.radians(angle_deg)
    return math.cos(rad), math.sin(rad)

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# --- Classes ---
class Ship:
    def __init__(self):
        self.pos = (WIDTH / 2, HEIGHT / 2)
        self.vel = [0, 0]
        self.angle = 0
        self.lives = LIVES
        self.respawn()
        self.hyperspace_timer = 0

    def respawn(self):
        self.pos = (WIDTH / 2, HEIGHT / 2)
        self.vel = [0, 0]
        self.angle = 0
        self.invincible = 120  # frames

    def update(self, keys):
        # Rotation
        if keys[pygame.K_LEFT]:
            self.angle += SHIP_ROTATE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle -= SHIP_ROTATE_SPEED
        # Thrust
        if keys[pygame.K_UP]:
            vec = angle_to_vector(self.angle)
            self.vel[0] += vec[0] * SHIP_THRUST
            self.vel[1] += vec[1] * SHIP_THRUST
        # Friction
        self.vel[0] *= SHIP_FRICTION
        self.vel[1] *= SHIP_FRICTION
        # Move
        self.pos = wrap_position((self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]))
        # Invincibility timer
        if self.invincible > 0:
            self.invincible -= 1
        # Hyperspace cooldown
        if self.hyperspace_timer > 0:
            self.hyperspace_timer -= 1

    def draw(self, surf):
        # Draw triangle
        points = []
        for i in range(3):
            angle = self.angle + i * 120
            vec = angle_to_vector(angle)
            points.append((
                self.pos[0] + vec[0] * SHIP_SIZE / 2,
                self.pos[1] + vec[1] * SHIP_SIZE / 2
            ))
        color = (255, 255, 255) if self.invincible % 10 < 5 else (100, 100, 100)
        pygame.draw.polygon(surf, color, points, 2)

    def shoot(self):
        vec = angle_to_vector(self.angle)
        bullet_vel = [self.vel[0] + vec[0] * BULLET_SPEED, self.vel[1] + vec[1] * BULLET_SPEED]
        return Bullet(self.pos, bullet_vel)

    def hyperspace(self):
        if self.hyperspace_timer == 0:
            self.pos = (random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
            self.vel = [0, 0]
            self.hyperspace_timer = HYPERSPACE_COOLDOWN
            self.invincible = 60

class Bullet:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.lifetime = BULLET_LIFETIME

    def update(self):
        self.pos = wrap_position((self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]))
        self.lifetime -= 1

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 255, 0), (int(self.pos[0]), int(self.pos[1])), 2)

    def alive(self):
        return self.lifetime > 0

class Asteroid:
    def __init__(self, pos, size, vel=None):
        self.size = size
        self.radius = ASTEROID_SIZES[size] // 2
        self.pos = pos
        if vel is None:
            angle = random.uniform(0, 360)
            speed = ASTEROID_SPEEDS[size] * random.uniform(0.7, 1.3)
            vec = angle_to_vector(angle)
            self.vel = [vec[0] * speed, vec[1] * speed]
        else:
            self.vel = vel

    def update(self):
        self.pos = wrap_position((self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]))

    def draw(self, surf):
        pygame.draw.circle(surf, (180, 180, 180), (int(self.pos[0]), int(self.pos[1])), self.radius, 2)

    def split(self):
        if self.size == 'large':
            return [Asteroid(self.pos, 'medium'), Asteroid(self.pos, 'medium')]
        elif self.size == 'medium':
            return [Asteroid(self.pos, 'small'), Asteroid(self.pos, 'small')]
        else:
            return []

class UFO:
    def __init__(self, size):
        self.size = size
        self.radius = UFO_SIZES[size] // 2
        self.pos = (random.choice([0, WIDTH]), random.uniform(0, HEIGHT))
        self.vel = [random.choice([-1, 1]) * (2 if size == 'large' else 3), 0]
        self.shoot_timer = random.randint(60, 120)

    def update(self):
        self.pos = wrap_position((self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]))
        self.shoot_timer -= 1

    def draw(self, surf):
        color = (255, 0, 0) if self.size == 'small' else (0, 255, 0)
        pygame.draw.rect(surf, color, (self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius*2, self.radius))

    def shoot(self, ship_pos):
        # Large UFO shoots randomly, small UFO aims at player
        if self.size == 'large':
            angle = random.uniform(0, 360)
        else:
            dx, dy = ship_pos[0] - self.pos[0], ship_pos[1] - self.pos[1]
            angle = math.degrees(math.atan2(dy, dx))
        vec = angle_to_vector(angle)
        bullet_vel = [vec[0] * BULLET_SPEED, vec[1] * BULLET_SPEED]
        return Bullet(self.pos, bullet_vel)

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    ship = Ship()
    bullets = []
    asteroids = []
    ufos = []
    ufo_bullets = []
    score = 0
    wave = 1
    running = True

    def spawn_asteroids(n):
        for _ in range(n):
            while True:
                pos = (random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
                if dist(pos, ship.pos) > 100:
                    break
            asteroids.append(Asteroid(pos, 'large'))

    spawn_asteroids(4)

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullets.append(ship.shoot())
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    ship.hyperspace()

        # Update
        ship.update(keys)
        for b in bullets:
            b.update()
        bullets = [b for b in bullets if b.alive()]
        for a in asteroids:
            a.update()
        for u in ufos:
            u.update()
        for b in ufo_bullets:
            b.update()
        ufo_bullets = [b for b in ufo_bullets if b.alive()]

        # UFO spawn
        if random.random() < 0.002 and not ufos:
            ufos.append(UFO(random.choice(['large', 'small'])))

        # UFO shooting
        for u in ufos:
            if u.shoot_timer <= 0:
                ufo_bullets.append(u.shoot(ship.pos))
                u.shoot_timer = random.randint(60, 120)

        # Collisions: bullets vs asteroids
        for b in bullets[:]:
            for a in asteroids[:]:
                if dist(b.pos, a.pos) < a.radius:
                    bullets.remove(b)
                    asteroids.remove(a)
                    score += ASTEROID_POINTS[a.size]
                    asteroids.extend(a.split())
                    break

        # Collisions: ship vs asteroids
        if ship.invincible == 0:
            for a in asteroids:
                if dist(ship.pos, a.pos) < a.radius + SHIP_SIZE / 2:
                    ship.lives -= 1
                    ship.respawn()
                    break

        # Collisions: bullets vs UFOs
        for b in bullets[:]:
            for u in ufos[:]:
                if dist(b.pos, u.pos) < u.radius:
                    bullets.remove(b)
                    ufos.remove(u)
                    score += UFO_POINTS[u.size]
                    break

        # Collisions: ship vs UFOs
        if ship.invincible == 0:
            for u in ufos:
                if dist(ship.pos, u.pos) < u.radius + SHIP_SIZE / 2:
                    ship.lives -= 1
                    ship.respawn()
                    break

        # Collisions: UFO bullets vs ship
        if ship.invincible == 0:
            for b in ufo_bullets:
                if dist(ship.pos, b.pos) < SHIP_SIZE / 2:
                    ship.lives -= 1
                    ship.respawn()
                    break

        # Collisions: bullets vs UFO bullets (optional)
        # (not implemented for simplicity)

        # Next wave
        if not asteroids:
            wave += 1
            spawn_asteroids(3 + wave)

        # Game over
        if ship.lives <= 0:
            running = False

        # Draw
        screen.fill((0, 0, 0))
        ship.draw(screen)
        for b in bullets:
            b.draw(screen)
        for a in asteroids:
            a.draw(screen)
        for u in ufos:
            u.draw(screen)
        for b in ufo_bullets:
            b.draw(screen)
        # HUD
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {ship.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        pygame.display.flip()
        clock.tick(FPS)

    # Game Over screen
    screen.fill((0, 0, 0))
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ALIEN_ROWS = 3
ALIEN_COLS = 5
ALIEN_X_MARGIN = 60
ALIEN_Y_MARGIN = 60
ALIEN_X_SPACING = 60
ALIEN_Y_SPACING = 48
SHIELD_COUNT = 4
SHIELD_WIDTH = 80
SHIELD_HEIGHT = 40
PLAYER_LIVES = 3
MEGA_SHOT_COOLDOWN = 10

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 0, 0)
BLUE = (0, 128, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 200)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
ORANGE = (255, 140, 0)

class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 24
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        pygame.draw.rect(self.image, WHITE, (self.width//2-4, 0, 8, self.height//2))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed = 6
        self.lives = PLAYER_LIVES
        self.last_mega_shot = -MEGA_SHOT_COOLDOWN

    def move(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == 'right' and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, row):
        super().__init__()
        self.width = 36
        self.height = 24
        self.image = pygame.Surface((self.width, self.height))
        color = [GREEN, DARK_GREEN, YELLOW, ORANGE, RED][row % 5]
        self.image.fill(color)
        pygame.draw.rect(self.image, BLACK, (4, 4, self.width-8, self.height-8), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.row = row

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 6
        self.height = 18
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class MegaShot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 16
        self.height = 24
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8
        self.grow_rate = 2

    def update(self):
        self.rect.y += self.speed
        self.width += self.grow_rate
        self.height += self.grow_rate
        old_center = self.rect.center
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(center=old_center)
        if self.rect.bottom < 0 or self.width > 120:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 10
        self.height = 18
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        pygame.draw.rect(self.image, YELLOW, (2, 2, self.width-4, self.height-4))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((SHIELD_WIDTH, SHIELD_HEIGHT), pygame.SRCALPHA)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 12

    def hit(self):
        self.health -= 1
        alpha = max(60, int(255 * self.health / 12))
        self.image.fill((0, 255, 0, alpha))
        if self.health <= 0:
            self.kill()

class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 28
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, GREY, [0, 0, self.width, self.height])
        pygame.draw.rect(self.image, RED, (self.width//2-10, self.height//2, 20, 8))
        self.rect = self.image.get_rect(topleft=(-self.width, 40))
        self.speed = 5
        self.points = random.choice([50, 100, 150, 300])

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

def draw_text(surface, text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont('Arial', size, bold=True)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, rect)

class BossArmor(pygame.sprite.Sprite):
    def __init__(self, boss, offset_x):
        super().__init__()
        self.width = 30
        self.height = 16
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.boss = boss
        self.offset_x = offset_x
        self.health = 2  # Weak armor

    def update(self):
        # Attach to boss position
        self.rect.centerx = self.boss.rect.centerx + self.offset_x
        self.rect.top = self.boss.rect.bottom + 2

    def hit(self):
        self.health -= 1
        alpha = max(60, int(255 * self.health / 2))
        self.image.fill((0, 255, 0, alpha))
        if self.health <= 0:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self, armor_count):
        super().__init__()
        self.width = 100
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(ORANGE)
        pygame.draw.rect(self.image, RED, (0, 0, self.width, self.height), 3)
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH // 2, 40))
        self.health = 5
        self.max_health = 5
        self.speed = 3
        self.direction = 1
        self.last_shot = 0
        self.shot_cooldown = 5000
        self.armor_count = armor_count
        self.armor_sprites = pygame.sprite.Group()
        # Place armor pieces under the boss
        if armor_count > 0:
            spacing = self.width // (armor_count + 1)
            for i in range(armor_count):
                offset = -self.width//2 + spacing * (i+1)
                armor = BossArmor(self, offset)
                self.armor_sprites.add(armor)

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
        self.armor_sprites.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.armor_sprites.draw(surface)
        bar_width = self.width
        bar_height = 10
        fill = int(bar_width * self.health / self.max_health)
        pygame.draw.rect(surface, RED, (self.rect.left, self.rect.top - 16, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.rect.left, self.rect.top - 16, fill, bar_height))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("League Invaders")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    mega_shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    ufo_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    boss = None
    boss_appearances = 0
    boss_active = False

    rocket = Rocket()
    all_sprites.add(rocket)

    for i in range(SHIELD_COUNT):
        x = (i + 1) * SCREEN_WIDTH // (SHIELD_COUNT + 1)
        y = SCREEN_HEIGHT - 120
        shield = Shield(x, y)
        shields.add(shield)
        all_sprites.add(shield)

    def spawn_aliens():
        aliens.empty()
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLS):
                x = ALIEN_X_MARGIN + col * ALIEN_X_SPACING
                y = ALIEN_Y_MARGIN + row * ALIEN_Y_SPACING
                alien = Alien(x, y, row)
                aliens.add(alien)
                all_sprites.add(alien)

    spawn_aliens()
    alien_direction = 1
    alien_speed = 20
    alien_move_timer = 0
    alien_move_delay = 600

    score = 0
    running = True
    game_over = False
    start_screen = True
    last_bomb_time = 0
    bomb_interval = 1200
    last_ufo_time = 0
    ufo_interval = random.randint(15000, 25000)
    last_shot_time = 0
    shot_cooldown = 200
    waves_cleared = 0

    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        if start_screen:
            screen.fill(BLACK)
            draw_text(screen, "LEAGUE INVADERS", 64, SCREEN_WIDTH // 2, 180)
            draw_text(screen, "Press SPACE to Start", 36, SCREEN_WIDTH // 2, 320)
            draw_text(screen, "Left/Right to Move, Space to Shoot, M for Mega Shot", 28, SCREEN_WIDTH // 2, 370)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    start_screen = False
            continue

        if game_over:
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, 200, (255, 0, 0))
            draw_text(screen, f"Score: {score}", 36, SCREEN_WIDTH // 2, 300)
            draw_text(screen, "Press R to Restart or Q to Quit", 32, SCREEN_WIDTH // 2, 400)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        rocket.lives = PLAYER_LIVES
                        score = 0
                        all_sprites.empty()
                        aliens.empty()
                        projectiles.empty()
                        mega_shots.empty()
                        bombs.empty()
                        shields.empty()
                        ufo_group.empty()
                        boss_group.empty()
                        all_sprites.add(rocket)
                        for i in range(SHIELD_COUNT):
                            x = (i + 1) * SCREEN_WIDTH // (SHIELD_COUNT + 1)
                            y = SCREEN_HEIGHT - 120
                            shield = Shield(x, y)
                            shields.add(shield)
                            all_sprites.add(shield)
                        spawn_aliens()
                        alien_direction = 1
                        alien_move_delay = 600
                        boss_active = False
                        boss_appearances = 0
                        waves_cleared = 0
                        game_over = False
                        start_screen = True
                    if event.key == pygame.K_q:
                        running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rocket.move('left')
        if keys[pygame.K_RIGHT]:
            rocket.move('right')

        if keys[pygame.K_SPACE]:
            if now - last_shot_time > shot_cooldown and len(projectiles) < 3:
                proj = Projectile(rocket.rect.centerx, rocket.rect.top)
                projectiles.add(proj)
                all_sprites.add(proj)
                last_shot_time = now

        if keys[pygame.K_m]:
            if time.time() - rocket.last_mega_shot > MEGA_SHOT_COOLDOWN:
                mega = MegaShot(rocket.rect.centerx, rocket.rect.top)
                mega.speed = -8
                mega.grow_rate = 2
                mega_shots.add(mega)
                all_sprites.add(mega)
                rocket.last_mega_shot = time.time()

        if boss_active:
            boss_group.update()
            boss.armor_sprites.update()
            if now - boss.last_shot > boss.shot_cooldown:
                boss.last_shot = now
                mega = MegaShot(boss.rect.centerx, boss.rect.bottom)
                mega.speed = 8
                mega.grow_rate = 2
                mega_shots.add(mega)
                all_sprites.add(mega)
            # Projectiles hit armor first
            for armor in boss.armor_sprites:
                for proj in projectiles:
                    if armor.rect.colliderect(proj.rect):
                        armor.hit()
                        proj.kill()
                for mega in mega_shots:
                    if mega.speed < 0 and armor.rect.colliderect(mega.rect):
                        armor.hit()
                        mega.kill()
            # Only damage boss if all armor is gone
            if len(boss.armor_sprites) == 0:
                for proj in projectiles:
                    if boss.rect.colliderect(proj.rect):
                        boss.health -= 1
                        proj.kill()
                for mega in mega_shots:
                    if mega.speed < 0 and boss.rect.colliderect(mega.rect):
                        boss.health -= 2
                        mega.kill()
            # Boss mega shots hit player
            for mega in mega_shots:
                if mega.speed > 0 and rocket.rect.colliderect(mega.rect):
                    rocket.lives -= 1
                    mega.kill()
                    if rocket.lives <= 0:
                        game_over = True
            if boss.health <= 0:
                boss.kill()
                boss_active = False
                spawn_aliens()
                alien_move_delay = 600

        if not boss_active:
            if now - alien_move_timer > alien_move_delay:
                alien_move_timer = now
                move_sideways = True
                for alien in aliens:
                    alien.rect.x += alien_direction * alien_speed
                    if alien.rect.right >= SCREEN_WIDTH - 10 or alien.rect.left <= 10:
                        move_sideways = False
                if not move_sideways:
                    alien_direction *= -1
                    for alien in aliens:
                        alien.rect.y += 24
                        if alien.rect.bottom >= SCREEN_HEIGHT - 120:
                            game_over = True
                if len(aliens) > 0:
                    alien_move_delay = max(80, 600 - (50 * (ALIEN_ROWS * ALIEN_COLS - len(aliens))))

            if now - last_bomb_time > bomb_interval and len(aliens) > 0:
                last_bomb_time = now
                shooter = random.choice(list(aliens))
                bomb = Bomb(shooter.rect.centerx, shooter.rect.bottom)
                bombs.add(bomb)
                all_sprites.add(bomb)

        projectiles.update()
        mega_shots.update()
        bombs.update()
        ufo_group.update()

        for proj in projectiles:
            hit_aliens = pygame.sprite.spritecollide(proj, aliens, True)
            if hit_aliens:
                proj.kill()
                for alien in hit_aliens:
                    score += 10 + (ALIEN_ROWS - alien.row) * 10

        for mega in mega_shots:
            hit_aliens = pygame.sprite.spritecollide(mega, aliens, True)
            if hit_aliens:
                for alien in hit_aliens:
                    score += 10 + (ALIEN_ROWS - alien.row) * 10

        for proj in projectiles:
            hit_shields = pygame.sprite.spritecollide(proj, shields, False)
            if hit_shields:
                proj.kill()
                for shield in hit_shields:
                    shield.hit()

        for mega in mega_shots:
            hit_shields = pygame.sprite.spritecollide(mega, shields, False)
            if hit_shields:
                for shield in hit_shields:
                    shield.hit()

        for bomb in bombs:
            hit_shields = pygame.sprite.spritecollide(bomb, shields, False)
            if hit_shields:
                bomb.kill()
                for shield in hit_shields:
                    shield.hit()

        if pygame.sprite.spritecollide(rocket, bombs, True):
            rocket.lives -= 1
            if rocket.lives <= 0:
                game_over = True

        if pygame.sprite.spritecollide(rocket, aliens, False):
            game_over = True

        for ufo in ufo_group:
            if pygame.sprite.spritecollide(ufo, projectiles, True) or pygame.sprite.spritecollide(ufo, mega_shots, False):
                score += ufo.points
                ufo.kill()

        for proj in projectiles:
            if proj.rect.bottom < 0:
                proj.kill()
        for mega in mega_shots:
            if mega.rect.bottom < 0:
                mega.kill()

        # Boss appears every other wave (after each wave)
        if len(aliens) == 0 and not boss_active:
            waves_cleared += 1
            if waves_cleared % 2 == 0:
                boss_appearances += 1
                armor_count = min(3, boss_appearances)
                boss = Boss(armor_count)
                boss_group.empty()
                boss_group.add(boss)
                all_sprites.add(boss)
                boss_active = True
                for b in bombs: b.kill()
                for m in mega_shots: m.kill()
            else:
                spawn_aliens()
                alien_move_delay = 600

        screen.fill(BLACK)
        all_sprites.draw(screen)
        ufo_group.draw(screen)
        if boss_active:
            boss_group.draw(screen)
            boss.draw(screen)
        rocket.draw(screen)
        draw_text(screen, f"Score: {score}", 28, 90, 20)
        draw_text(screen, f"Lives: {rocket.lives}", 28, SCREEN_WIDTH - 100, 20)
        cooldown_left = max(0, int(MEGA_SHOT_COOLDOWN - (time.time() - rocket.last_mega_shot)))
        draw_text(screen, f"Mega: {cooldown_left}s", 24, SCREEN_WIDTH // 2, 20, (255, 200, 200))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
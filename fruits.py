import pygame
import random
import math

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Cut Game")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (255, 70, 70)
GREEN = (80, 220, 100)
YELLOW = (255, 220, 50)
ORANGE = (255, 150, 40)
PURPLE = (180, 80, 220)

FRUIT_COLORS = [RED, GREEN, YELLOW, ORANGE, PURPLE]


class Fruit:
    def __init__(self):
        self.radius = random.randint(25, 35)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = HEIGHT + self.radius

        # Movement
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-16, -12)

        self.color = random.choice(FRUIT_COLORS)
        self.cut = False

    def update(self):
        # Gravity
        self.speed_y += 0.45

        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

        # Small fruit shine
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x - 10), int(self.y - 10)),
            5
        )

        # Leaf
        pygame.draw.ellipse(
            screen,
            GREEN,
            (self.x - 4, self.y - self.radius - 8, 15, 10)
        )

    def touched(self, mouse_x, mouse_y):
        distance = math.sqrt(
            (mouse_x - self.x) ** 2 +
            (mouse_y - self.y) ** 2
        )
        return distance <= self.radius


fruits = []
score = 0
lives = 3

spawn_timer = 0
running = True
game_over = False

# Mouse trail
trail = []

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                fruits.clear()
                score = 0
                lives = 3
                game_over = False

    if not game_over:

        # Spawn fruits
        spawn_timer += 1
        if spawn_timer >= 45:
            fruits.append(Fruit())
            spawn_timer = 0

        # Mouse cutting
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            trail.append((mx, my))

            if len(trail) > 10:
                trail.pop(0)

            for fruit in fruits[:]:
                if fruit.touched(mx, my):
                    fruits.remove(fruit)
                    score += 1
        else:
            trail.clear()

        # Update fruits
        for fruit in fruits[:]:
            fruit.update()

            # Fruit missed
            if fruit.y - fruit.radius > HEIGHT:
                fruits.remove(fruit)
                lives -= 1

                if lives <= 0:
                    game_over = True

    # Background
    screen.fill(BLACK)

    # Draw fruits
    for fruit in fruits:
        fruit.draw()

    # Draw cutting trail
    if len(trail) > 1:
        pygame.draw.lines(
            screen,
            WHITE,
            False,
            trail,
            5
        )

    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # Lives
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(lives_text, (WIDTH - 130, 20))

    # Game over screen
    if game_over:
        text = big_font.render("GAME OVER", True, RED)
        restart = font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        screen.blit(
            text,
            text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        )

        screen.blit(
            restart,
            restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        )

    pygame.display.flip()

pygame.quit()
import pygame
import random
import sys

WIDTH = 480
HEIGHT = 640
FPS = 60

CAR_WIDTH = 40
CAR_HEIGHT = 70
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 70
LANE_PADDING = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Car Dodge Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
large_font = pygame.font.SysFont(None, 64)


def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font_obj = pygame.font.SysFont(None, size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def draw_road():
    screen.fill((20, 20, 20))
    pygame.draw.rect(screen, (50, 50, 50), (LANE_PADDING, 0, WIDTH - 2 * LANE_PADDING, HEIGHT))
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, (220, 220, 220), (WIDTH // 2 - 5, i + 10, 10, 20))
    pygame.draw.line(screen, (200, 200, 200), (LANE_PADDING, 0), (LANE_PADDING, HEIGHT), 4)
    pygame.draw.line(screen, (200, 200, 200), (WIDTH - LANE_PADDING, 0), (WIDTH - LANE_PADDING, HEIGHT), 4)


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def main():
    player_x = WIDTH // 2 - CAR_WIDTH // 2
    player_y = HEIGHT - CAR_HEIGHT - 20
    player_speed = 5

    obstacles = []
    obstacle_timer = 0
    score = 0
    game_over = False

    while True:
        dt = clock.tick(FPS)
        if not game_over:
            score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    main()

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_y -= player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_y += player_speed

        player_x = clamp(player_x, LANE_PADDING + 5, WIDTH - LANE_PADDING - CAR_WIDTH - 5)
        player_y = clamp(player_y, 0, HEIGHT - CAR_HEIGHT)

        if not game_over:
            obstacle_timer += dt
            if obstacle_timer > 700:
                obstacle_timer = 0
                lane_x = random.choice([
                    LANE_PADDING + 20,
                    LANE_PADDING + 20 + (WIDTH - 2 * LANE_PADDING - OBSTACLE_WIDTH) // 2,
                    WIDTH - LANE_PADDING - OBSTACLE_WIDTH - 20,
                ])
                obstacles.append({
                    "x": lane_x,
                    "y": -OBSTACLE_HEIGHT,
                    "speed": random.randint(4, 8),
                })

            for obs in obstacles:
                obs["y"] += obs["speed"]

            obstacles = [obs for obs in obstacles if obs["y"] < HEIGHT + OBSTACLE_HEIGHT]

            player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)
            for obs in obstacles:
                obs_rect = pygame.Rect(obs["x"], obs["y"], OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                if player_rect.colliderect(obs_rect):
                    game_over = True
                    break

        draw_road()

        pygame.draw.rect(screen, (0, 180, 255), (player_x, player_y, CAR_WIDTH, CAR_HEIGHT), border_radius=8)
        pygame.draw.rect(screen, (0, 120, 190), (player_x + 8, player_y + 12, CAR_WIDTH - 16, CAR_HEIGHT - 24), border_radius=6)

        for obs in obstacles:
            pygame.draw.rect(screen, (220, 50, 50), (obs["x"], obs["y"], OBSTACLE_WIDTH, OBSTACLE_HEIGHT), border_radius=8)
            pygame.draw.rect(screen, (180, 30, 30), (obs["x"] + 6, obs["y"] + 10, OBSTACLE_WIDTH - 12, OBSTACLE_HEIGHT - 20), border_radius=6)

        draw_text(screen, f"Score: {score // 10}", 28, WIDTH // 2, 30)

        if game_over:
            draw_text(screen, "Game Over", 64, WIDTH // 2, HEIGHT // 2 - 40, color=(255, 220, 0))
            draw_text(screen, "Press R to restart", 32, WIDTH // 2, HEIGHT // 2 + 30, color=(255, 255, 255))

        pygame.display.flip()


if __name__ == "__main__":
    main()

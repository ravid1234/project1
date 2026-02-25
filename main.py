import pygame
import asyncio
import sys

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Python Web")

# Colors & Font
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)
font = pygame.font.SysFont(None, 64)

# Player setup
player_rect = pygame.Rect(375, 540, 50, 40)
player_speed = 5

# Bullets & Enemies
bullets = []
enemies = []
enemy_speed = 2

for row in range(5):
    for col in range(10):
        enemies.append(pygame.Rect(col * 60 + 50, row * 50 + 50, 40, 30))

async def main():
    global enemy_speed
    running = True
    game_over = False
    won = False
    waiting_to_start = True # This satisfies the browser's "Media User Action"
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        # --- 1. START SCREEN (Bypasses "Stuck" Loading) ---
        if waiting_to_start:
            msg = "CLICK TO START"
            text_surface = font.render(msg, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 - 32))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # First click/key starts the engine and allows sound/logic
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    waiting_to_start = False
            
            pygame.display.flip()
            await asyncio.sleep(0) # Keep browser responsive
            continue

        # --- 2. EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player_rect.centerx - 2, player_rect.top, 5, 15))

        # --- 3. GAME LOGIC ---
        if not game_over:
            # Player Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
                player_rect.x += player_speed

            # Bullet movement
            for bullet in bullets[:]:
                bullet.y -= 7
                if bullet.bottom < 0:
                    bullets.remove(bullet)

            # Enemy movement
            move_down = False
            for enemy in enemies:
                enemy.x += enemy_speed
                if enemy.right >= SCREEN_WIDTH or enemy.left <= 0:
                    move_down = True
            if move_down:
                enemy_speed *= -1
                for enemy in enemies:
                    enemy.y += 10

            # Collision detection
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.colliderect(enemy):
                        if bullet in bullets: bullets.remove(bullet)
                        enemies.remove(enemy)
                        break

            # Win/Loss Logic
            if not enemies:
                won = True
                game_over = True
            if any(enemy.bottom >= player_rect.top for enemy in enemies):
                won = False
                game_over = True

        # --- 4. DRAWING ---
        pygame.draw.rect(screen, GREEN, player_rect)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        if game_over:
            msg = "YOU WIN!" if won else "GAME OVER"
            color = GREEN if won else RED
            text_surface = font.render(msg, True, color)
            screen.blit(text_surface, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 32))

        pygame.display.flip()
        await asyncio.sleep(0) # CRITICAL: Allows browser to run the loop
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main()) # Proper web entry point

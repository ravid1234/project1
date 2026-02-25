import pygame
import asyncio # Required for web
import sys

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Python Web")

# Colors
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)

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

async def main(): # Pygbag requires the loop in an async function
    global enemy_speed
    score = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player_rect.centerx - 2, player_rect.top, 5, 15))

        # Movement
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
                    score += 10
                    break

        # Drawing
        pygame.draw.rect(screen, GREEN, player_rect)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Game Over Check
        if not enemies or any(enemy.bottom >= player_rect.top for enemy in enemies):
            running = False

        pygame.display.flip()
        
        # CRITICAL: Allow browser to update
        await asyncio.sleep(0) 
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Run the game
asyncio.run(main())

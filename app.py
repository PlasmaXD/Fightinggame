import pygame
import sys

# ゲームの初期設定
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("格闘ゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# プレイヤーの設定
player1 = pygame.Rect(100, 400, 50, 100)
player2 = pygame.Rect(600, 400, 50, 100)
player1_health = 100
player2_health = 100

player1_speed = 5
player2_speed = 5

# 地面の設定
ground = pygame.Rect(0, 500, 800, 100)

# 重力とジャンプの設定
gravity = 0.5
player1_velocity_y = 0
player2_velocity_y = 0
jump_strength = -10
player1_on_ground = True
player2_on_ground = True

# 攻撃の設定
attack_cooldown = 500  # ミリ秒
last_attack_time_player1 = 0
last_attack_time_player2 = 0

# ゲームのメインループ
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # プレイヤー1の操作
    if keys[pygame.K_a]:
        player1.x -= player1_speed
    if keys[pygame.K_d]:
        player1.x += player1_speed
    if keys[pygame.K_w] and player1_on_ground:
        player1_velocity_y = jump_strength
        player1_on_ground = False

    # プレイヤー2の操作
    if keys[pygame.K_LEFT]:
        player2.x -= player2_speed
    if keys[pygame.K_RIGHT]:
        player2.x += player2_speed
    if keys[pygame.K_UP] and player2_on_ground:
        player2_velocity_y = jump_strength
        player2_on_ground = False

    current_time = pygame.time.get_ticks()

    # プレイヤー1の攻撃
    if keys[pygame.K_SPACE]:  # パンチ攻撃
        if current_time - last_attack_time_player1 > attack_cooldown:
            attack_rect = pygame.Rect(player1.right, player1.y + 20, 20, 20)
            if attack_rect.colliderect(player2):
                if not keys[pygame.K_RSHIFT]:  # プレイヤー2が防御していない場合
                    player2_health -= 10
            last_attack_time_player1 = current_time

    if keys[pygame.K_f]:  # キック攻撃
        if current_time - last_attack_time_player1 > attack_cooldown:
            attack_rect = pygame.Rect(player1.right, player1.y + 50, 30, 20)
            if attack_rect.colliderect(player2):
                if not keys[pygame.K_RSHIFT]:  # プレイヤー2が防御していない場合
                    player2_health -= 15
            last_attack_time_player1 = current_time

    # プレイヤー2の攻撃
    if keys[pygame.K_RETURN]:  # パンチ攻撃
        if current_time - last_attack_time_player2 > attack_cooldown:
            attack_rect = pygame.Rect(player2.left - 20, player2.y + 20, 20, 20)
            if attack_rect.colliderect(player1):
                if not keys[pygame.K_LSHIFT]:  # プレイヤー1が防御していない場合
                    player1_health -= 10
            last_attack_time_player2 = current_time

    if keys[pygame.K_SLASH]:  # キック攻撃
        if current_time - last_attack_time_player2 > attack_cooldown:
            attack_rect = pygame.Rect(player2.left - 30, player2.y + 50, 30, 20)
            if attack_rect.colliderect(player1):
                if not keys[pygame.K_LSHIFT]:  # プレイヤー1が防御していない場合
                    player1_health -= 15
            last_attack_time_player2 = current_time

    # 重力の適用
    player1_velocity_y += gravity
    player2_velocity_y += gravity

    player1.y += player1_velocity_y
    player2.y += player2_velocity_y

    # 地面との衝突判定
    if player1.colliderect(ground):
        player1.y = ground.top - player1.height
        player1_velocity_y = 0
        player1_on_ground = True
    else:
        player1_on_ground = False

    if player2.colliderect(ground):
        player2.y = ground.top - player2.height
        player2_velocity_y = 0
        player2_on_ground = True
    else:
        player2_on_ground = False

    # ゲーム画面の描画
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)
    pygame.draw.rect(screen, BLACK, ground)

    # 防御の描画
    if keys[pygame.K_LSHIFT]:
        pygame.draw.rect(screen, GRAY, (player1.x - 10, player1.y, 10, 100))
    if keys[pygame.K_RSHIFT]:
        pygame.draw.rect(screen, GRAY, (player2.x + player2.width, player2.y, 10, 100))

    # ヘルスバーの描画
    pygame.draw.rect(screen, RED, (10, 10, player1_health * 2, 20))
    pygame.draw.rect(screen, BLUE, (580, 10, player2_health * 2, 20))

    pygame.display.flip()
    clock.tick(60)

    # ゲーム終了判定
    if player1_health <= 0 or player2_health <= 0:
        running = False

# 終了メッセージ
print("ゲーム終了")

pygame.quit()

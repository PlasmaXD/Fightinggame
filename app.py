import pygame
import sys
import random

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
YELLOW = (255, 255, 0)

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

# 遠距離攻撃の設定
projectiles = []
projectile_speed = 7
projectile_cooldown = 1000  # ミリ秒
last_projectile_time_player1 = 0
last_projectile_time_player2 = 0
effects = []  # エフェクト用のリスト
effect_duration = 300  # エフェクトの持続時間（ミリ秒）

# CPUのジャンプタイミング
cpu_jump_cooldown = random.randint(2000, 5000)
last_jump_time_cpu = pygame.time.get_ticks()

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

    current_time = pygame.time.get_ticks()

    # プレイヤー1の攻撃
    if keys[pygame.K_SPACE]:  # パンチ攻撃
        if current_time - last_attack_time_player1 > attack_cooldown:
            attack_rect = pygame.Rect(player1.right, player1.y + 20, 20, 20)
            if attack_rect.colliderect(player2):
                player2_health -= 10
            last_attack_time_player1 = current_time

    if keys[pygame.K_f]:  # キック攻撃
        if current_time - last_attack_time_player1 > attack_cooldown:
            attack_rect = pygame.Rect(player1.right, player1.y + 50, 30, 20)
            if attack_rect.colliderect(player2):
                player2_health -= 15
            last_attack_time_player1 = current_time

    # プレイヤー1の遠距離攻撃
    if keys[pygame.K_e]:  # 遠距離攻撃
        if current_time - last_projectile_time_player1 > projectile_cooldown:
            projectiles.append(pygame.Rect(player1.right, player1.y + 50, 20, 10))
            effects.append(
                {'rect': pygame.Rect(player1.right, player1.y + 50, 20, 10), 'time': current_time, 'color': YELLOW})
            last_projectile_time_player1 = current_time

    # CPUの操作
    # プレイヤー1との距離を計算
    distance_to_player1 = player1.x - player2.x

    # CPUのジャンプ
    if current_time - last_jump_time_cpu > cpu_jump_cooldown:
        if player2_on_ground and abs(distance_to_player1) < 100:
            player2_velocity_y = jump_strength
            player2_on_ground = False
        last_jump_time_cpu = current_time
        cpu_jump_cooldown = random.randint(2000, 5000)

    # プレイヤー1に向かって移動
    if distance_to_player1 > 100:
        player2.x += player2_speed
    elif distance_to_player1 < -100:
        player2.x -= player2_speed
    else:
        # プレイヤー1が近い場合、防御または攻撃
        if random.randint(0, 100) < 30:  # 30%の確率で防御
            if random.randint(0, 1) == 0:
                pygame.draw.rect(screen, GRAY, (player2.x + player2.width, player2.y, 10, 100))
        else:
            if random.randint(0, 1) == 0:  # パンチ攻撃
                if current_time - last_attack_time_player2 > attack_cooldown:
                    attack_rect = pygame.Rect(player2.left - 20, player2.y + 20, 20, 20)
                    if attack_rect.colliderect(player1):
                        player1_health -= 10
                    last_attack_time_player2 = current_time
            else:  # キック攻撃
                if current_time - last_attack_time_player2 > attack_cooldown:
                    attack_rect = pygame.Rect(player2.left - 30, player2.y + 50, 30, 20)
                    if attack_rect.colliderect(player1):
                        player1_health -= 15
                    last_attack_time_player2 = current_time

    # CPUの遠距離攻撃
    if random.randint(0, 100) < 5:  # 5%の確率で遠距離攻撃
        if current_time - last_projectile_time_player2 > projectile_cooldown:
            projectiles.append(pygame.Rect(player2.left, player2.y + 50, 20, 10))
            effects.append(
                {'rect': pygame.Rect(player2.left, player2.y + 50, 20, 10), 'time': current_time, 'color': YELLOW})
            last_projectile_time_player2 = current_time

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

    # プロジェクタイルの移動と描画
    for projectile in projectiles:
        if projectile.x < player1.x:
            projectile.x -= projectile_speed
        else:
            projectile.x += projectile_speed
        pygame.draw.rect(screen, BLACK, projectile)

        # プレイヤーに当たった場合の処理
        if projectile.colliderect(player1):
            player1_health -= 5
            effects.append({'rect': pygame.Rect(player1.x, player1.y, 50, 100), 'time': current_time, 'color': RED})
            projectiles.remove(projectile)
        elif projectile.colliderect(player2):
            player2_health -= 5
            effects.append({'rect': pygame.Rect(player2.x, player2.y, 50, 100), 'time': current_time, 'color': RED})
            projectiles.remove(projectile)

        # 画面外に出た場合の処理
        if projectile.x < 0 or projectile.x > 800:
            projectiles.remove(projectile)

    # ゲーム画面の描画
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)
    pygame.draw.rect(screen, BLACK, ground)

    # プロジェクタイルの描画
    for projectile in projectiles:
        pygame.draw.rect(screen, BLACK, projectile)

    # エフェクトの描画
    for effect in effects:
        if current_time - effect['time'] < effect_duration:
            pygame.draw.rect(screen, effect['color'], effect['rect'])
        else:
            effects.remove(effect)

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

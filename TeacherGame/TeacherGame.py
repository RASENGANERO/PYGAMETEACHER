# -*- coding: cp1251 -*-
import pygame
import random
import time

# Инициализация PyGame
pygame.init()

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Прикольная бегалка!')

programIcon = pygame.image.load('assets/favicon.ico')
pygame.display.set_icon(programIcon)
# Загрузка спрайта персонажа
character_sprite_path = 'assets/player2.png'
character_sprite = pygame.image.load(character_sprite_path)

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (232, 89, 28)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Параметры игрока
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
player_speed = 10

# Параметры врагов и бонусов
enemy_size = 50
enemy_list = []
bonus_list = []
SPEED = 10

# Параметры меню и игры
menu_active = True
game_over = False
game_lost = False
difficulty_settings = {"Легко": 5, "Средне": 10, "Сложно": 15}
difficulty = "Средне"

# Счет
score = 0

# Таймер
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont("monospace", 35)
menu_font = pygame.font.SysFont("monospace", 50)

# Переменные для таймера игры
game_start_time = None
game_duration = 20# 5 минут
time_remaining = game_duration

# Функция для сохранения рекордов
def save_high_score(new_score):
    if new_score < 0:  # Не сохраняем отрицательные результаты
        return
    try:
        with open("highscores.txt", "r+") as file:
            scores = [int(line.strip()) for line in file.readlines()]
            scores.append(new_score)
            scores = sorted(scores, reverse=True)[:5]  # Сохраняем только топ-5 результатов
            file.seek(0)
            file.truncate()
            for score in scores:
                file.write(f"{score}\n")
    except FileNotFoundError:
        with open("highscores.txt", "w") as file:
            file.write(f"{new_score}\n")

# Функция для получения списка рекордов
def get_high_scores():
    try:
        with open("highscores.txt", "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
            return scores
    except FileNotFoundError:
        return []


# Функция для отображения главного меню
def draw_menu():
    screen.fill(GRAY)
    y_offset = 150
    for i, diff in enumerate(difficulty_settings):
        text = menu_font.render(diff, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset + i * 60))
        pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 10))
        screen.blit(text, text_rect)

    # Отображение таблицы лидеров
    high_scores = get_high_scores()
    y_offset = 350
    scores_text = menu_font.render("Лучшие результаты:", True, BLACK)
    screen.blit(scores_text, (SCREEN_WIDTH / 2 - 150, y_offset - 50))
    for score in high_scores:
        score_text = font.render(str(score), True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH / 2 - 50, y_offset))
        y_offset += 40

# Функция для выбора сложности в меню
def select_difficulty(pos):
    global difficulty, menu_active, SPEED
    index = (pos[1] - 150) // 60
    if 0 <= index < len(difficulty_settings):
        difficulty = list(difficulty_settings.keys())[index]
        SPEED = difficulty_settings[difficulty]
        menu_active = False
        start_new_game()

# Функция для отрисовки текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Функция для обнаружения столкновений
def detect_collisions(player_pos, enemy_list, bonus_list):
    global score
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for enemy_pos in enemy_list:
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            enemy_list.remove(enemy_pos)
            score -= 1

    for bonus_pos in bonus_list:
        bonus_rect = pygame.Rect(bonus_pos[0], bonus_pos[1], enemy_size, enemy_size)
        if player_rect.colliderect(bonus_rect):
            bonus_list.remove(bonus_pos)
            score += 1

# Функция для обновления позиций объектов
def update_object_positions(object_list):
    for obj_pos in object_list:
        if obj_pos[1] >= 0 and obj_pos[1] < SCREEN_HEIGHT:
            obj_pos[1] += SPEED
        else:
            object_list.remove(obj_pos)

# Функция для создания новых объектов
def drop_objects(object_list, color):
    delay = random.random()
    if len(object_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
        y_pos = 0
        object_list.append([x_pos, y_pos, color])

# Функция для сброса игры
def reset_game():
    global player_pos, score, enemy_list, bonus_list, game_lost, game_start_time
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
    score = 0
    enemy_list = []
    bonus_list = []
    game_lost = False
    game_start_time = time.time()

# Функция для начала новой игры
def start_new_game():
    global game_start_time
    game_start_time = time.time()
    reset_game()

# Функция для отображения экрана Game Over
def draw_game_over_screen():
    screen.fill(GRAY)
    over_text = menu_font.render("Игра окончена!", True, BLACK)
    over_rect = over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(over_text, over_rect)

    retry_text = menu_font.render("Повторить", True, BLACK)
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    screen.blit(retry_text, retry_rect)

    menu_text = menu_font.render("Меню", True, BLACK)
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90))
    screen.blit(menu_text, menu_rect)

    return retry_rect, menu_rect
# Игровой цикл
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if menu_active and event.type == pygame.MOUSEBUTTONDOWN:
            select_difficulty(pygame.mouse.get_pos())

        if game_lost:
            retry_button, menu_button = draw_game_over_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(mouse_pos):
                    reset_game()
                    game_lost = False
                elif menu_button.collidepoint(mouse_pos):
                    menu_active = True
                    game_lost = False

    keys = pygame.key.get_pressed()
    if not menu_active and not game_lost:
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
            if player_pos[0] < 0:
                player_pos[0] = 0

        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
            if player_pos[0] > SCREEN_WIDTH - player_size:
                player_pos[0] = SCREEN_WIDTH - player_size

        current_time = time.time()
        time_elapsed = current_time - game_start_time
        time_remaining = max(game_duration - int(time_elapsed), 0)
        if game_start_time and (current_time - game_start_time > game_duration):
            game_lost = True
            if score > 0:  # Сохраняем только положительные результаты
                save_high_score(score)
        draw_text(f"Осталось времени: {time_remaining}", font, BLACK, screen, SCREEN_WIDTH - 150, 10)

    if menu_active:
        draw_menu()
    elif game_lost:
        pass
    else:
        screen.fill((70, 84, 212))
        

        drop_objects(enemy_list, ORANGE)
        drop_objects(bonus_list, GREEN)
        update_object_positions(enemy_list)
        update_object_positions(bonus_list)
        detect_collisions(player_pos, enemy_list, bonus_list)

        for enemy_pos in enemy_list:
            pygame.draw.rect(screen, ORANGE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

        for bonus_pos in bonus_list:
            pygame.draw.rect(screen, GREEN, (bonus_pos[0], bonus_pos[1], enemy_size, enemy_size))

        screen.blit(character_sprite, (player_pos[0], player_pos[1]))
        draw_text("Счёт: {}".format(score), font, BLACK, screen, 10, 10)

        clock.tick(30)
    pygame.display.update()
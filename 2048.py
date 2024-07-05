import pygame
import random
import sys
import math

# Инициализация Pygame
pygame.init()

# Размеры окна и ячейки
WINDOW_SIZE = 400
CELL_SIZE = WINDOW_SIZE // 4
FONT_SIZE = 32
BACKGROUND_COLOR = (187, 173, 160)
GRID_COLOR = (205, 193, 180)
TEXT_COLOR = (255, 255, 255)

# Инициализация окна
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('2048 ИГРА ХАРД ЛВЛ - Лисенок Edition')

# Цвета и текст плиток
tile_colors = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (187, 173, 160),
    8192: (255, 0, 0),       # Новые значения и цвета плиток
    16384: (255, 255, 0),
    32768: (0, 255, 0)
}

# Функция для отрисовки текста
def draw_text(text, x, y, font_size=FONT_SIZE, color=TEXT_COLOR):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

# Функция для отрисовки плиток
def draw_board(board):
    for row in range(4):
        for col in range(4):
            value = board[row][col]
            tile_color = tile_colors.get(value, tile_colors[32768])
            pygame.draw.rect(window, tile_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if value != 0:
                draw_text(str(value), col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)

# Функция для создания новой плитки
def add_new_tile(board):
    empty_cells = [(row, col) for row in range(4) for col in range(4) if board[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 2 if random.random() < 0.9 else 4

# Функция для проверки на конец игры
def game_over(board):
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                return False
            if col < 3 and board[row][col] == board[row][col + 1]:
                return False
            if row < 3 and board[row][col] == board[row + 1][col]:
                return False
    return True

# Функции для движения плиток
def move_up(board):
    moved = False
    for col in range(4):
        for row in range(1, 4):
            if board[row][col] != 0:
                for k in range(row, 0, -1):
                    if board[k - 1][col] == 0:
                        board[k - 1][col] = board[k][col]
                        board[k][col] = 0
                        moved = True
                    elif board[k - 1][col] == board[k][col]:
                        board[k - 1][col] *= 2
                        board[k][col] = 0
                        moved = True
                        break
    return moved

def move_down(board):
    moved = False
    for col in range(4):
        for row in range(2, -1, -1):
            if board[row][col] != 0:
                for k in range(row, 3):
                    if board[k + 1][col] == 0:
                        board[k + 1][col] = board[k][col]
                        board[k][col] = 0
                        moved = True
                    elif board[k + 1][col] == board[k][col]:
                        board[k + 1][col] *= 2
                        board[k][col] = 0
                        moved = True
                        break
    return moved

def move_left(board):
    moved = False
    for row in range(4):
        for col in range(1, 4):
            if board[row][col] != 0:
                for k in range(col, 0, -1):
                    if board[row][k - 1] == 0:
                        board[row][k - 1] = board[row][k]
                        board[row][k] = 0
                        moved = True
                    elif board[row][k - 1] == board[row][k]:
                        board[row][k - 1] *= 2
                        board[row][k] = 0
                        moved = True
                        break
    return moved

def move_right(board):
    moved = False
    for row in range(4):
        for col in range(2, -1, -1):
            if board[row][col] != 0:
                for k in range(col, 3):
                    if board[row][k + 1] == 0:
                        board[row][k + 1] = board[row][k]
                        board[row][k] = 0
                        moved = True
                    elif board[row][k + 1] == board[row][k]:
                        board[row][k + 1] *= 2
                        board[row][k] = 0
                        moved = True
                        break
    return moved

# Мощный ИИ для автоматического хода
def ai_move(board):
    best_move, _ = minimax(board, 5, True, -math.inf, math.inf)
    if best_move:
        best_move(board)
        add_new_tile(board)

# Функция минимакса с альфа-бета отсечением
def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or game_over(board):
        return None, evaluate_board(board)

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move_func in [move_up, move_down, move_left, move_right]:
            temp_board = [row[:] for row in board]
            if move_func(temp_board):
                _, eval = minimax(temp_board, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move_func
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return best_move, max_eval
    else:
        min_eval = math.inf
        for row in range(4):
            for col in range(4):
                if board[row][col] == 0:
                    board[row][col] = 2
                    _, eval = minimax(board, depth - 1, True, alpha, beta)
                    board[row][col] = 0
                    if eval < min_eval:
                        min_eval = eval
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return None, min_eval

# Функция для оценки текущего состояния доски
def evaluate_board(board):
    empty_cells = sum(row.count(0) for row in board)
    monotonicity = 0
    max_tile = max(max(row) for row in board)

    for row in board:
        for i in range(3):
            monotonicity += abs(row[i] - row[i + 1])

    for col in range(4):
        for row in range(3):
            monotonicity += abs(board[row][col] - board[row + 1][col])

    return empty_cells * 1000 - monotonicity + max_tile * 10

# Функция для отображения меню при завершении игры
def end_game_menu():
    while True:
        draw_text("Игра завершена", WINDOW_SIZE // 2, WINDOW_SIZE // 2)
        draw_text("1 - Вернуться в главное меню", WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50)
        draw_text("2 - Закрыть программу", WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "menu"
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

# Основной цикл игры
def main():
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)

    player_mode = None

    while player_mode is None:
        window.fill(BACKGROUND_COLOR)
        draw_board(board)
        draw_text("Смертный", 100, 75)
        draw_text("Супер Лисенок!", 300, 75)
        draw_text("Нажмите 1 или 2", WINDOW_SIZE // 2, WINDOW_SIZE // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_mode = "Human"
                elif event.key == pygame.K_2:
                    player_mode = "AI"

    while True:
        window.fill(BACKGROUND_COLOR)
        draw_board(board)
        pygame.display.update()

        if game_over(board):
            if end_game_menu() == "menu":
                return main()
            else:
                pygame.quit()
                sys.exit()

        if player_mode == "Human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    moved = False
                    if event.key == pygame.K_UP:
                        moved = move_up(board)
                    elif event.key == pygame.K_DOWN:
                        moved = move_down(board)
                    elif event.key == pygame.K_LEFT:
                        moved = move_left(board)
                    elif event.key == pygame.K_RIGHT:
                        moved = move_right(board)
                    if moved:
                        add_new_tile(board)

        elif player_mode == "AI":
            ai_move(board)
            # pygame.time.wait(200)  # Увеличиваем время задержки для "разгрузки"

if __name__ == "__main__":
    main()

    pygame.quit()
    sys.exit()

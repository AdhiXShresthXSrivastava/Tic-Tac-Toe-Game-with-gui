import pygame
import sys
import os

# === For sound file loading in PyInstaller ===
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 500
BG_TOP = (30, 30, 60)
BG_BOTTOM = (10, 10, 10)
TEXT_COLOR = (255, 255, 255)
X_COLOR = (255, 255, 255)
O_COLOR = (200, 50, 50)
LINE_COLOR = (150, 150, 150)
HIGHLIGHT_COLOR = (0, 255, 0)
LINE_WIDTH = 5
CELL_SIZE = WIDTH // 3
FONT = pygame.font.SysFont("arial", 28)
BIG_FONT = pygame.font.SysFont("arial", 42, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 20)

# Load sound effects
click_sound = pygame.mixer.Sound(resource_path("sound/click.wav"))
win_sound = pygame.mixer.Sound(resource_path("sound/win.wav"))
tie_sound = pygame.mixer.Sound(resource_path("sound/tie.wav"))
lose_sound = pygame.mixer.Sound(resource_path("sound/lose.wav"))

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Game state
board = [[" " for _ in range(3)] for _ in range(3)]
player = "X"
winner = None
game_active = False
game_over = False
mode = None
winning_line = None

# Helper functions
def check_temp_winner(sym):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == sym:
            return True
        if board[0][i] == board[1][i] == board[2][i] == sym:
            return True
    if board[0][0] == board[1][1] == board[2][2] == sym:
        return True
    if board[0][2] == board[1][1] == board[2][0] == sym:
        return True
    return False

def ai_move():
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = "O"
                if check_temp_winner("O"):
                    board[r][c] = " "
                    return r, c
                board[r][c] = " "

    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = "X"
                if check_temp_winner("X"):
                    board[r][c] = " "
                    return r, c
                board[r][c] = " "

    if board[1][1] == " ":
        return 1, 1

    for r, c in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[r][c] == " ":
            return r, c

    for r, c in [(0, 1), (1, 0), (1, 2), (2, 1)]:
        if board[r][c] == " ":
            return r, c

def draw_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio
        g = BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio
        b = BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 60), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE + 60), (WIDTH, i * CELL_SIZE + 60), LINE_WIDTH)

def draw_marks():
    for row in range(3):
        for col in range(3):
            cx = col * CELL_SIZE + CELL_SIZE // 2
            cy = row * CELL_SIZE + CELL_SIZE // 2 + 60
            if board[row][col] == "X":
                offset = 30
                pygame.draw.line(screen, X_COLOR, (cx - offset, cy - offset), (cx + offset, cy + offset), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, (cx + offset, cy - offset), (cx - offset, cy + offset), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, O_COLOR, (cx, cy), CELL_SIZE // 2 - 20, LINE_WIDTH)

def draw_turn():
    if game_active and not game_over:
        icon = "🧠" if player == "X" else "🔥"
        turn_text = FONT.render(f"{icon} {player}'s Turn", True, TEXT_COLOR)
        screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 15))

def check_winner():
    global winner, game_over, winning_line
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            winner = board[i][0]
            winning_line = ("row", i)
            game_over = True
            (win_sound if winner == "X" else lose_sound).play()
            return
        if board[0][i] == board[1][i] == board[2][i] != " ":
            winner = board[0][i]
            winning_line = ("col", i)
            game_over = True
            (win_sound if winner == "X" else lose_sound).play()
            return
    if board[0][0] == board[1][1] == board[2][2] != " ":
        winner = board[0][0]
        winning_line = ("diag", 1)
        game_over = True
        (win_sound if winner == "X" else lose_sound).play()
        return
    if board[0][2] == board[1][1] == board[2][0] != " ":
        winner = board[0][2]
        winning_line = ("diag", 2)
        game_over = True
        (win_sound if winner == "X" else lose_sound).play()
        return
    if all(cell != " " for row in board for cell in row):
        winner = "Tie"
        game_over = True
        tie_sound.play()

def draw_winning_line():
    if not winning_line:
        return
    if winning_line[0] == "row":
        y = winning_line[1] * CELL_SIZE + CELL_SIZE // 2 + 60
        pygame.draw.line(screen, HIGHLIGHT_COLOR, (20, y), (WIDTH - 20, y), 8)
    elif winning_line[0] == "col":
        x = winning_line[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.line(screen, HIGHLIGHT_COLOR, (x, 70), (x, HEIGHT - 20), 8)
    elif winning_line[0] == "diag":
        if winning_line[1] == 1:
            pygame.draw.line(screen, HIGHLIGHT_COLOR, (20, 70), (WIDTH - 20, HEIGHT - 20), 8)
        else:
            pygame.draw.line(screen, HIGHLIGHT_COLOR, (WIDTH - 20, 70), (20, HEIGHT - 20), 8)

def draw_creator():
    text = SMALL_FONT.render("🧑‍💻 Game developed by Adhishresth Srivastava", True, TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 30))

def draw_button(text, x, y, w, h, hovered=False):
    color = (180, 0, 0) if hovered else (200, 50, 50)
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=8)
    label = FONT.render(text, True, TEXT_COLOR)
    screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))

def draw_welcome_screen():
    draw_background()
    title = BIG_FONT.render("🕹️ Let's Play Tic-Tac-Toe!", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 5))
    mx, my = pygame.mouse.get_pos()

    hovered = WIDTH // 2 - 60 <= mx <= WIDTH // 2 + 60 and HEIGHT // 2 <= my <= HEIGHT // 2 + 50
    draw_button("2 Player", WIDTH // 2 - 60, HEIGHT // 2, 120, 50, hovered)

    hovered = WIDTH // 2 - 60 <= mx <= WIDTH // 2 + 60 and HEIGHT // 2 + 60 <= my <= HEIGHT // 2 + 110
    draw_button("Computer", WIDTH // 2 - 60, HEIGHT // 2 + 60, 120, 50, hovered)

    draw_creator()

def draw_result_screen():
    draw_background()
    result_msg = "🤝 It's a Tie!" if winner == "Tie" else f"🎉 {winner} Wins!"
    text = BIG_FONT.render(result_msg, True, TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))
    mx, my = pygame.mouse.get_pos()

    hovered = WIDTH // 2 - 80 <= mx <= WIDTH // 2 + 80 and HEIGHT // 2 <= my <= HEIGHT // 2 + 50
    draw_button("🔁 Play Again", WIDTH // 2 - 80, HEIGHT // 2, 160, 50, hovered)

    hovered = WIDTH // 2 - 80 <= mx <= WIDTH // 2 + 80 and HEIGHT // 2 + 60 <= my <= HEIGHT // 2 + 110
    draw_button("🏠 Home", WIDTH // 2 - 80, HEIGHT // 2 + 60, 160, 50, hovered)

    draw_creator()

# === Main loop ===
running = True
while running:
    if not game_active:
        draw_welcome_screen()
    elif game_over:
        draw_result_screen()
    else:
        draw_background()
        draw_grid()
        draw_marks()
        draw_turn()
        if winner and winner != "Tie":
            draw_winning_line()
        draw_creator()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 60 <= x <= WIDTH // 2 + 60 and HEIGHT // 2 <= y <= HEIGHT // 2 + 50:
                    game_active = True
                    mode = "2 Player"
                elif WIDTH // 2 - 60 <= x <= WIDTH // 2 + 60 and HEIGHT // 2 + 60 <= y <= HEIGHT // 2 + 110:
                    game_active = True
                    mode = "Computer"

        elif game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 80 <= x <= WIDTH // 2 + 80 and HEIGHT // 2 <= y <= HEIGHT // 2 + 50:
                    board = [[" " for _ in range(3)] for _ in range(3)]
                    game_active = True
                    game_over = False
                    winner = None
                    player = "X"
                    winning_line = None
                elif WIDTH // 2 - 80 <= x <= WIDTH // 2 + 80 and HEIGHT // 2 + 60 <= y <= HEIGHT // 2 + 110:
                    board = [[" " for _ in range(3)] for _ in range(3)]
                    game_active = False
                    game_over = False
                    winner = None
                    mode = None
                    player = "X"
                    winning_line = None

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < 60:
                    continue
                row, col = (y - 60) // CELL_SIZE, x // CELL_SIZE
                if board[row][col] == " ":
                    board[row][col] = player
                    click_sound.play()
                    check_winner()
                    if not game_over:
                        player = "O" if player == "X" else "X"

            if mode == "Computer" and player == "O" and not game_over:
                pygame.time.wait(300)
                row, col = ai_move()
                board[row][col] = player
                check_winner()
                if not game_over:
                    player = "X"

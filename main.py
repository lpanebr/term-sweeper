import random

# Constants for the game
N = 8  # Size of the board (8x8)
B = 10  # Number of mines

# ANSI color codes for colored output in terminal
COLORS = {
    "RESET": "\033[0m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    "BOLD": "\033[1m",
    "DIM": "\033[2m",
    "UNDERLINE": "\033[4m",
}

def initialize_board():
    # Initialize the board with mines and visibility matrix
    mines = [[0 for _ in range(N)] for _ in range(N)]
    visible = [[0 for _ in range(N)] for _ in range(N)]

    # Place mines randomly on the board
    placed_mines = 0
    while placed_mines < B:
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        if mines[x][y] == 0:
            mines[x][y] = 1
            placed_mines += 1

    return mines, visible

def print_board(visible, mines):
    # Print the current state of the board with colors
    print("  ", end="")
    for i in range(1, N + 1):
        print(COLORS["BOLD"] + COLORS["CYAN"] + chr(64 + i) + COLORS["RESET"], end=" ")
    print()

    for y in range(N):
        print(COLORS["BOLD"] + COLORS["CYAN"] + str(y + 1) + COLORS["RESET"], end=" ")
        for x in range(N):
            if visible[x][y] == 0:
                print(".", end=" ")
            elif visible[x][y] == 2:
                print(COLORS["YELLOW"] + "X" + COLORS["RESET"], end=" ")  # Flag for marked bombs
            else:
                count = count_surrounding_mines(mines, x, y)
                if mines[x][y] == 1:
                    print(COLORS["RED"] + "X" + COLORS["RESET"], end=" ")
                else:
                    color = COLORS["WHITE"]
                    if count == 1:
                        color = COLORS["BLUE"]
                    elif count == 2:
                        color = COLORS["GREEN"]
                    elif count == 3:
                        color = COLORS["YELLOW"]
                    elif count >= 4:
                        color = COLORS["RED"]
                    print(color + str(count) + COLORS["RESET"], end=" ")
        print()

def count_surrounding_mines(mines, x, y):
    # Count the number of mines surrounding a given cell
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if 0 <= x + dx < N and 0 <= y + dy < N:
                count += mines[x + dx][y + dy]
    return count

def reveal_mines(mines):
    # Reveal all mines on the board
    for x in range(N):
        for y in range(N):
            if mines[x][y] == 1:
                print(f"MINE AT {chr(64 + x + 1)}{y + 1}")

def reveal_adjacent(visible, mines, x, y):
    # Reveal all immediate surrounding cells of a given coordinate
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y + dy
            if (dx != 0 or dy != 0) and 0 <= nx < N and 0 <= ny < N:
                if visible[nx][ny] == 0:  # Only reveal if not already visible
                    visible[nx][ny] = 1
                    if mines[nx][ny] == 1:
                        # If a mine is found, reveal all mines and end the game
                        print(f"VOCÊ ACERTOU UMA MINA EM {chr(64 + nx + 1)}{ny + 1}! GAME OVER.")
                        reveal_mines(mines)
                        return True  # Signal that a mine was found
    return False  # No mine was found

def toggle_flag(visible, x, y):
    # Toggle the flag for marking or unmarking a cell as a suspected bomb
    if visible[x][y] == 0:
        visible[x][y] = 2  # Mark as suspected bomb
    elif visible[x][y] == 2:
        visible[x][y] = 0  # Unmark as suspected bomb

def check_victory(visible, mines):
    # Check if all non-mine cells are revealed
    for x in range(N):
        for y in range(N):
            if visible[x][y] == 0 and mines[x][y] == 0:
                return False
    return True

def play_game():
    print(COLORS["BOLD"] + "*** MINESWEEPER PARA COMMODORE 64 ***" + COLORS["RESET"])
    print(COLORS["CYAN"] + "INSTRUÇÕES:" + COLORS["RESET"])
    print("1. DIGITE UMA COORDENADA PARA REVELAR UMA CÉLULA (POR EXEMPLO, A5)")
    print("2. DIGITE 'Q' PARA SAIR DO JOGO")
    print("3. DIGITE 'ZA5' PARA REVELAR TODAS AS CÉLULAS AO REDOR DE A5")
    print("4. DIGITE 'XA5' PARA MARCAR/DESMARCAR A5 COMO UMA BOMBA")
    print()

    mines, visible = initialize_board()
    print_board(visible, mines)

    while True:
        coord = input("DIGITE A COORDENADA (EXEMPLO: A1): ").upper()
        if coord == "Q":
            break

        if len(coord) < 2:
            print("COORDENADA INVÁLIDA")
            continue

        # Handle special commands
        if coord[0] == 'Z':
            prefix = 'Z'
        elif coord[0] == 'X':
            prefix = 'X'
        else:
            prefix = ''

        try:
            x = ord(coord[len(prefix)]) - 65
            y = int(coord[len(prefix)+1:]) - 1
        except ValueError:
            print("COORDENADA INVÁLIDA")
            continue

        if x < 0 or x >= N or y < 0 or y >= N:
            print("COORDENADA INVÁLIDA")
            continue

        if prefix == 'Z':
            # Reveal adjacent cells without changing the center cell
            if reveal_adjacent(visible, mines, x, y):
                break  # End game if a mine was found
            print_board(visible, mines)
            if check_victory(visible, mines):
                print(COLORS["GREEN"] + COLORS["BOLD"] + "PARABÉNS! VOCÊ VENCEU O JOGO!" + COLORS["RESET"])
                break
            continue

        if prefix == 'X':
            # Toggle flag for the cell
            toggle_flag(visible, x, y)
            print_board(visible, mines)
            continue

        if visible[x][y] == 1:
            print("JÁ REVELADO")
            continue

        visible[x][y] = 1

        if mines[x][y] == 1:
            print(f"VOCÊ ACERTOU UMA MINA EM {chr(64 + x + 1)}{y + 1}! GAME OVER.")
            reveal_mines(mines)
            break

        print_board(visible, mines)

        if check_victory(visible, mines):
            print(COLORS["GREEN"] + COLORS["BOLD"] + "PARABÉNS! VOCÊ VENCEU O JOGO!" + COLORS["RESET"])
            break

play_game()

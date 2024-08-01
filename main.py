import random

# Constants for the game
N = 8  # Size of the board (8x8)
B = 10  # Number of mines

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
    # Print the current state of the board
    print("  ", end="")
    for i in range(1, N + 1):
        print(chr(64 + i), end=" ")
    print()

    for y in range(N):
        print(y + 1, end=" ")
        for x in range(N):
            if visible[x][y] == 0:
                print(".", end=" ")
            elif visible[x][y] == 2:
                print("F", end=" ")  # Flag for marked bombs
            else:
                # Count surrounding mines
                count = count_surrounding_mines(mines, x, y)
                print(count, end=" ")
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

def reveal_surroundings(visible, mines, x, y):
    # Reveal all surrounding cells of a given coordinate
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                if mines[nx][ny] == 1:
                    # If a mine is found, reveal all mines and end the game
                    print(f"VOCÊ ACERTOU UMA MINA EM {chr(64 + nx + 1)}{ny + 1}! GAME OVER.")
                    reveal_mines(mines)
                    return True  # Signal that a mine was found
                if visible[nx][ny] == 0:  # Only reveal if not already visible
                    visible[nx][ny] = 1
                    # Check for surrounding mines
                    if count_surrounding_mines(mines, nx, ny) == 0:
                        # If no mines around, recursively reveal further
                        reveal_surroundings(visible, mines, nx, ny)
    return False  # No mine was found

def play_game():
    print("*** MINESWEEPER PARA COMMODORE 64 ***")
    print("INSTRUÇÕES:")
    print("1. DIGITE UMA COORDENADA PARA REVELAR UMA CÉLULA (POR EXEMPLO, A5)")
    print("2. DIGITE 'Q' PARA SAIR DO JOGO")
    print("3. DIGITE 'ZA5' PARA REVELAR TODAS AS CÉLULAS AO REDOR DE A5")
    print("4. DIGITE 'XA5' PARA MARCAR A5 COMO UMA BOMBA")
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
            # Reveal surroundings
            if reveal_surroundings(visible, mines, x, y):
                break  # End game if a mine was found
            print_board(visible, mines)
            continue

        if prefix == 'X':
            # Mark a bomb
            visible[x][y] = 2
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

play_game()

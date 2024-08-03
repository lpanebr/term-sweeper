import random
import time
import os

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


def clear_screen():
    # Clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(visible, mines, mines_left, elapsed_time, game_over=False):
    # Clear the screen before printing the new board
    clear_screen()

    print("    ", end="")
    for i in range(1, N + 1):
        print(COLORS["DIM"] + chr(64 + i) + COLORS["RESET"], end=" ")
    print()
    # Print the top border and column labels
    print(COLORS["DIM"] + "  ┌" + "──" * N + "─┐" + COLORS["RESET"])

    # Print each row with row labels on both sides
    for y in range(N):
        print(COLORS["DIM"] + f"{y + 1} │" + COLORS["RESET"], end=" ")
        for x in range(N):
            if game_over and mines[x][y] == 1:
                print(COLORS["RED"] + "◉" + COLORS["RESET"],
                      end=" ")  # Show mines as ◉ on game over
            elif visible[x][y] == 0:
                print("▢", end=" ")  # Use ▢ for cells not revealed
            elif visible[x][y] == 2:
                print(COLORS["RED"] + "▸" + COLORS["RESET"],
                      end=" ")  # Use ▸ for flagged cells
            else:
                count = count_surrounding_mines(mines, x, y)
                if count == 0:
                    print(
                        " ", end=" "
                    )  # Show empty space for cells with no adjacent mines
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
        print(COLORS["DIM"] + f"│ {y + 1}" + COLORS["RESET"])

    # Print the bottom border and column labels
    print(COLORS["DIM"] + "  └" + "──" * N + "─┘" + COLORS["RESET"])
    print("    ", end="")
    for i in range(1, N + 1):
        print(COLORS["DIM"] + chr(64 + i) + COLORS["RESET"], end=" ")
    print()

    # Display remaining mines and elapsed time
    print(f"\nMINAS: {mines_left}")
    print(f"TEMPO: {elapsed_time}")


def count_surrounding_mines(mines, x, y):
    # Count the number of mines surrounding a given cell
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if 0 <= x + dx < N and 0 <= y + dy < N:
                count += mines[x + dx][y + dy]
    return count


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
                        print(
                            f"VOCÊ ACERTOU UMA MINA EM {chr(64 + nx + 1)}{ny + 1}! GAME OVER."
                        )
                        print_board(visible, mines, 0, 0,
                                    game_over=True)  # Show mines
                        return True  # Signal that a mine was found
    return False  # No mine was found


def auto_reveal(visible, mines, x, y):
    # Automatically reveal adjacent cells if the selected cell is empty (no surrounding mines)
    queue = [(x, y)]
    visited = set(queue)

    while queue:
        cx, cy = queue.pop(0)
        if count_surrounding_mines(mines, cx, cy) == 0:
            # If no mines around, reveal all adjacent cells
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = cx + dx, cy + dy
                    if (0 <= nx < N
                            and 0 <= ny < N) and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        if visible[nx][ny] == 0:
                            visible[nx][ny] = 1
                            if count_surrounding_mines(mines, nx, ny) == 0:
                                queue.append((nx, ny))


def toggle_flag(visible, x, y):
    # Toggle the flag for marking or unmarking a cell as a suspected bomb
    if visible[x][y] == 0:
        visible[x][y] = 2  # Mark as suspected bomb
    elif visible[x][y] == 2:
        visible[x][y] = 0  # Unmark as suspected bomb


def check_victory(visible, mines):
    # Check if all non-mine cells are revealed and all mine cells are marked
    for x in range(N):
        for y in range(N):
            # Check if there are any non-mine cells that are not revealed
            if visible[x][y] == 0 and mines[x][y] == 0:
                return False
            # Check if there are any mine cells that are not marked
            if mines[x][y] == 1 and visible[x][y] != 2:
                return False
    return True


def play_game():
    print(COLORS["BOLD"] + "*** MINESWEEPER PARA COMMODORE 64 ***" +
          COLORS["RESET"])
    print(COLORS["CYAN"] + "INSTRUÇÕES:" + COLORS["RESET"])
    print("1. DIGITE UMA COORDENADA PARA REVELAR UMA CÉLULA (POR EXEMPLO, A5)")
    print("2. DIGITE 'Q' PARA SAIR DO JOGO")
    print("3. DIGITE 'ZA5' PARA REVELAR TODAS AS CÉLULAS AO REDOR DE A5")
    print("4. DIGITE 'XA5' PARA MARCAR/DESMARCAR A5 COMO UMA BOMBA")
    print()

    while True:
        mines, visible = initialize_board()
        first_move = True
        start_time = 0

        while True:
            # Calculate the number of unmarked mines
            marked_flags = sum(row.count(2) for row in visible)
            mines_left = B - marked_flags

            # Calculate elapsed time
            if not first_move:
                elapsed_time = int(time.time() - start_time)
            else:
                elapsed_time = 0

            print_board(visible, mines, mines_left, elapsed_time)

            coord = input("DIGITE A COORDENADA (EXEMPLO: A1): ").upper()
            if coord == "Q":
                choice = input("VOCÊ DESEJA JOGAR NOVAMENTE? (S/N): ").upper()
                if choice == "N":
                    return  # Termina o jogo
                elif choice == "S":
                    break  # Reinicia o loop para começar um novo jogo
                else:
                    print(
                        "OPÇÃO INVÁLIDA. DIGITE 'S' PARA SIM OU 'N' PARA NÃO.")
                    continue

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
                y = int(coord[len(prefix) + 1:]) - 1
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
                print_board(visible, mines, mines_left, elapsed_time)
                if check_victory(visible, mines):
                    print(COLORS["GREEN"] + COLORS["BOLD"] +
                          "PARABÉNS! VOCÊ VENCEU O JOGO!" + COLORS["RESET"])
                    break
                continue

            if prefix == 'X':
                # Toggle flag for the cell
                if visible[x][y] in (0, 2):  # Only toggle if not revealed
                    toggle_flag(visible, x, y)
                else:
                    print(
                        "CÉLULA JÁ REVELADA. NÃO PODE SER MARCADA COMO BOMBA.")
                print_board(visible, mines, mines_left, elapsed_time)
                continue

            if visible[x][y] == 1:
                print("JÁ REVELADO")
                continue

            if first_move:
                start_time = time.time()
                first_move = False

            visible[x][y] = 1

            # Automatically reveal adjacent cells if the revealed cell is empty
            if count_surrounding_mines(mines, x, y) == 0:
                auto_reveal(visible, mines, x, y)

            if mines[x][y] == 1:
                print(
                    f"VOCÊ ACERTOU UMA MINA EM {chr(64 + x + 1)}{y + 1}! GAME OVER."
                )
                print_board(visible, mines, 0, 0, game_over=True)  # Show mines
                break

            print_board(visible, mines, mines_left, elapsed_time)

            if check_victory(visible, mines):
                print(COLORS["GREEN"] + COLORS["BOLD"] +
                      "PARABÉNS! VOCÊ VENCEU O JOGO!" + COLORS["RESET"])
                break

        # Ask if the player wants to play again
        choice = input("VOCÊ DESEJA JOGAR NOVAMENTE? (S/N): ").upper()
        if choice == "N":
            break
        elif choice == "S":
            continue  # Reinicia o jogo
        else:
            print("OPÇÃO INVÁLIDA. DIGITE 'S' PARA SIM OU 'N' PARA NÃO.")


play_game()

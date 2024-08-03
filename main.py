import random
import time
import os
import re

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

# Instructions for the game
instructions = (
    f"{COLORS['BOLD']}{COLORS['BLUE']}TermSweeper{COLORS['RESET']}\n\n"
    f"{COLORS['CYAN']}INSTRUCTIONS{COLORS['RESET']}\n"
    f"{COLORS['GREEN']}1. Open a cell:{COLORS['RESET']} Enter a coordinate (e.g., a5)\n"
    f"{COLORS['GREEN']}2. Exit the game:{COLORS['RESET']} q\n"
    f"{COLORS['GREEN']}3. Open surrounding cells:{COLORS['RESET']} Use z as a prefix (e.g., za5)\n"
    f"{COLORS['GREEN']}4. Flag/unflag a mine:{COLORS['RESET']} Use f as a prefix (e.g., fa5)\n"
    f"{COLORS['GREEN']}5. Show/Hide help instructions:{COLORS['RESET']} h"
)


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
    os.system("cls" if os.name == "nt" else "clear")


def print_board(
    visible,
    mines,
    mines_left,
    elapsed_time,
    show_instructions,
    warning="",
    victory="",
    game_over_msg="",
):
    # Clear the screen before printing the new board
    clear_screen()

    # Print column labels
    print("    ", end="")
    for i in range(1, N + 1):
        print(COLORS["DIM"] + chr(64 + i) + COLORS["RESET"], end=" ")
    print()

    # Print the top border
    print(COLORS["DIM"] + "  ┌" + "──" * N + "─┐" + COLORS["RESET"])

    # Print each row with row labels on both sides
    for y in range(N):
        print(COLORS["DIM"] + f"{y + 1} │" + COLORS["RESET"], end=" ")
        for x in range(N):
            # Show mines on game over
            if game_over_msg and mines[x][y] == 1:
                print(
                    COLORS["RED"] + "◉" + COLORS["RESET"], end=" "
                )  # Show mines as ◉ on game over
            elif visible[x][y] == 0:
                print("▩", end=" ")  # Use ▩ for cells not revealed
            elif visible[x][y] == 2:
                print(
                    COLORS["RED"] + "▩" + COLORS["RESET"], end=" "
                )  # Use ▩ for flagged cells
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
    print(f"\nMINES: {mines_left}")
    print(f"TIME: {elapsed_time}")

    # Show warning if provided
    if warning:
        print()
        print_boxed_text(warning, COLORS["YELLOW"], COLORS["WHITE"])

    # Show victory message if provided
    if victory:
        print()
        print_boxed_text(victory, COLORS["GREEN"], COLORS["WHITE"])

    # Show game over message if provided
    if game_over_msg:
        print()
        print_boxed_text(game_over_msg, COLORS["RED"], COLORS["YELLOW"])

    # Show instructions if the flag is set to True
    if show_instructions:
        print()
        print_boxed_text(instructions, COLORS["DIM"], COLORS["RESET"])


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
                        return f"You hit a mine at {chr(64 + nx + 1)}{ny + 1}! Game Over."  # Signal that a mine was found
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
                    if (0 <= nx < N and 0 <= ny < N) and (nx, ny) not in visited:
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


def print_boxed_text(text, border_color, text_color):
    reset_color = COLORS["RESET"]
    lines = text.split("\n")

    # Remove ANSI escape codes to calculate the correct length
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    stripped_lines = [ansi_escape.sub("", line) for line in lines]

    max_length = max(
        len(line) for line in stripped_lines
    )  # Find the maximum length of stripped lines

    # Print the top border
    print(border_color + "  ┌─" + "─" * max_length + "─┐" + reset_color)

    # Print each line within the box
    for line in lines:
        # Calculate padding
        stripped_line = ansi_escape.sub("", line)
        padding = max_length - len(stripped_line)

        # Print the text centered with padding spaces
        print(
            border_color
            + "  │ "
            + text_color
            + line
            + " " * padding
            + reset_color
            + border_color
            + " │"
        )

    # Print the bottom border
    print(border_color + "  └─" + "─" * max_length + "─┘" + reset_color)


def play_game():
    print()
    show_instructions = True  # Initialize the instructions display flag

    while True:
        mines, visible = initialize_board()
        first_move = True
        start_time = 0
        game_over_msg = ""  # Initialize the game over message variable
        warning_msg = ""  # Initialize the warning message variable
        victory_msg = ""  # Initialize the victory message variable
        game_over = False  # Initialize the game over flag

        while True:
            # Calculate the number of unmarked mines
            marked_flags = sum(row.count(2) for row in visible)
            mines_left = B - marked_flags

            # Calculate elapsed time
            if not first_move:
                elapsed_time = int(time.time() - start_time)
            else:
                elapsed_time = 0

            # Print the board once per iteration
            print_board(
                visible,
                mines,
                mines_left,
                elapsed_time,
                show_instructions,
                warning=warning_msg,
                victory=victory_msg,
                game_over_msg=game_over_msg,
            )

            # Reset messages for the next loop
            warning_msg = ""
            victory_msg = ""
            game_over_msg = ""  # Reset game over message to avoid repetition

            coord = input("ENTER COORDINATE (E.G., A1): ").upper()

            if coord == "H":
                # Toggle the instructions display flag
                show_instructions = not show_instructions
                continue

            if coord == "Q":
                choice = input("DO YOU WANT TO PLAY AGAIN? (Y/N): ").upper()
                if choice == "N":
                    return  # End the game
                elif choice == "Y":
                    break  # Restart the loop to start a new game
                else:
                    warning_msg = "INVALID OPTION. ENTER 'Y' FOR YES OR 'N' FOR NO."
                    continue

            if len(coord) < 2:
                warning_msg = "INVALID COORDINATE"
                continue

            # Handle special commands
            if coord[0] == "Z":
                prefix = "Z"
            elif coord[0] == "F":
                prefix = "F"
            else:
                prefix = ""

            try:
                x = ord(coord[len(prefix)]) - 65
                y = int(coord[len(prefix) + 1 :]) - 1
            except ValueError:
                warning_msg = "INVALID COORDINATE"
                continue

            if x < 0 or x >= N or y < 0 or y >= N:
                warning_msg = "INVALID COORDINATE"
                continue

            if prefix == "Z":
                # Reveal adjacent cells without changing the center cell
                result = reveal_adjacent(visible, mines, x, y)
                if result:
                    game_over_msg = result
                    game_over = True  # Set game over flag
                    break  # End game if a mine was found
                if check_victory(visible, mines):
                    victory_msg = "CONGRATULATIONS! YOU WON THE GAME!"
                    break
                continue

            if prefix == "F":
                # Toggle flag for the cell
                if visible[x][y] in (0, 2):  # Only toggle if not revealed
                    toggle_flag(visible, x, y)
                    # Check for victory after toggling a flag
                    if check_victory(visible, mines):
                        victory_msg = "CONGRATULATIONS! YOU WON THE GAME!"
                        break
                else:
                    warning_msg = "CELL ALREADY REVEALED. CANNOT BE MARKED AS A MINE."
                continue

            if visible[x][y] == 1:
                warning_msg = "ALREADY REVEALED"
                continue

            if first_move:
                start_time = time.time()
                first_move = False

            visible[x][y] = 1

            # Automatically reveal adjacent cells if the revealed cell is empty
            if count_surrounding_mines(mines, x, y) == 0:
                auto_reveal(visible, mines, x, y)

            if mines[x][y] == 1:
                game_over_msg = (
                    f"You hit a mine at {chr(64 + x + 1)}{y + 1}! Game Over."
                )
                game_over = True  # Set game over flag
                break

            if check_victory(visible, mines):
                victory_msg = "CONGRATULATIONS! YOU WON THE GAME!"
                break

        # Display game over message if game is over
        if game_over:
            print_board(
                visible,
                mines,
                0,
                elapsed_time,
                show_instructions=False,
                game_over_msg=game_over_msg,
            )
            print_boxed_text(game_over_msg, COLORS["RED"], COLORS["YELLOW"])
        elif victory_msg:  # Display victory message if player wins
            print_board(
                visible,
                mines,
                0,
                elapsed_time,
                show_instructions=False,
                victory=victory_msg,
            )

        # Ask if the player wants to play again
        choice = input("DO YOU WANT TO PLAY AGAIN? (Y/N): ").upper()
        if choice == "N":
            break
        elif choice == "Y":
            continue  # Restart the game
        else:
            print_boxed_text(
                "INVALID OPTION. ENTER 'Y' FOR YES OR 'N' FOR NO.",
                COLORS["YELLOW"],
                COLORS["WHITE"],
            )


play_game()

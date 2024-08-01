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
            else:
                # Count surrounding mines
                count = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= x + dx < N and 0 <= y + dy < N:
                            count += mines[x + dx][y + dy]
                print(count, end=" ")
        print()

def reveal_mines(mines):
    # Reveal all mines on the board
    for x in range(N):
        for y in range(N):
            if mines[x][y] == 1:
                print(f"MINE AT {chr(64 + x + 1)}{y + 1}")

def play_game():
    print("*** MINESWEEPER PARA COMMODORE 64 ***")
    print("INSTRUÇÕES:")
    print("1. DIGITE UMA COORDENADA PARA REVELAR UMA CÉLULA (POR EXEMPLO, A5)")
    print("2. DIGITE 'Q' PARA SAIR DO JOGO")
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
        
        try:
            x = ord(coord[0]) - 65
            y = int(coord[1:]) - 1
        except ValueError:
            print("COORDENADA INVÁLIDA")
            continue
        
        if x < 0 or x >= N or y < 0 or y >= N:
            print("COORDENADA INVÁLIDA")
            continue
        
        if visible[x][y] == 1:
            print("JÁ REVELADO")
            continue
        
        visible[x][y] = 1
        
        if mines[x][y] == 1:
            print("VOCÊ ACERTOU UMA MINA! GAME OVER.")
            reveal_mines(mines)
            break
        
        print_board(visible, mines)

play_game()
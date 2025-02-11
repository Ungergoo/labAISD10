import tkinter as tk
from tkinter import messagebox
import random

board = [[" "] * 3 for _ in range(3)]
buttons = [[None] * 3 for _ in range(3)]
game_running = True

def create_widgets(root):
    for row in range(3):
        for col in range(3):
            buttons[row][col] = tk.Button(root, text=" ", font=("Arial", 20, "bold"), width=6, height=3,
                                           command=lambda r=row, c=col: make_move(r, c, root))
            buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

    new_game_button = tk.Button(root, text="Новая игра", font=("Arial", 14), command=lambda: new_game(root))
    new_game_button.grid(row=3, column=0, columnspan=3, pady=10)

def make_move(row, col, root):
    global game_running
    if game_running and board[row][col] == " ":
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled")
        if check_winner("X"):
            end_game("Вы победили!")
            return
        root.after(500, lambda: computer_move(root))

def computer_move(root):
    global game_running
    if not game_running:
        return

    if try_to_win("O"):
        return

    if try_to_win("X", block=True):
        return

    random_move(root)

def try_to_win(smb, block=False):
    for row in range(3):
        if can_complete_line(row, 0, row, 1, row, 2, smb, block):
            return True
    for col in range(3):
        if can_complete_line(0, col, 1, col, 2, col, smb, block):
            return True
    if can_complete_line(0, 0, 1, 1, 2, 2, smb, block):
        return True
    if can_complete_line(2, 0, 1, 1, 0, 2, smb, block):
        return True
    return False

def can_complete_line(r1, c1, r2, c2, r3, c3, smb, block):
    line = [board[r1][c1], board[r2][c2], board[r3][c3]]
    if line.count(smb) == 2 and line.count(" ") == 1:
        empty_index = line.index(" ")
        row, col = [(r1, c1), (r2, c2), (r3, c3)][empty_index]
        board[row][col] = "O"
        buttons[row][col].config(text="O", state="disabled")
        if not block and check_winner("O"):  
            end_game("Компьютер победил!")
        return True
    return False

def random_move(root):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = "O"
        buttons[row][col].config(text="O", state="disabled")
        if check_winner("O"):
            end_game("Компьютер победил!")

def check_winner(player):
    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    if all(board[row][col] != " " for row in range(3) for col in range(3)):
        end_game("Ничья!")
        return False
    return False

def end_game(message):
    global game_running
    game_running = False
    messagebox.showinfo("Игра окончена", message)

def new_game(root):
    global game_running
    global board
    board = [[" "] * 3 for _ in range(3)]
    game_running = True
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=" ", state="normal")

def main():
    root = tk.Tk()
    root.title("Крестики-нолики")
    create_widgets(root)
    root.mainloop()

if __name__ == "__main__":
    main()

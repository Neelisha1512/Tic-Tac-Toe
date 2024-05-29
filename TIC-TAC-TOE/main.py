import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.current_player = "X"
        self.board = [0] * 9
        self.buttons = []
        self.single_player = False
        self.player_x_score = 0
        self.player_o_score = 0

        self.create_widgets()

    def create_widgets(self):
        self.mode_label = tk.Label(self.root, text="Choose Game Mode:", font=('Arial', 14),bg='lightblue')
        self.mode_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.single_player_button = tk.Button(self.root, text="Single Player", font=('Arial', 12),bg='lightblue',
                                              command=self.start_single_player)
        self.single_player_button.grid(row=1, column=0, columnspan=3, pady=5)

        self.multi_player_button = tk.Button(self.root, text="Multiplayer", font=('Arial', 12),bg='lightblue',
                                             command=self.start_multi_player)
        self.multi_player_button.grid(row=2, column=0, columnspan=3, pady=5)

        self.score_label = tk.Label(self.root, text=f"Player X: {self.player_x_score}  Player O: {self.player_o_score}",
                                    font=('Arial', 12))
        self.score_label.grid(row=3, column=0, columnspan=3, pady=10)

        for i in range(9):
            button = tk.Button(self.root, text="", font=('normal', 40), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i), bg="lightgray")
            button.grid(row=(i // 3) + 4, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        self.reset_button = tk.Button(self.root, text="Restart", font=('Arial', 12), command=self.restart_game)
        self.reset_button.grid(row=7, column=0, columnspan=3, pady=10)

    def start_single_player(self):
        self.single_player = True
        self.current_player = "X"
        self.mode_label.grid_remove()
        self.single_player_button.grid_remove()
        self.multi_player_button.grid_remove()

    def start_multi_player(self):
        self.single_player = False
        self.current_player = "X"
        self.mode_label.grid_remove()
        self.single_player_button.grid_remove()
        self.multi_player_button.grid_remove()

    def on_button_click(self, index):
        if self.board[index] == 0:
            if self.single_player:
                self.board[index] = -1
                self.buttons[index].config(text="X", bg="lightblue")
                if self.check_winner():
                    self.player_x_score += 1
                    self.update_score()
                    messagebox.showinfo("Tic-Tac-Toe", "Player X wins!")
                    self.disable_buttons()
                    return
                elif 0 not in self.board:
                    messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                    return
                self.comp_turn()
            else:
                self.board[index] = -1 if self.current_player == "X" else 1
                self.buttons[index].config(text=self.current_player,
                                           bg="lightblue" if self.current_player == "X" else "lightgreen")
                if self.check_winner():
                    if self.current_player == "X":
                        self.player_x_score += 1
                    else:
                        self.player_o_score += 1
                    self.update_score()
                    messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player} wins!")
                    self.disable_buttons()
                elif 0 not in self.board:
                    messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != 0:
                return True
        return False

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def restart_game(self):
        self.board = [0] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL, bg="lightgray")
        if self.single_player:
            self.start_single_player()
        else:
            self.start_multi_player()

    def update_score(self):
        self.score_label.config(text=f"Player X: {self.player_x_score}  Player O: {self.player_o_score}")

    def minmax(self, board, player):
        winner = self.analyze_board(board)
        if winner != 0:
            return winner * player
        pos = -1
        value = -2
        for i in range(9):
            if board[i] == 0:
                board[i] = player
                score = -self.minmax(board, -player)
                board[i] = 0
                if score > value:
                    value = score
                    pos = i
        if pos == -1:
            return 0
        return value

    def comp_turn(self):
        pos = -1
        value = -2
        for i in range(9):
            if self.board[i] == 0:
                self.board[i] = 1
                score = -self.minmax(self.board, -1)
                self.board[i] = 0
                if score > value:
                    value = score
                    pos = i
        self.board[pos] = 1
        self.buttons[pos].config(text="O", bg="lightgreen")
        if self.check_winner():
            self.player_o_score += 1
            self.update_score()
            messagebox.showinfo("Tic-Tac-Toe", "Computer wins!")
            self.disable_buttons()
        elif 0 not in self.board:
            messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")

    def analyze_board(self, board):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] != 0:
                return board[condition[0]]
        return 0


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

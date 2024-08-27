import tkinter as tk
import random

# Board size
BOARD_SIZE = 19
CELL_SIZE = DIFFER = 30  # Pixel size of each grid
COLS = ROWS = 16
WIDTH = BOARD_SIZE * CELL_SIZE
HEIGHT = DIFFER * (ROWS + 0.67)
o_x, o_y = 50, 30   # Define the coordinates of the upper left corner of the chessboard

class PlayerSelection:
  def __init__(self, root):
    self.root = root
    self.setup_window("Choose Player", "400x200+100+100")
    # Label for selection
    self.label = tk.Label(root, text = "Choose the Game Mode:")
    self.label.pack(pady = 5)
    # Radio buttons to select the game mode
    # Variable to store the selected player (default is two-player mode)
    self.move_var = tk.StringVar(value = "2p")
    self.move_var.trace("w", self.update_mode)
    self.two_player_button = tk.Radiobutton(root, text = "Two Players", variable = self.move_var, value = "2p")
    self.two_player_button.pack()
    self.ai_player_button = tk.Radiobutton(root, text = "Play Against AI", variable = self.move_var, value = "ai")
    self.ai_player_button.pack()

    # Difficult selection for AI
    self.difficulty_var = tk.StringVar(value = "Easy")
    self.easy_button = tk.Radiobutton(root, text = "Easy", variable = self.difficulty_var, value = "Easy")
    self.medium_button = tk.Radiobutton(root, text = "Medium", variable = self.difficulty_var, value = "Medium")
    self.hard_button = tk.Radiobutton(root, text = "Hard", variable = self.difficulty_var, value = "Hard")
    self.difficulty_buttons = [self.easy_button, self.medium_button, self.hard_button]

    # Initially disable difficulty selection
    self.set_difficulty_buttons_state(tk.DISABLED)

    # Button to start the game
    self.start_button = tk.Button(root, text = "Start Game", command = self.start_game)
    self.start_button.pack(pady = 10)

  def update_mode(self, *args):
    mode = self.move_var.get()
    if mode == "ai":
      self.set_difficulty_buttons_state(tk.NORMAL)
    else:
      self.set_difficulty_buttons_state(tk.DISABLED)

  def set_difficulty_buttons_state(self, state):
    for button in self.difficulty_buttons:
      button.pack()
      button.config(state = state)

  def start_game(self):
    mode = self.move_var.get()
    difficulty = self.difficulty_var.get() if mode == "ai" else None
    self.root.destroy() # Close the player selection window

    # Open the Gomoku game window
    game_window = tk.Tk()
    Gomoku(game_window, mode, difficulty)
    game_window.mainloop()

  def setup_window(self, title, geometry):
    self.root.title(title)
    self.root.geometry(geometry)

class Gomoku:
  def __init__(self, root, mode, difficulty = None) -> None:
    self.root = root
    self.root.title('Gomoku')
    self.board = [[0] * COLS for _ in range(ROWS)]
    self.cnt = 1
    self.current_player = 'black'
    self.mode = mode
    self.difficulty = difficulty
    self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='beige')
    self.canvas.bind('<Button-1>', self.place_chess)
    self.canvas.pack()

    self.win_label = tk.Label(root, text="")
    self.win_label.pack()
    button_frame = tk.Frame(root)
    button_frame.pack()
    self.reset_button = tk.Button(button_frame, text='Reset Game', font = ("Arial", 14), command=self.reset_game)
    self.reset_button.grid(row = 0, column = 0, padx = 5, pady = 10)
    self.change_mode = tk.Button(button_frame, text='Change Mode', font = ("Arial", 14), command=self.reset_mode)
    self.change_mode.grid(row = 0, column = 1, padx = 5, pady = 10)
    self.draw_board()

  def ai_mode(self):
    if self.difficulty == "Easy":
      self.ai_easy()
    elif self.difficulty == "Medium":
      self.ai_medium()
    elif self.difficulty == "Hard":
      self.ai_hard()

  def ai_easy(self):
    empty_positions = [(r, c) for r in range(ROWS) for c in range(COLS) if self.board[r][c] == 0]
    if empty_positions:
      row, col = random.choice(empty_positions)
      self.place_chess_ai(row, col)

  def ai_medium():
    pass

  def ai_hard():
    pass

  def place_chess_ai(self, row, col):
    # Determine color based on the counter (odd for black, even for white)
    color = 'black' if self.cnt % 2 != 0 else 'white'
    # Call the generic function to place the piece for the player
    self.place_chess_generic(row, col, color)

  def place_chess_player(self, row, col):
    # Determine color based on the counter (odd for black, even for white)
    color = 'black' if self.cnt % 2 != 0 else 'white'
    # Call the generic function to place the piece for the player
    self.place_chess_generic(row, col, color)
  
  def place_chess_generic(self, row, col, color):
    # Calculate the coordinates for placing the piece
    x1, y1 = o_x + col * DIFFER - 10, o_y + row * DIFFER - 10
    x2, y2 = x1 + 20, y1 + 20
    # Place the piece on the canvas
    self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    # Update the board with the corresponding color (1 for black, 2 for white)
    self.board[row][col] = 1 if color == 'black' else 2
    # Check for a winner after placing the piece
    if self.check_winner(row, col):
      winner = 'Black' if self.board[row][col] == 1 else 'White'
      self.win_label.config(text=f'{winner} wins!')
      self.canvas.unbind('<Button-1>')  # Disable further clicks if the game is over
    # Increment the counter to switch turns
    self.cnt += 1

  def draw_board(self):
    for i in range(ROWS):
      self.canvas.create_line(o_x, o_y + i * DIFFER, o_x + (COLS - 1) * DIFFER, o_y + i * DIFFER)
      self.canvas.create_line(o_x + i * DIFFER, o_y, o_x + i * DIFFER, o_y + (ROWS - 1) * DIFFER)
    
  def place_chess(self, event):
    x, y = event.x, event.y
    if o_x <= x <= o_x + (COLS - 1) * DIFFER and o_y <= y <= o_y + (ROWS - 1) * DIFFER:
      # Convert x and y to the row and column indices of the board
      col = round((x - o_x) / DIFFER)
      row = round((y - o_y) / DIFFER)

      # Check if the selected position is valid and not already occupied
      if 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == 0:
        # Place the piece for the player
        self.place_chess_player(row, col)
        # If in AI mode and no winner, let  the AI take its turn
        if self.mode == 'ai' and not self.check_winner(row, col):
          self.ai_mode()

  def check_winner(self, row, col):
    directions = [
      [(0, 1), (0, -1)],  # Horizontal
      [(1, 0), (-1, 0)],  # Vertical
      [(1, 1), (-1, -1)], # Diagonal \
      [(1, -1), (-1, 1)]  # Diagonal /
    ]
    for direction in directions:
      cnt = 1   # Including the current chess
      for dx, dy in direction:
        cnt += self.count_in_direction(row, col, dx, dy, self.board[row][col])
      if cnt >= 5:
        return True
    return False

  def count_in_direction(self, row, col, dx, dy, piece):
    cnt = 0
    x, y = row + dx, col + dy
    while 0 <= x < ROWS and 0 <= y < COLS and self.board[x][y] == piece:
      cnt += 1
      x += dx
      y += dy
    return cnt
  
  def reset_game(self):
    # Clear the board and reset variables
    self.board = [[0] * COLS for _ in range(ROWS)]
    self.cnt = 1
    self.current_player = 'black'
    self.canvas.delete('all')
    self.canvas.bind('<Button-1>', self.place_chess)
    self.draw_board()

  def reset_mode(self):
    # Close the current window and open a new PlayerSelection window
    self.root.destroy()
    player_select_window = tk.Tk()
    PlayerSelection(player_select_window)
    player_select_window.mainloop()

if __name__ == "__main__":
  root = tk.Tk()
  PlayerSelection(root)
  root.mainloop()

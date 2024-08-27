class Gomoku:
  def __init__(self, size = 19) -> None:
    # Initial the game size and the status
    self.size = size
    self.board = [[' ' for _ in range(size)] for _ in range(size)]
    self.current_player = 'X'

  def print_board(self):
    # Print the board
    for row in self.board:
      print(' '.join(row))
    print()

  def is_valid_move(self, x, y):
    # Check whether this position can place a chess piece
    return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == ' '

  def make_move(self, x, y):
    # Placing a chess, and is it successfully
    if self.is_valid_move(x, y):
      self.board[x][y] = self.current_player
      if self.check_winner(x, y):
        print(f"Player {self.current_player} wins!")
      else:
        self.switch_player()
      return True
    else:
      return False
    
  def switch_player(self):
    self.current_player = 'O' if self.current_player == 'X' else 'X'

  def check_winner(self, x, y):
    directions = [
      (0, 1),   # Horizontal
      (1, 0),   # Vertical
      (1, 1),   # Main Diagonal
      (-1, 1)   # Sub Diagonal
    ]
    for dx, dy in directions:
      cnt = 1
      # Check in one direction
      cnt += self.count_in_direction(x, y, dx, dy)
      # Check in the opposite direction
      cnt += self.count_in_direction(x, y, -dx, -dy)
      if cnt >= 5:
        return True
    return False

  def count_in_direction(self, x, y, dx, dy):
    cnt = 0
    nx, ny = x + dx, y + dy
    while 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
      cnt += 1
      nx += dx
      ny += dy
    return cnt

# Testing the initial and the basic operation
game = Gomoku()
game.print_board()

game.make_move(0, 0)
game.make_move(1, 1)
game.make_move(0, 1)
game.make_move(1, 2)
game.make_move(0, 2)
game.make_move(1, 3)
game.make_move(0, 3)
game.make_move(1, 4)
game.make_move(0, 4)
game.print_board()
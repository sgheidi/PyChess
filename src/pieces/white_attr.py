from common import *

class White_Attr(object):
  "A global namespace for attributes relating to white pieces."

  def __init__(self):
    self.blocks = [[0 for i in range(8)] for j in range(8)]
    for row in range(8):
      for col in range(8):
        self.blocks[row][col] = 1 if row == 6 or row == 7 else 0
    self.lose = False
    self.turn = True
    self.checker = ""
    self.num_queens = 1
    self.en_passant = [0 for i in range(8)]
    self.castled = 0
    self.opening_book = 0
    self.ai = 0
    self.verbose = 0

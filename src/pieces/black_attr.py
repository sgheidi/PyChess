from common import *

class Black_Attr(object):
  "A global namespace for attributes relating to black pieces."

  def __init__(self):
    # * AI rewards *
    self.PASSED_PAWN_REWARD = 0.0
    self.CONNECTED_PASSED_PAWN_REWARD = 0.0
    self.KNIGHT_OUTPOST_REWARD = 0.0
    self.PAWN_STRUCTURE_REWARD = 0.0
    self.BISHOP_PAIR_REWARD = 0.0
    self.KING_SAFETY_REWARD = 0.0
    self.PROMOTION_REWARD = 0.0
    self.RBQ_OPENFILE_REWARD = 0.0
    # ********************
    self.blocks = [[0 for i in range(8)] for j in range(8)]
    for row in range(8):
      for col in range(8):
        self.blocks[row][col] = 1 if row == 0 or row == 1 else 0
    self.lose = False
    self.turn = False
    self.checker = ""
    self.num_queens = 1
    self.en_passant = [0 for i in range(8)]
    self.castled = 0
    self.opening_book = 0
    self.ai = 1
    self.verbose = 0
    self.still_opening = 1
    if testing:
      self.turn = True

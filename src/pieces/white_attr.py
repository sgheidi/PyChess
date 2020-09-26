from common import *

class White_Attr(object):
  "A global namespace for attributes relating to white pieces."

  def __init__(self):
    # * AI rewards and penalties *
    self.PASSED_PAWN_REWARD = 0.0
    self.CONNECTED_PASSED_PAWN_REWARD = 0.0
    self.KNIGHT_OUTPOST_REWARD = 0.0
    self.PAWN_STRUCTURE_REWARD = 0.0
    self.BISHOP_PAIR_REWARD = 0.0
    self.KING_SAFETY_REWARD = 0.0
    self.PROMOTION_REWARD = 0.0
    self.RBQ_OPENFILE_REWARD = 0.05
    self.STACKED_PAWNS_PENALTY = 0.0
    # ********************
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

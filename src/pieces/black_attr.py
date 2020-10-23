from common import *

class Black_Attr(object):
  "A global namespace for attributes relating to black pieces."

  def __init__(self):
    # this is a constant that introduces randomness to the AI's moves within n.
    # that is, if the best move is evaluated as x, then the AI will choose a random move
    # in the bounds with evaluation [x - n, x]. Default n = 0.15
    self.AI_RANDOMNESS_THRESHOLD = 0.15
    # * AI rewards and penalties *
    self.PASSED_PAWN_REWARD = 0.0
    self.CONNECTED_PASSED_PAWN_REWARD = 2.8
    self.KNIGHT_OUTPOST_REWARD = 2.5
    self.BISHOP_OUTPOST_REWARD = 1.2
    self.BISHOP_PAIR_REWARD = 0.90
    # king should be in its sides' corner when not in endgame
    self.KING_SAFETY_REWARD = 0.0
    self.PROMOTION_REWARD = 0.0
    self.RBQ_OPENFILE_REWARD = 0.05
    self.N_STACKED_PAWNS_PENALTY = [1.2, 2.5, 3.0]
    self.EARLY_PIECE_DEVELOPMENT_REWARD = 0.0
    self.KNIGHT_FORK_REWARD = 0.0
    self.CONNECTED_PAWNS_REWARD = 0.0

    self.ISOLATED_PAWN_PENALTY = 0.6
    self.PROTECTED_PAST_PAWN_REWARD = 2.2
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
    self.opening_book = 1
    if len(sys.argv) == 1:
      self.ai = 0
    else:
      if sys.argv[1] == "--black":
        self.ai = 0
      else:
        self.ai = 1
    self.verbose = 0
    self.still_opening = 1
    if testing:
      self.turn = True

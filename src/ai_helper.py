from common import *

class Helper(object):
  def shuffle(self, di):
    "Shuffle dict `di`."
    temp = di.copy()
    new_di = {}
    for i in temp.copy():
      a = random.choice(list(temp.keys()))
      new_di[a] = temp[a]
      temp.pop(a)
    return new_di

  def get_all_black_moves(self):
    "Returns a dictionary containing all pieces and valid moves."
    moves = {}
    if BlackKing.alive and BlackKing.movelist != []:
      moves["K"] = BlackKing.movelist.copy()
      if Black_.castle_criteria_king():
        moves["K"].append("CK")
      if Black_.castle_criteria_queen():
        moves["K"].append("CQ")
    for i in range(Black.num_queens):
      if BlackQueen.alive[i] and BlackQueen.movelist[i] != []:
        moves["Q" + str(i)] = BlackQueen.movelist[i].copy()
    for i in range(2):
      if BlackBishop.alive[i] and BlackBishop.movelist[i] != []:
        moves["B" + str(i)] = BlackBishop.movelist[i].copy()
      if BlackKnight.alive[i] and BlackKnight.movelist[i] != []:
        moves["N" + str(i)] = BlackKnight.movelist[i].copy()
      if BlackRook.alive[i] and BlackRook.movelist[i] != []:
        moves["R" + str(i)] = BlackRook.movelist[i].copy()
    for i in range(8):
      if BlackPawn.alive[i] and BlackPawn.movelist[i] != []:
        moves["P" + str(i)] = BlackPawn.movelist[i].copy()
    return self.shuffle(moves)

  def get_all_white_moves(self):
    "Returns a dictionary containing all pieces and valid moves."
    moves = {}
    if WhiteKing.alive and WhiteKing.movelist != []:
      moves["K"] = WhiteKing.movelist.copy()
      if White_.castle_criteria_king():
        moves["K"].append("CK")
      if White_.castle_criteria_queen():
        moves["K"].append("CQ")
    for i in range(White.num_queens):
      if WhiteQueen.alive[i] and WhiteQueen.movelist[i] != []:
        moves["Q" + str(i)] = WhiteQueen.movelist[i].copy()
    for i in range(8):
      if WhitePawn.alive[i] and WhitePawn.movelist[i] != []:
        moves["P" + str(i)] = WhitePawn.movelist[i].copy()
    for i in range(2):
      if WhiteBishop.alive[i] and WhiteBishop.movelist[i] != []:
        moves["B" + str(i)] = WhiteBishop.movelist[i].copy()
      if WhiteKnight.alive[i] and WhiteKnight.movelist[i] != []:
        moves["N" + str(i)] = WhiteKnight.movelist[i].copy()
      if WhiteRook.alive[i] and WhiteRook.movelist[i] != []:
        moves["R" + str(i)] = WhiteRook.movelist[i].copy()
    return self.shuffle(moves)

  def good_pawn_structure_black(self):
    """A bad pawn structure is, for example, {1, 0, 1, 0, 1, 0, 1, 0}: where any subset of
    the set of 8 pawns are alternating as 1 -> 0 or 0 -> 1. Avoid this (causes weak light/dark
    squares in the spaces in between).
    """
    # fix. this is difficult
    return False
    for i in range(8):
      if BlackPawn.alive[i]:
        if i <= 5:
          if (BlackPawn.col[i+2] == (BlackPawn.col[i] + 2)) and BlackPawn.col[i-1]:
            return False
        elif i >= 2:
          if BlackPawn.col[i-2] == (BlackPawn.col[i] - 2):
            return False
    return True

  def RBQ_openfiles_black(self, score):
    "R, B, Q get rewards for as many moves they have in their movelists (i.e len(movelist))."
    for i in range(Black.num_queens):
      score -= Black.RBQ_OPENFILE_REWARD*len(BlackQueen.movelist[i])
    for i in range(2):
      score -= Black.RBQ_OPENFILE_REWARD*len(BlackRook.movelist[i])
      score -= Black.RBQ_OPENFILE_REWARD*len(BlackBishop.movelist[i])
    return score

  def RBQ_openfiles_white(self, score):
    "R, B, Q get rewards for as many moves they have in their movelists (i.e len(movelist))."
    for i in range(White.num_queens):
      score += White.RBQ_OPENFILE_REWARD*len(WhiteQueen.movelist[i])
    for i in range(2):
      score += White.RBQ_OPENFILE_REWARD*len(WhiteRook.movelist[i])
      score += White.RBQ_OPENFILE_REWARD*len(WhiteBishop.movelist[i])
    return score

  def knight_outpost_black(self, score):
    """A good knight outpost is where it is protected by a pawn, and no enemy pawns can attack it,
    either because no enemy pawns are on parallel files or the knight is on the same row or ahead
    of them.
    """
    pass

  def knight_fork_black(self, score):
    "Forking rooks and queens with knight has a very high reward."
    pass

  def early_piece_development_black(self, score):
    "A moderate score is given for early piece development of non-pawn pieces."
    pass

  def evaluate_pos(self):
    """Evaluation current board position. Returns a number.
    Low eval number -> good for black.
    High eval number -> good for white.
    """
    score = 0
    if BlackKing.alive:
      score -= 5
    for i in range(Black.num_queens):
      if BlackQueen.alive[i]:
        score -= 9
    for i in range(8):
      if BlackPawn.alive[i]:
        score -= 1
        # promote
        if BlackPawn.row[i] == 7:
          score -= 10
    for i in range(2):
      if BlackBishop.alive[i]:
        score -= 3
      if BlackKnight.alive[i]:
        score -= 3
      if BlackRook.alive[i]:
        score -= 5
    if Black.castled == 1:
      score -= 1.0
    if BlackBishop.alive[0] and BlackBishop.alive[1]:
      score -= Black.BISHOP_PAIR_REWARD
    score = self.RBQ_openfiles_black(score)

    if WhiteKing.alive:
      score += 5
    for i in range(White.num_queens):
      if WhiteQueen.alive[i]:
        score += 9
    for i in range(8):
      if WhitePawn.alive[i]:
        score += 1
        # promote
        if WhitePawn.row[i] == 0:
          score += 10
    for i in range(2):
      if WhiteBishop.alive[i]:
        score += 3
      if WhiteKnight.alive[i]:
        score += 3
      if WhiteRook.alive[i]:
        score += 5
    if White.castled == 1:
      score += 1.0
    score = self.RBQ_openfiles_white(score)
    return float(score)

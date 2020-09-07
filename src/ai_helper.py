from common import *

class Helper(object):

  def shuffle(self, di):
    "Shuffle dict."
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
          score -= 7
    for i in range(2):
      if BlackBishop.alive[i]:
        score -= 3
      if BlackKnight.alive[i]:
        score -= 3
      if BlackRook.alive[i]:
        score -= 5
    if Black.castled == 1:
      score -= 0.5

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
          score += 7
    for i in range(2):
      if WhiteBishop.alive[i]:
        score += 3
      if WhiteKnight.alive[i]:
        score += 3
      if WhiteRook.alive[i]:
        score += 5
    if White.castled == 1:
      score += 0.5
    return float(score)

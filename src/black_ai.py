from common import *

class Black_AI(object):
  def __init__(self):
    self.depth = 2

  def generate_move(self):
    if Black.opening_book and Black.still_opening:
      pass
      # Black_.play_opening()
    move = self.find_best_move().copy()
    if move["piece"] == "K" and move["pos"] == "CK":
      Black_.castle_king(True)
    elif move["piece"] == "K" and move["pos"] == "CQ":
      Black_.castle_queen(True)
    else:
      try:
        Black_.move_piece(move["piece"], move["pos"][0], move["pos"][1], True)
      except:
        print("No move found.") if Black.verbose else None
        return

  def find_best_move(self):
    "Use minimax & alpha-beta pruning to find the best move."
    best_move = {"score": -9999, "piece": "", "pos": ()}
    moves = helper.get_all_black_moves().copy()
    Board.set_freeze()
    for i in moves:
      for k in moves[i]:
        if k == "CK":
          Black_.castle_king(False)
          score = self.minimax(self.depth, -10000, 10000, "W")
          print("Undoing " + i + str(k)) if Black.verbose else None
          Board.undo()
        elif k == "CQ":
          Black_.castle_queen(False)
          score = self.minimax(self.depth, -10000, 10000, "W")
          print("Undoing " + i + str(k)) if Black.verbose else None
          Board.undo()
        else:
          Black_.move_piece(i, k[0], k[1], False)
          score = self.minimax(self.depth, -10000, 10000, "W")
          print("Undoing " + i + str(k)) if Black.verbose else None
          print(i, k, score)
          Board.undo()
        if score >= best_move["score"]:
          best_move["score"] = score
          best_move["piece"] = i
          best_move["pos"] = k
    print("Returned best move %s to %s with score %s"%(best_move["piece"], best_move["pos"],
    best_move["score"])) if Black.verbose else None
    Board.unfreeze()
    return best_move

  def minimax(self, n, alpha, beta, player):
    "Recursively search all valid moves, beginning at depth n."
    black_moves = helper.get_all_black_moves().copy()
    white_moves = helper.get_all_white_moves().copy()
    if n == 0:
      return -helper.evaluate_pos()
    # minimizing player
    if player == "B":
      best_move = -9999
      for i in black_moves:
        for k in black_moves[i]:
          if k == "CK":
            Black_.castle_king(False)
            best_move = max(best_move, self.minimax(n-1, alpha, beta, "W"))
            print("Undoing " + i + str(k)) if Black.verbose else None
            Board.undo()
          elif k == "CQ":
            Black_.castle_queen(False)
            best_move = max(best_move, self.minimax(n-1, alpha, beta, "W"))
            print("Undoing " + i + str(k)) if Black.verbose else None
            Board.undo()
          else:
            Black_.move_piece(i, k[0], k[1], False)
            best_move = max(best_move, self.minimax(n-1, alpha, beta, "W"))
            print("Undoing " + i + str(k)) if Black.verbose else None
            Board.undo()
          alpha = max(alpha, best_move)
          if beta <= alpha:
            return best_move
          elif Board.checkmate:
            if verbose:
              print("Game ended in search...")
            Board.checkmate = False
            Board.stalemate = False
            Board.insufficient_mat = False
            if White.checker == "":
              return 9999
            else:
              return -9999
    # maximizing player
    else:
      best_move = 9999
      for i in white_moves:
        for k in white_moves[i]:
          if k == "CK":
            White_.castle_king(False)
            best_move = min(best_move, self.minimax(n-1, alpha, beta, "B"))
            print("Undoing " + i + str(k)) if Black.verbose else None
            Board.undo()
          elif k == "CQ":
            White_.castle_queen(False)
            best_move = min(best_move, self.minimax(n-1, alpha, beta, "B"))
            print("Undoing " + i + str(k)) if Black.verbose else None
            Board.undo()
          else:
            White_.move_piece(i, k[0], k[1], False)
            best_move = min(best_move, self.minimax(n-1, alpha, beta, "B"))
            print("Undoing " + i + str(k)) if Black.verbose else None
            Board.undo()
          beta = min(beta, best_move)
          if beta <= alpha:
            return best_move
          elif Board.checkmate or Board.stalemate or Board.insufficient_mat:
            if verbose:
              print("Game ended in search...")
            Board.checkmate = False
            Board.stalemate = False
            Board.insufficient_mat = False
            if White.checker == "":
              return -9999
            else:
              return 9999

    return best_move

from common import *

class Game_Board(object):
  "Class for drawing board elements & controlling game state/pieces."

  def __init__(self):
    self.shadepos = (-1,-1)
    self.piece = ""
    self.black_pieces = ["BlackKing", "BlackQueen", "BlackBishop", "BlackRook",
    "BlackKnight", "BlackPawn"]
    self.white_pieces = ["WhiteKing", "WhiteQueen", "WhiteBishop", "WhiteRook",
    "WhiteKnight", "WhitePawn"]
    self.stalemate = False
    self.tfr = False
    self.insufficient_mat = False
    self.checkmate = False
    # stack for undo
    self.moves = {"color": [], "piece": [], "pos": [], "killed": []}
    self.killed = {"piece": [], "pos": []}
    self.total_moves = 0
    self.freeze = False
    self.save_img = False
    self.num_screenshots = 0

  def capture_image(self):
    pg.image.save(win, "../media/frames/" + str(self.num_screenshots) + ".jpeg")
    self.num_screenshots += 1
    self.save_img = False

  def set_freeze(self):
    self.freeze = True

  def unfreeze(self):
    self.freeze = False

  def draw_board(self):
    counter = 0
    outer = False
    for y in range(OFFSET, RES+OFFSET, UNIT):
      outer = True
      for x in range(0, RES, UNIT):
        if outer:
          counter += 2
        else:
          counter += 1
        outer = False
        if counter%2 != 0:
          pg.draw.rect(win, (200,200,200), (x, y, UNIT, UNIT))
        elif counter%2 == 0:
          pg.draw.rect(win, (82, 134, 217), (x, y, UNIT, UNIT))

  def shade(self, row, col):
    """Outline square with coordinates (row,col) to
    show a piece that will be moved.
    """
    x = col*UNIT
    y = row*UNIT
    shadeColor = (240, 203, 93)
    pg.draw.rect(win, shadeColor, (x, y, UNIT,UNIT))

  def get_col(self, x):
    "Get column value from x value."
    return x//UNIT

  def get_row(self, y):
    "Get row value from y value."
    return y//UNIT

  def show_black(self):
    for i in self.black_pieces:
      eval(i).show()

  def show_white(self):
    for i in self.white_pieces:
      eval(i).show()

  def update_all_moves(self):
    """Every time a piece moves, the movelist of all other pieces should be updated.
    Note that the piece movelists other than the king should be updated first, since the
    king's movelist is calculated based off of those.
    """
    white_minus_king = [i for i in self.white_pieces if i != "WhiteKing"]
    black_minus_king = [i for i in self.black_pieces if i != "BlackKing"]
    for i in white_minus_king:
      eval(i).update_movelist()
    for i in black_minus_king:
      eval(i).update_movelist()

    WhiteKing.update_movelist()
    BlackKing.update_movelist()

  def check_insuffience_mat(self):
    """A draw by insufficient material occurs if both sides have any of:
    - A lone king
    - A king and bishop
    - A king and knight
    - A king and 2 knights
    and no pawns.
    """
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    if (Black_.lone_king() or Black_.one_bishop() or Black_.two_knights() or \
    Black_.one_knight()) and (White_.lone_king() or White_.one_bishop() or \
    White_.two_knights() or White_.one_knight()):
      return True
    return False

  def check_tfr(self):
    """A draw by 3-fold repetition occurs if the same position occurs in 3 consecutive
    turns.
    """
    pass

  def check_end(self):
    "If game has ended, show a status message (checkmate, draw, stalemate)."
    color = (19, 81, 168)
    if self.insufficient_mat:
      win.blit(font.render('Draw by insufficient', False, color),
      (15,(RES//2)-(RES//8)))
      win.blit(font.render('material', False, color),
      (15,(RES//2)-(RES//40)))
    elif self.stalemate:
      win.blit(font.render('Stalemate', False, color), (RES//4, RES//2))
    elif self.checkmate:
      win.blit(font.render('Checkmate', False, color), (RES//4, RES//2))

  def check_draw(self):
    if self.check_insuffience_mat():
      self.insufficient_mat = True
    elif self.check_tfr():
      self.tfr = True

  def undo(self):
    "Undo the last move played. Used for AI move generation in tree traversal."
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    if len(self.moves["piece"]) == 0:
      print("Nothing to undo!")
      return
    if (Black.ai or White.ai) and self.freeze and len(self.moves["piece"]) <= self.total_moves:
      print("AI undo'ing too far") if verbose else None
      return
    if (self.checkmate or self.stalemate or self.insufficient_mat) and self.freeze == False:
      self.checkmate = False
      self.stalemate = False
      self.insufficient_mat = False
    (row, col) = (self.moves["pos"][-1][0], self.moves["pos"][-1][1])
    piece = self.moves["piece"][-1]
    # * Black *
    # move back
    if self.moves["color"][-1] == "B":
      if piece == "K":
        BlackKing.Move(row, col)
      elif piece == "CK":
        BlackKing.Move(0, 4)
        BlackRook.Move(1, 0, 7)
        Black.castled = 0
        BlackRook.moved[1] = 0
        BlackKing.moved = 0
      elif piece == "CQ":
        BlackKing.Move(0, 4)
        BlackRook.Move(0, 0, 0)
        Black.castled = 0
        BlackRook.moved[0] = 0
        BlackKing.moved = 0
      for i in range(Black.num_queens):
        if piece == "Q" + str(i):
          BlackQueen.Move(i, row, col)
      for i in range(8):
        if piece == "P" + str(i):
          if row == 6:
            # use black queen pos since it was promoted to q
            Black.blocks[BlackQueen.row[-1]][BlackQueen.col[-1]] = 0
            Black_.unpromote(i, row, col)
          else:
            BlackPawn.Move(i, row, col)
      for i in range(2):
        if piece == "B" + str(i):
          BlackBishop.Move(i, row, col)
        elif piece == "R" + str(i):
          BlackRook.Move(i, row, col)
        elif piece == "N" + str(i):
          BlackKnight.Move(i, row, col)
      # revive if piece killed
      if self.moves["killed"][-1] == True:
        if self.killed["piece"][-1] == "K":
          WhiteKing.alive = 1
          WhiteKing.Move(self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        for i in range(White.num_queens):
          if self.killed["piece"][-1] == "Q" + str(i):
            WhiteQueen.alive[i] = 1
            WhiteQueen.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        for i in range(8):
          if self.killed["piece"][-1] == "P" + str(i):
            WhitePawn.alive[i] = 1
            WhitePawn.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        for i in range(2):
          if self.killed["piece"][-1] == "B" + str(i):
            WhiteBishop.alive[i] = 1
            WhiteBishop.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
          elif self.killed["piece"][-1] == "N" + str(i):
            WhiteKnight.alive[i] = 1
            WhiteKnight.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
          elif self.killed["piece"][-1] == "R" + str(i):
            WhiteRook.alive[i] = 1
            WhiteRook.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        self.killed["piece"].pop(-1)
        self.killed["pos"].pop(-1)
      self.update_all_moves()
      Black_.check_white_pin()
      if Black_.check_white_check():
        White_.update_check_movelists()
      Black_.reset_enpassant()
      self.moves["color"].pop(-1)
      self.moves["piece"].pop(-1)
      self.moves["pos"].pop(-1)
      self.moves["killed"].pop(-1)

    # * White *
    # move back
    elif self.moves["color"][-1] == "W":
      if piece == "K":
        WhiteKing.Move(row, col)
      elif piece == "CK":
        WhiteKing.Move(7, 4)
        WhiteRook.Move(1, 7, 7)
        White.castled = 0
        WhiteRook.moved[1] = 0
        WhiteKing.moved = 0
      elif piece == "CQ":
        WhiteKing.Move(7, 4)
        WhiteRook.Move(0, 7, 0)
        White.castled = 0
        WhiteRook.moved[0] = 0
        WhiteKing.moved = 0
      for i in range(White.num_queens):
        if piece == "Q" + str(i):
          WhiteQueen.Move(i, row, col)
      for i in range(8):
        if piece == "P" + str(i):
          if row == 1:
            # use white queen pos since it was promoted to q
            White.blocks[WhiteQueen.row[-1]][WhiteQueen.col[-1]] = 0
            White_.unpromote(i, row, col)
          else:
            WhitePawn.Move(i, row, col)
      for i in range(2):
        if piece == "B" + str(i):
          WhiteBishop.Move(i, row, col)
        elif piece == "R" + str(i):
          WhiteRook.Move(i, row, col)
        elif piece == "N" + str(i):
          WhiteKnight.Move(i, row, col)
      # revive if piece killed
      if self.moves["killed"][-1] == True:
        if self.killed["piece"][-1] == "K":
          BlackKing.alive = 1
          BlackKing.Move(self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        for i in range(Black.num_queens):
          if self.killed["piece"][-1] == "Q" + str(i):
            BlackQueen.alive[i] = 1
            BlackQueen.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        for i in range(8):
          if self.killed["piece"][-1] == "P" + str(i):
            BlackPawn.alive[i] = 1
            BlackPawn.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        for i in range(2):
          if self.killed["piece"][-1] == "B" + str(i):
            BlackBishop.alive[i] = 1
            BlackBishop.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
          elif self.killed["piece"][-1] == "N" + str(i):
            BlackKnight.alive[i] = 1
            BlackKnight.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
          elif self.killed["piece"][-1] == "R" + str(i):
            BlackRook.alive[i] = 1
            BlackRook.Move(i, self.killed["pos"][-1][0], self.killed["pos"][-1][1])
        self.killed["piece"].pop(-1)
        self.killed["pos"].pop(-1)
      self.update_all_moves()
      White_.check_black_pin()
      if White_.check_black_check():
        Black_.update_check_movelists()
      White_.reset_enpassant()
      self.moves["color"].pop(-1)
      self.moves["piece"].pop(-1)
      self.moves["pos"].pop(-1)
      self.moves["killed"].pop(-1)
    if not self.freeze:
      self.total_moves -= 1

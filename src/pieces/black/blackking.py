from common import *

class Black_King(object):
  def __init__(self):
    self.img = pg.image.load('../assets/sprites/blackKing.png')
    self.img = pg.transform.scale(self.img, (Piece.scale, Piece.scale))
    self.col = 4
    self.row = 0
    self.x = Piece.paddingx + self.col*UNIT
    self.y = Piece.paddingy + self.row*UNIT
    self.movelist = []
    self.alive = 1
    self.moved = False

  def show(self):
    if self.alive == 1:
      win.blit(self.img,(self.x, self.y))

  def Move(self, row, col):
    "Move king to coordinates (row, col)."
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    if (self.row, self.col) != (-1, -1):
      Black.blocks[self.row][self.col] = 0
    Black.blocks[row][col] = 1
    self.col = col
    self.row = row
    self.x = Piece.paddingx + col*UNIT
    self.y = Piece.paddingy + row*UNIT
    if Black_.get_freeze() == False:
      self.moved = 1

  def update_movelist(self):
    self.movelist.clear()
    if self.alive == 0:
      return
    # sides
    if self.row + 1 <= 7:
      if Black.blocks[self.row+1][self.col] == 0:
        self.movelist.append((self.row+1, self.col))
    if self.row - 1 >= 0:
      if Black.blocks[self.row-1][self.col] == 0:
        self.movelist.append((self.row-1, self.col))
    if self.col + 1 <= 7:
      if Black.blocks[self.row][self.col+1] == 0:
        self.movelist.append((self.row, self.col+1))
    if self.col - 1 >= 0:
      if Black.blocks[self.row][self.col-1] == 0:
        self.movelist.append((self.row, self.col-1))
    # diagonals
    if self.row - 1 >= 0 and self.col + 1 <= 7:
      if Black.blocks[self.row-1][self.col+1] == 0:
        self.movelist.append((self.row-1, self.col+1))
    if self.row - 1 >= 0 and self.col - 1 >= 0:
      if Black.blocks[self.row-1][self.col-1] == 0:
        self.movelist.append((self.row-1, self.col-1))
    if self.row + 1 <= 7 and self.col - 1 >= 0:
      if Black.blocks[self.row+1][self.col-1] == 0:
        self.movelist.append((self.row+1, self.col-1))
    if self.row + 1 <= 7 and self.col + 1 <= 7:
      if Black.blocks[self.row+1][self.col+1] == 0:
        self.movelist.append((self.row+1, self.col+1))
    self.filter_check_positions()
    self.filter_king_positions()

  def filter_check_positions(self):
    """The black king cannot move to a position where it would be checked (i.e positions
    in white piece's movelists).
    Remove these positions from its movelist.
    """
    for i in range(White.num_queens):
      for k in WhiteQueen.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in WhiteQueen.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
    for i in range(2):
      for k in WhiteBishop.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in WhiteBishop.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in WhiteRook.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in WhiteRook.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in WhiteKnight.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in WhiteKnight.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
    for i in range(8):
      for k in WhitePawn.hit_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)

  def filter_king_positions(self):
    "Kings can never be next to each other."
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    whiteking_row = White_.get_pos("K")[0]
    whiteking_col = White_.get_pos("K")[1]
    avoid_moves = [(whiteking_row-1, whiteking_col-1), (whiteking_row-1, whiteking_col),
    (whiteking_row-1, whiteking_col+1), (whiteking_row, whiteking_col-1),
    (whiteking_row, whiteking_col+1), (whiteking_row+1, whiteking_col-1),
    (whiteking_row+1, whiteking_col), (whiteking_row+1, whiteking_col+1)]
    for i in avoid_moves:
      if i in self.movelist:
        self.movelist.remove(i)

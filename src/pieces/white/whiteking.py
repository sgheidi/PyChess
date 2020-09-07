from common import *

class White_King(object):
  def __init__(self):
    self.img = pg.image.load('../assets/sprites/whiteKing.png')
    self.img = pg.transform.scale(self.img, (Piece.scale, Piece.scale))
    self.col = 4
    self.row = 7
    self.x = Piece.paddingx + self.col*UNIT
    self.y = Piece.paddingy + self.row*UNIT
    self.movelist = []
    self.protecting_movelist = []
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
      White.blocks[self.row][self.col] = 0
    White.blocks[row][col] = 1
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
      if White.blocks[self.row+1][self.col] == 0:
        self.movelist.append((self.row+1, self.col))
      elif White.blocks[self.row+1][self.col] == 1:
        self.protecting_movelist.append((self.row+1, self.col))
    if self.row - 1 >= 0:
      if White.blocks[self.row-1][self.col] == 0:
        self.movelist.append((self.row-1, self.col))
      elif White.blocks[self.row-1][self.col] == 1:
        self.protecting_movelist.append((self.row-1, self.col))
    if self.col + 1 <= 7:
      if White.blocks[self.row][self.col+1] == 0:
        self.movelist.append((self.row, self.col+1))
      elif White.blocks[self.row][self.col+1] == 1:
        self.protecting_movelist.append((self.row, self.col+1))
    if self.col - 1 >= 0:
      if White.blocks[self.row][self.col-1] == 0:
        self.movelist.append((self.row, self.col-1))
      if White.blocks[self.row][self.col-1] == 1:
        self.protecting_movelist.append((self.row, self.col-1))
    # diagonals
    if self.row - 1 >= 0 and self.col + 1 <= 7:
      if White.blocks[self.row-1][self.col+1] == 0:
        self.movelist.append((self.row-1, self.col+1))
      elif White.blocks[self.row-1][self.col+1] == 1:
        self.protecting_movelist.append((self.row-1, self.col+1))
    if self.row - 1 >= 0 and self.col - 1 >= 0:
      if White.blocks[self.row-1][self.col-1] == 0:
        self.movelist.append((self.row-1, self.col-1))
      elif White.blocks[self.row-1][self.col-1] == 1:
        self.protecting_movelist.append((self.row-1, self.col-1))
    if self.row + 1 <= 7 and self.col - 1 >= 0:
      if White.blocks[self.row+1][self.col-1] == 0:
        self.movelist.append((self.row+1, self.col-1))
      elif White.blocks[self.row+1][self.col-1] == 1:
        self.protecting_movelist.append((self.row+1, self.col-1))
    if self.row + 1 <= 7 and self.col + 1 <= 7:
      if White.blocks[self.row+1][self.col+1] == 0:
        self.movelist.append((self.row+1, self.col+1))
      elif White.blocks[self.row+1][self.col+1] == 1:
        self.protecting_movelist.append((self.row+1, self.col+1))
    self.filter_check_positions()
    self.filter_king_positions()

  def filter_check_positions(self):
    """The white king cannot move to a position where it would be checked (i.e positions
    in black piece's movelists).
    Remove these positions from its movelist.
    """
    for i in range(Black.num_queens):
      for k in BlackQueen.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in BlackQueen.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
    for i in range(2):
      for k in BlackBishop.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in BlackBishop.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in BlackRook.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in BlackRook.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in BlackKnight.movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
      for k in BlackKnight.protecting_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)
    for i in range(8):
      for k in BlackPawn.hit_movelist[i]:
        if k in self.movelist:
          self.movelist.remove(k)

  def filter_king_positions(self):
    "Kings can never be next to each other."
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    blackking_row = Black_.get_pos("K")[0]
    blackking_col = Black_.get_pos("K")[1]
    avoid_moves = [(blackking_row-1, blackking_col-1), (blackking_row-1, blackking_col),
    (blackking_row-1, blackking_col+1), (blackking_row, blackking_col-1),
    (blackking_row, blackking_col+1), (blackking_row+1, blackking_col-1),
    (blackking_row+1, blackking_col), (blackking_row+1, blackking_col+1)]
    for i in avoid_moves:
      if i in self.movelist:
        self.movelist.remove(i)

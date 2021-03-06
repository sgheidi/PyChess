from common import *

class Black_Bishop(object):
  def __init__(self):
    self.img = [pg.image.load('../assets/sprites/blackBishop.png') for x in range(2)]
    self.img = [pg.transform.scale(self.img[x], (Piece.scale, Piece.scale)) for x in range(2)]
    self.col = [2, 5]
    self.row = [0, 0]
    self.x = [Piece.paddingx + self.col[0]*UNIT, Piece.paddingx + self.col[1]*UNIT]
    self.y = [Piece.paddingy + self.row[0]*UNIT, Piece.paddingy + self.row[1]*UNIT]
    self.movelist = [[], []]
    self.protecting_movelist = [[], []]
    self.pinned_movelist = [[], []]
    self.alive = [1 for i in range(2)]
    self.in_path = [0 for i in range(2)]
    self.dir = ["UL", "UR", "LR", "LL"]

  def show(self):
    for i in range(2):
      if self.alive[i] == 1:
        win.blit(self.img[i],(self.x[i], self.y[i]))

  def Move(self, i, row, col):
    "Move bishop i to coordinates (row, col)."
    if (self.row[i], self.col[i]) != (-1, -1):
      Black.blocks[self.row[i]][self.col[i]] = 0
    Black.blocks[row][col] = 1
    self.col[i] = col
    self.row[i] = row
    self.x[i] = Piece.paddingx + col*UNIT
    self.y[i] = Piece.paddingy + row*UNIT

  def update_movelist(self):
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()

    for i in range(2):
      self.movelist[i].clear()
      self.protecting_movelist[i].clear()
      if self.alive[i] == 0:
        continue
      row = self.row[i]
      col = self.col[i]
      # diagonal pointing to top-left corner of screen
      while row-1 >= 0 and col-1 >= 0:
        if Black.blocks[row-1][col-1] == 1:
          self.protecting_movelist[i].append((row-1, col-1))
          break
        if White.blocks[row-1][col-1] == 1:
          blackking_pos = White_.get_pos("K")
          if blackking_pos[0] == row-1 and blackking_pos[1] == col-1:
            self.movelist[i].append((row - 1, col - 1))
            self.movelist[i].append((row - 2, col - 2))
            break
          self.movelist[i].append((row - 1, col - 1))
          break
        row -= 1
        col -= 1
        self.movelist[i].append((row, col))
      row = self.row[i]
      col = self.col[i]
      # diagonal to top-right corner of screen
      while row-1 >= 0 and col+1 <= 7:
        if Black.blocks[row-1][col+1] == 1:
          self.protecting_movelist[i].append((row-1, col+1))
          break
        if White.blocks[row-1][col+1] == 1:
          blackking_pos = White_.get_pos("K")
          if blackking_pos[0] == row-1 and blackking_pos[1] == col+1:
            self.movelist[i].append((row - 1, col + 1))
            self.movelist[i].append((row - 2, col + 2))
            break
          self.movelist[i].append((row - 1, col + 1))
          break
        row -= 1
        col += 1
        self.movelist[i].append((row, col))
      row = self.row[i]
      col = self.col[i]
      # diagonal to bottom-right corner of screen
      while row+1 <= 7 and col+1 <= 7:
        if Black.blocks[row+1][col+1] == 1:
          self.protecting_movelist[i].append((row+1, col+1))
          break
        if White.blocks[row+1][col+1] == 1:
          blackking_pos = White_.get_pos("K")
          if blackking_pos[0] == row+1 and blackking_pos[1] == col+1:
            self.movelist[i].append((row + 1, col + 1))
            self.movelist[i].append((row + 2, col + 2))
            break
          self.movelist[i].append((row + 1, col + 1))
          break
        row += 1
        col += 1
        self.movelist[i].append((row, col))
      row = self.row[i]
      col = self.col[i]
      # diagonal to bottom-left corner of screen
      while row+1 <= 7 and col-1 >= 0:
        if Black.blocks[row+1][col-1] == 1:
          self.protecting_movelist[i].append((row+1, col-1))
          break
        if White.blocks[row+1][col-1] == 1:
          blackking_pos = White_.get_pos("K")
          if blackking_pos[0] == row+1 and blackking_pos[1] == col-1:
            self.movelist[i].append((row + 1, col - 1))
            self.movelist[i].append((row + 2, col - 2))
            break
          self.movelist[i].append((row + 1, col - 1))
          break
        row += 1
        col -= 1
        self.movelist[i].append((row, col))

  def king_in_path(self):
    """Determine if king is in path of bishop. Used for pinning.
    Returns "UL", "UR", "LL", "LR" for where the king's position is relative
    to the bishop (upper left, upper right, lower left, lower right).
    Also sets the in_path flag for the bishop to 1.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.alive[i] == 0:
        continue
      self.in_path[i] = 0
      row = self.row[i]
      col = self.col[i]
      while row >= 0 and col >= 0:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = 1
          return "UL"
        row -= 1
        col -= 1
      row = self.row[i]
      col = self.col[i]
      while row >= 0 and col <= 7:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = 1
          return "UR"
        row -= 1
        col += 1
      row = self.row[i]
      col = self.col[i]
      while row <= 7 and col <= 7:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = 1
          return "LR"
        row += 1
        col += 1
      row = self.row[i]
      col = self.col[i]
      while row <= 7 and col >= 0:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = 1
          return "LL"
        row += 1
        col -= 1

  def num_pieces(self, dir):
    """Determine the number of white pieces between bishop and white
    king in direction dir.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      if dir == "UL":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while row >= 0 and col >= 0:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row -= 1
          col -= 1
          num_blocks += 1
      elif dir == "UR":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while row >= 0 and col <= 7:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row -= 1
          col += 1
          num_blocks += 1
      elif dir == "LR":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while row <= 7 and col <= 7:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row += 1
          col += 1
          num_blocks += 1
      elif dir == "LL":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while row <= 7 and col >= 0:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row += 1
          col -= 1
          num_blocks += 1

  def get_pinned_piece(self, dir):
    "A piece has been pinned in direction dir. Get that piece."
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      if dir == "UL":
        row = self.row[i]
        col = self.col[i]
        while row >= 0 and col >= 0:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          row -= 1
          col -= 1
      elif dir == "UR":
        row = self.row[i]
        col = self.col[i]
        while row >= 0 and col <= 7:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          row -= 1
          col += 1
      elif dir == "LR":
        row = self.row[i]
        col = self.col[i]
        while row <= 7 and col <= 7:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          row += 1
          col += 1
      elif dir == "LL":
        row = self.row[i]
        col = self.col[i]
        while row <= 7 and col >= 0:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          row += 1
          col -= 1

  def pin_piece(self, pinned_piece, dir):
    """A white piece is pinned between bishop and king in direction dir.
    Pin that piece by filtering any moves that are not in the bishop's pinned_movelist.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      self.pinned_movelist[i].clear()
      if dir == "UL":
        row = self.row[i]
        col = self.col[i]
        while row >= 0 and col >= 0:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row -= 1
          col -= 1
      elif dir == "UR":
        row = self.row[i]
        col = self.col[i]
        while row >= 0 and col <= 7:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row -= 1
          col += 1
      elif dir == "LR":
        row = self.row[i]
        col = self.col[i]
        while row <= 7 and col <= 7:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row += 1
          col += 1
      elif dir == "LL":
        row = self.row[i]
        col = self.col[i]
        while row <= 7 and col >= 0:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row += 1
          col -= 1

  def check_pin(self):
    """Core function for pinning.
    Check if any white piece is pinned. If it is, pin that piece.
    """
    for i in self.dir:
      if self.king_in_path() == i and self.num_pieces(i) == 1:
        pinned_piece = self.get_pinned_piece(i)
        self.pin_piece(pinned_piece, i)

  def build_check_movelist(self):
    """White king has been checked by a bishop. Build and return a movelist going
    in the direction of the white king.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    white_king_row = White_.get_pos("K")[0]
    white_king_col = White_.get_pos("K")[1]
    movelist = []
    for i in range(2):
      if Black.checker != "B" + str(i):
        continue
      row = self.row[i]
      col = self.col[i]
      # king in lower right (relative to bishop)
      if white_king_row > self.row[i] and white_king_col > self.col[i]:
        while row <= 7 and col <= 7:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row += 1
          col += 1
      # lower left
      elif white_king_row > self.row[i] and white_king_col < self.col[i]:
        while row <= 7 and col >= 0:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row += 1
          col -= 1
      # upper left
      elif white_king_row < self.row[i] and white_king_col < self.col[i]:
        while row >= 0 and col >= 0:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row -= 1
          col -= 1
      # upper right
      elif white_king_row < self.row[i] and white_king_col > self.col[i]:
        while row >= 0 and col <= 7:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row -= 1
          col += 1

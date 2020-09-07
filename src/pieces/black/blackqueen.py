from common import *

class Black_Queen(object):
  def __init__(self):
    self.img = [pg.image.load('../assets/sprites/blackQueen.png') for i in
    range(Black.num_queens)]
    self.img = [pg.transform.scale(self.img[x], (Piece.scale, Piece.scale)) for x in
    range(Black.num_queens)]
    self.col = [3]
    self.row = [0]
    self.x = [Piece.paddingx + self.col[0]*UNIT]
    self.y = [Piece.paddingy + self.row[0]*UNIT]
    self.movelist = [[]]
    self.protecting_movelist = [[]]
    self.pinned_movelist = [[]]
    self.alive = [1 for i in range(Black.num_queens)]
    self.in_path = [0 for i in range(Black.num_queens)]
    self.dir = ["L", "R", "U", "D", "UL", "UR", "LR", "LL"]

  def show(self):
    for i in range(Black.num_queens):
      if self.alive[i] == 1:
        win.blit(self.img[i],(self.x[i], self.y[i]))

  def Move(self, i, row, col):
    "Move queen to coordinates (row, col)."
    if (self.row[i], self.col[i]) != (-1, -1):
      Black.blocks[self.row[i]][self.col[i]] = 0
    Black.blocks[row][col] = 1
    self.col[i] = col
    self.row[i] = row
    self.x[i] = Piece.paddingx + col*UNIT
    self.y[i] = Piece.paddingy + row*UNIT

  def update_movelist(self):
    "Queen movelist is the sum of Bishop and Rook moves."
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(Black.num_queens):
      if self.alive[i] == 0:
        continue
      # Rook part
      self.movelist[i].clear()
      self.protecting_movelist[i].clear()
      row = self.row[i]
      col = self.col[i]
      while row-1 >= 0:
        if Black.blocks[row-1][col] == 1:
          self.protecting_movelist[i].append((row-1, col))
          break
        if White.blocks[row-1][col] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row-1 and whiteking_pos[1] == col:
            self.movelist[i].append((row - 1, col))
            self.movelist[i].append((row - 2, col))
            break
          self.movelist[i].append((row - 1, col))
          break
        row -= 1
        self.movelist[i].append((row, col))
      row = self.row[i]
      while row+1 <= 7:
        if Black.blocks[row+1][col] == 1:
          self.protecting_movelist[i].append((row+1, col))
          break
        if White.blocks[row+1][col] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row+1 and whiteking_pos[1] == col:
            self.movelist[i].append((row + 1, col))
            self.movelist[i].append((row + 2, col))
            break
          self.movelist[i].append((row + 1, col))
          break
        row += 1
        self.movelist[i].append((row, col))
      row = self.row[i]
      while col-1 >= 0:
        if Black.blocks[row][col-1] == 1:
          self.protecting_movelist[i].append((row, col-1))
          break
        if White.blocks[row][col-1] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row and whiteking_pos[1] == col-1:
            self.movelist[i].append((row, col - 1))
            self.movelist[i].append((row, col - 2))
            break
          self.movelist[i].append((row, col - 1))
          break
        col -= 1
        self.movelist[i].append((row, col))
      col = self.col[i]
      while col+1 <= 7:
        if Black.blocks[row][col+1] == 1:
          self.protecting_movelist[i].append((row, col+1))
          break
        if White.blocks[row][col+1] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row and whiteking_pos[1] == col+1:
            self.movelist[i].append((row, col + 1))
            self.movelist[i].append((row, col + 2))
            break
          self.movelist[i].append((row, col + 1))
          break
        col += 1
        self.movelist[i].append((row, col))
      # Bishop part
      row = self.row[i]
      col = self.col[i]
      while row-1 >= 0 and col-1 >= 0:
        if Black.blocks[row-1][col-1] == 1:
          self.protecting_movelist[i].append((row-1, col-1))
          break
        if White.blocks[row-1][col-1] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row-1 and whiteking_pos[1] == col-1:
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
      while row-1 >= 0 and col+1 <= 7:
        if Black.blocks[row-1][col+1] == 1:
          self.protecting_movelist[i].append((row-1, col+1))
          break
        if White.blocks[row-1][col+1] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row-1 and whiteking_pos[1] == col+1:
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
      while row+1 <= 7 and col+1 <= 7:
        if Black.blocks[row+1][col+1] == 1:
          self.protecting_movelist[i].append((row+1, col+1))
          break
        if White.blocks[row+1][col+1] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row+1 and whiteking_pos[1] == col+1:
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
      while row+1 <= 7 and col-1 >= 0:
        if Black.blocks[row+1][col-1] == 1:
          self.protecting_movelist[i].append((row+1, col-1))
          break
        if White.blocks[row+1][col-1] == 1:
          whiteking_pos = White_.get_pos("K")
          if whiteking_pos[0] == row+1 and whiteking_pos[1] == col-1:
            self.movelist[i].append((row + 1, col - 1))
            self.movelist[i].append((row + 2, col - 2))
            break
          self.movelist[i].append((row + 1, col - 1))
          break
        row += 1
        col -= 1
        self.movelist[i].append((row, col))

  def king_in_path(self):
    """Determine if king is in path of queen. Used for pinning.
    Assigns a list of directions to self.in_path for where the king's
    position is relative to the queen (see self.dir).
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(Black.num_queens):
      if self.alive[i] == 0:
        continue
      self.in_path[i] = 0
      col = self.col[i]
      row = self.row[i]
      # Rook part
      while col >= 0:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "L"
        col -= 1
      col = self.col[i]
      row = self.row[i]
      while col <= 7:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "R"
        col += 1
      col = self.col[i]
      row = self.row[i]
      while row >= 0:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "U"
        row -= 1
      col = self.col[i]
      row = self.row[i]
      while row <= 7:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "D"
        row += 1
      # Bishop part
      row = self.row[i]
      col = self.col[i]
      while row >= 0 and col >= 0:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "UL"
        row -= 1
        col -= 1
      row = self.row[i]
      col = self.col[i]
      while row >= 0 and col <= 7:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "UR"
        row -= 1
        col += 1
      row = self.row[i]
      col = self.col[i]
      while row <= 7 and col <= 7:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "LR"
        row += 1
        col += 1
      row = self.row[i]
      col = self.col[i]
      while row <= 7 and col >= 0:
        if (row, col) ==  White_.get_pos("K"):
          self.in_path[i] = "LL"
        row += 1
        col -= 1

  def num_pieces(self, dir):
    """Determine the number of white pieces between queen and black
    king in direction dir.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(Black.num_queens):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      # Rook part
      if dir == "L":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while col >= 0:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          col -= 1
          num_blocks += 1
      elif dir == "R":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while col <= 7:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          col += 1
          num_blocks += 1
      elif dir == "U":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while row >= 0:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row -= 1
          num_blocks += 1
      elif dir == "D":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        while row <= 7:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            return -1
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row += 1
          num_blocks += 1
      # Bishop part
      elif dir == "UL":
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
    """A piece has been pinned in direction dir. Get that piece."""
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(Black.num_queens):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      # Rook part
      if dir == "L":
        row = self.row[i]
        col = self.col[i]
        while col >= 0:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          col -= 1
      elif dir == "R":
        row = self.row[i]
        col = self.col[i]
        while col <= 7:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          col += 1
      elif dir == "U":
        row = self.row[i]
        col = self.col[i]
        while row >= 0:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          row -= 1
      elif dir == "D":
        row = self.row[i]
        col = self.col[i]
        while row <= 7:
          if White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            return White_.get_piece(row, col)
          row += 1
      # Bishop part
      elif dir == "UL":
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
    """A white piece is pinned between queen and king in direction dir.
    Pin that piece by filtering any moves that are not in the queen's pinned_movelist.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(Black.num_queens):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      self.pinned_movelist[i].clear()
      # Rook part
      if dir == "L":
        row = self.row[i]
        col = self.col[i]
        while col >= 0:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          col -= 1
      elif dir == "R":
        row = self.row[i]
        col = self.col[i]
        while col <= 7:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          col += 1
      elif dir == "U":
        row = self.row[i]
        col = self.col[i]
        while row >= 0:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row -= 1
      elif dir == "D":
        row = self.row[i]
        col = self.col[i]
        while row <= 7:
          if (row, col) == White_.get_pos("K"):
            White_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row += 1
      # Bishop part
      elif dir == "UL":
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
    Check if any black piece is pinned. If it is, pin that piece.
    """
    self.king_in_path()
    for i in range(Black.num_queens):
      if self.in_path[i] != 0 and self.num_pieces(self.in_path[i]) == 1:
        pinned_piece = self.get_pinned_piece(self.in_path[i])
        self.pin_piece(pinned_piece, self.in_path[i])

  def build_check_movelist(self):
    """White king has been checked by queen. Build and return a movelist going
    in the direction of the white king.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    white_king_row = White_.get_pos("K")[0]
    white_king_col = White_.get_pos("K")[1]
    movelist = []
    for i in range(Black.num_queens):
      if Black.checker != "Q" + str(i):
        continue
      row = self.row[i]
      col = self.col[i]
      # * rook part *
      # king is above queen
      if white_king_row < self.row[i] and white_king_col == self.col[i]:
        while row >= 0:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row -= 1
      # below
      elif white_king_row > self.row[i] and white_king_col == self.col[i]:
        while row <= 7:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row += 1
      # left
      elif white_king_col < self.col[i] and white_king_row == self.row[i]:
        while col >= 0:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          col -= 1
      # right
      elif white_king_col > self.col[i] and white_king_row == self.row[i]:
        while col <= 7:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          col += 1
      # * bishop part *
      # lower right
      elif white_king_row > self.row[i] and white_king_col > self.col[i]:
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

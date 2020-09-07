from common import *

class Black_Rook(object):
  def __init__(self):
    self.img = [pg.image.load('../assets/sprites/blackRook.png') for x in range(2)]
    self.img = [pg.transform.scale(self.img[x], (Piece.scale, Piece.scale)) for x in range(2)]
    self.col = [0, 7]
    self.row = [0, 0]
    self.x = [Piece.paddingx + self.col[0]*UNIT, Piece.paddingx + self.col[1]*UNIT]
    self.y = [Piece.paddingy + self.row[0]*UNIT, Piece.paddingy + self.row[1]*UNIT]
    self.movelist = [[], []]
    self.protecting_movelist = [[], []]
    self.pinned_movelist = [[], []]
    self.alive = [1 for i in range(2)]
    self.in_path = [0 for i in range(2)]
    self.dir = ["L", "R", "U", "D"]
    self.moved = [0 for i in range(2)]

  def show(self):
    for i in range(2):
      if self.alive[i] == 1:
        win.blit(self.img[i],(self.x[i], self.y[i]))

  def Move(self, i, row, col):
    "Move rook i to coordinates (row, col)."
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    if (self.row[i], self.col[i]) != (-1, -1):
      Black.blocks[self.row[i]][self.col[i]] = 0
    Black.blocks[row][col] = 1
    self.col[i] = col
    self.row[i] = row
    self.x[i] = Piece.paddingx + col*UNIT
    self.y[i] = Piece.paddingy + row*UNIT
    if Black_.get_freeze() == False:
      self.moved[i] = 1

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
      # up
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
      # down
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
      # left
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
      # right
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

  def king_in_path(self):
    """Determine if king is in path of rook. Used for pinning.
    Returns "L", "R", "U", "D" for where the king's position is relative
    to the rook (left, right, up, down).
    Also sets the in_path flag for the rook to 1.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.alive[i] == 0:
        continue
      self.in_path[i] = 0
      col = self.col[i]
      row = self.row[i]
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

  def num_pieces(self, dir):
    """Determine the number of black pieces between rook and white
    king in direction dir.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      if dir == "L":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        black_found = 0
        while col >= 0:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            black_found = 1
            break
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          col -= 1
          num_blocks += 1
        if black_found:
          continue
      elif dir == "R":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        black_found = 0
        while col <= 7:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            black_found = 1
            break
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          col += 1
          num_blocks += 1
        if black_found:
          continue
      elif dir == "U":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        black_found = 0
        while row >= 0:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            black_found = 1
            break
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row -= 1
          num_blocks += 1
        if black_found:
          continue
      elif dir == "D":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        black_found = 0
        while row <= 7:
          if Black.blocks[row][col] == 1 and num_blocks > 0:
            black_found = 1
            break
          elif White.blocks[row][col] == 1 and (row, col) != White_.get_pos("K"):
            num += 1
          elif (row, col) == White_.get_pos("K"):
            return num
          row += 1
          num_blocks += 1
        if black_found:
          continue

  def get_pinned_piece(self, dir):
    "A piece has been pinned in direction dir. Get that piece."
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
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

  def pin_piece(self, pinned_piece, dir):
    """A white piece is pinned between rook and king in direction dir.
    Pin that piece by filtering any moves that are not in the rook's pinned_movelist.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      self.pinned_movelist[i].clear()
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

  def check_pin(self):
    """Core function for pinning.
    Check if any white piece is pinned. If it is, pin that piece.
    """
    self.king_in_path()
    for i in range(2):
      if self.in_path[i] != 0 and self.num_pieces(self.in_path[i]) == 1:
        pinned_piece = self.get_pinned_piece(self.in_path[i])
        self.pin_piece(pinned_piece, self.in_path[i])

  def build_check_movelist(self):
    """White king has been checked by a rook. Build and return a movelist going
    in the direction of the white king.
    """
    from pieces.white_funcs import White_Funcs
    White_ = White_Funcs()
    white_king_row = White_.get_pos("K")[0]
    white_king_col = White_.get_pos("K")[1]
    movelist = []
    for i in range(2):
      if Black.checker != "R" + str(i):
        continue
      row = self.row[i]
      col = self.col[i]
      # king is above rook
      if white_king_row < self.row[i]:
        while row >= 0:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row -= 1
      # below
      elif white_king_row > self.row[i]:
        while row <= 7:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          row += 1
      # left
      elif white_king_col < self.col[i]:
        while col >= 0:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          col -= 1
      # right
      elif white_king_col > self.col[i]:
        while col <= 7:
          if (row, col) == (white_king_row, white_king_col):
            return movelist
          movelist.append((row, col))
          col += 1

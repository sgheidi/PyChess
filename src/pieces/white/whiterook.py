from common import *

class White_Rook(object):
  def __init__(self):
    self.img = [pg.image.load('../assets/sprites/whiteRook.png') for x in range(2)]
    self.img = [pg.transform.scale(self.img[x], (Piece.scale, Piece.scale)) for x in range(2)]
    self.col = [0, 7]
    self.row = [7, 7]
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
      White.blocks[self.row[i]][self.col[i]] = 0
    White.blocks[row][col] = 1
    self.col[i] = col
    self.row[i] = row
    self.x[i] = Piece.paddingx + col*UNIT
    self.y[i] = Piece.paddingy + row*UNIT
    if Black_.get_freeze() == False:
      self.moved[i] = 1

  def update_movelist(self):
    # We are importing inside this function because we cannot import at the top (since
    # Black_Funcs class does not know about the black pieces at that point yet)
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)

    for i in range(2):
      self.movelist[i].clear()
      self.protecting_movelist[i].clear()
      if self.alive[i] == 0:
        continue
      row = self.row[i]
      col = self.col[i]
      # up
      while row-1 >= 0:
        if White.blocks[row-1][col] == 1:
          self.protecting_movelist[i].append((row-1, col))
          break
        if Black.blocks[row-1][col] == 1:
          blackking_pos = Black_.get_pos("K")
          if blackking_pos[0] == row-1 and blackking_pos[1] == col:
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
        if White.blocks[row+1][col] == 1:
          self.protecting_movelist[i].append((row+1, col))
          break
        if Black.blocks[row+1][col] == 1:
          blackking_pos = Black_.get_pos("K")
          if blackking_pos[0] == row+1 and blackking_pos[1] == col:
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
        if White.blocks[row][col-1] == 1:
          self.protecting_movelist[i].append((row, col-1))
          break
        if Black.blocks[row][col-1] == 1:
          blackking_pos = Black_.get_pos("K")
          if blackking_pos[0] == row and blackking_pos[1] == col-1:
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
        if White.blocks[row][col+1] == 1:
          self.protecting_movelist[i].append((row, col+1))
          break
        if Black.blocks[row][col+1] == 1:
          blackking_pos = Black_.get_pos("K")
          if blackking_pos[0] == row and blackking_pos[1] == col+1:
            self.movelist[i].append((row, col + 1))
            self.movelist[i].append((row, col + 2))
            break
          self.movelist[i].append((row, col + 1))
          break
        col += 1
        self.movelist[i].append((row, col))

  def king_in_path(self):
    """Determine if king is in path of rook. Used for pinning.
    Assigns "L", "R", "U", "D" to Rook's in_path variable for where the
    king's position is relative to the rook (left, right, up, down).
    """
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    for i in range(2):
      if self.alive[i] == 0:
        continue
      self.in_path[i] = 0
      col = self.col[i]
      row = self.row[i]
      while col >= 0:
        if (row, col) ==  Black_.get_pos("K"):
          self.in_path[i] = "L"
        col -= 1
      col = self.col[i]
      row = self.row[i]
      while col <= 7:
        if (row, col) ==  Black_.get_pos("K"):
          self.in_path[i] = "R"
        col += 1
      col = self.col[i]
      row = self.row[i]
      while row >= 0:
        if (row, col) ==  Black_.get_pos("K"):
          self.in_path[i] = "U"
        row -= 1
      col = self.col[i]
      row = self.row[i]
      while row <= 7:
        if (row, col) ==  Black_.get_pos("K"):
          self.in_path[i] = "D"
        row += 1

  def num_pieces(self, dir):
    """Determine the number of black pieces between rook and black
    king in direction dir.
    """
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      if dir == "L":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        white_found = 0
        while col >= 0:
          if White.blocks[row][col] == 1 and num_blocks > 0:
            white_found = 1
            break
          elif Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            num += 1
          elif (row, col) == Black_.get_pos("K"):
            return num
          col -= 1
          num_blocks += 1
        if white_found:
          continue
      elif dir == "R":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        white_found = 0
        while col <= 7:
          if White.blocks[row][col] == 1 and num_blocks > 0:
            white_found = 1
            break
          elif Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            num += 1
          elif (row, col) == Black_.get_pos("K"):
            return num
          col += 1
          num_blocks += 1
        if white_found:
          continue
      elif dir == "U":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        white_found = 0
        while row >= 0:
          if White.blocks[row][col] == 1 and num_blocks > 0:
            white_found = 1
            break
          elif Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            num += 1
          elif (row, col) == Black_.get_pos("K"):
            return num
          row -= 1
          num_blocks += 1
        if white_found:
          continue
      elif dir == "D":
        row = self.row[i]
        col = self.col[i]
        num = 0
        num_blocks = 0
        white_found = 0
        while row <= 7:
          if White.blocks[row][col] == 1 and num_blocks > 0:
            white_found = 1
            break
          elif Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            num += 1
          elif (row, col) == Black_.get_pos("K"):
            return num
          row += 1
          num_blocks += 1
        if white_found:
          continue

  def get_pinned_piece(self, dir):
    """A piece has been pinned in direction dir. Get that piece."""
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      if dir == "L":
        row = self.row[i]
        col = self.col[i]
        while col >= 0:
          if Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            return Black_.get_piece(row, col)
          col -= 1
      elif dir == "R":
        row = self.row[i]
        col = self.col[i]
        while col <= 7:
          if Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            return Black_.get_piece(row, col)
          col += 1
      elif dir == "U":
        row = self.row[i]
        col = self.col[i]
        while row >= 0:
          if Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            return Black_.get_piece(row, col)
          row -= 1
      elif dir == "D":
        row = self.row[i]
        col = self.col[i]
        while row <= 7:
          if Black.blocks[row][col] == 1 and (row, col) != Black_.get_pos("K"):
            return Black_.get_piece(row, col)
          row += 1

  def pin_piece(self, pinned_piece, dir):
    """A black piece is pinned between rook and king in direction dir.
    Pin that piece by filtering any moves that are not in the rook's pinned_movelist.
    """
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    for i in range(2):
      if self.in_path[i] == 0 or self.alive[i] == 0:
        continue
      self.pinned_movelist[i].clear()
      if dir == "L":
        row = self.row[i]
        col = self.col[i]
        while col >= 0:
          if (row, col) == Black_.get_pos("K"):
            Black_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          col -= 1
      elif dir == "R":
        row = self.row[i]
        col = self.col[i]
        while col <= 7:
          if (row, col) == Black_.get_pos("K"):
            Black_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          col += 1
      elif dir == "U":
        row = self.row[i]
        col = self.col[i]
        while row >= 0:
          if (row, col) == Black_.get_pos("K"):
            Black_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row -= 1
      elif dir == "D":
        row = self.row[i]
        col = self.col[i]
        while row <= 7:
          if (row, col) == Black_.get_pos("K"):
            Black_.filter(pinned_piece, self.pinned_movelist[i])
            return
          self.pinned_movelist[i].append((row, col))
          row += 1

  def check_pin(self):
    """Core function for pinning.
    Check if any black piece is pinned. If it is, pin that piece.
    """
    self.king_in_path()
    for i in range(2):
      if self.in_path[i] != 0 and self.num_pieces(self.in_path[i]) == 1:
        pinned_piece = self.get_pinned_piece(self.in_path[i])
        self.pin_piece(pinned_piece, self.in_path[i])

  def build_check_movelist(self):
    """Black king has been checked by a rook. Build and return a movelist going
    in the direction of the black king.
    """
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    black_king_row = Black_.get_pos("K")[0]
    black_king_col = Black_.get_pos("K")[1]
    movelist = []
    for i in range(2):
      if White.checker != "R" + str(i):
        continue
      row = self.row[i]
      col = self.col[i]
      # king is above rook
      if black_king_row < self.row[i]:
        while row >= 0:
          if (row, col) == (black_king_row, black_king_col):
            return movelist
          movelist.append((row, col))
          row -= 1
      # below
      elif black_king_row > self.row[i]:
        while row <= 7:
          if (row, col) == (black_king_row, black_king_col):
            return movelist
          movelist.append((row, col))
          row += 1
      # left
      elif black_king_col < self.col[i]:
        while col >= 0:
          if (row, col) == (black_king_row, black_king_col):
            return movelist
          movelist.append((row, col))
          col -= 1
      # right
      elif black_king_col > self.col[i]:
        while col <= 7:
          if (row, col) == (black_king_row, black_king_col):
            return movelist
          movelist.append((row, col))
          col += 1

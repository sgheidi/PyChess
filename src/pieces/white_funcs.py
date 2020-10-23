from common import *
from pieces.black_funcs import Black_Funcs

class White_Funcs(object):
  "Methods relating to white pieces."

  def __init__(self):
    self.Black_ = Black_Funcs(self)
    self.piece = ""

  def play(self):
    if Board.stalemate or Board.checkmate or Board.insufficient_mat or Board.tfr:
      return
    if White.ai:
      from white_ai import White_AI
      AI = White_AI()
      AI.generate_move()
      Board.save_img = True
      White.turn = False
      Black.turn = True
    else:
      if White.blocks[Queue.row[-1]][Queue.col[-1]] == 1:
        self.piece = self.get_piece(Queue.row[-1], Queue.col[-1])
      # regular move
      if len(Queue.col) >= 2 and White.blocks[Queue.row[0]][Queue.col[0]] == 1 \
      and White.blocks[Queue.row[1]][Queue.col[1]] == 0:
        self.move_piece(self.piece, Queue.row[-1], Queue.col[-1], True)
        Board.ai_move = True
      # queen side castle
      elif len(Queue.col) >= 2 and (Queue.row[0], Queue.col[0]) == (WhiteKing.row, WhiteKing.col) \
      and (Queue.row[1], Queue.col[1]) == (WhiteRook.row[0], WhiteRook.col[0]) and \
      self.castle_criteria_queen():
        self.castle_queen(True)
      # king side castle
      elif len(Queue.col) >= 2 and (Queue.row[0], Queue.col[0]) == (WhiteKing.row, WhiteKing.col) \
      and (Queue.row[1], Queue.col[1]) == (WhiteRook.row[1], WhiteRook.col[1]) and \
      self.castle_criteria_king():
        self.castle_king(True)

  def filter(self, piece, pinned_movelist):
    """Helper function which removes any coordinates in a white piece's movelist
    which is not contained in pinned_movelist. Used to assign pinned movelists to pieces.
    """
    new_movelist = []
    for i in range(White.num_queens):
      if piece == "Q" + str(i):
        for k in WhiteQueen.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        WhiteQueen.movelist[i] = new_movelist.copy()
    for i in range(8):
      new_movelist.clear()
      if piece == "P" + str(i):
        for k in WhitePawn.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        WhitePawn.movelist[i] = new_movelist.copy()
    for i in range(2):
      new_movelist.clear()
      if piece == "R" + str(i):
        for k in WhiteRook.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        WhiteRook.movelist[i] = new_movelist.copy()
      elif piece == "B" + str(i):
        for k in WhiteBishop.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        WhiteBishop.movelist[i] = new_movelist.copy()
      elif piece == "N" + str(i):
        for k in WhiteKnight.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        WhiteKnight.movelist[i] = new_movelist.copy()

  def get_pos(self, piece):
    """Getter for accessing white piece positions.
    Return coordinates of white piece.
    """
    if piece == "K":
      return (WhiteKing.row, WhiteKing.col)
    for i in range(8):
      if piece == "P" + str(i):
        return (WhitePawn.row[i], WhitePawn.col[i])

  def get_movelist(self, piece):
    """Getter for accessing white piece movelist.
    Return movelist of white piece.
    """
    if piece == "K":
      return WhiteKing.movelist
    for i in range(White.num_queens):
      if piece == "Q" + str(i):
        return WhiteQueen.movelist[i]
    for i in range(2):
      if piece == "B" + str(i):
        return WhiteBishop.movelist[i]
      elif piece == "N" + str(i):
        return WhiteKnight.movelist[i]
      elif piece == "R" + str(i):
        return WhiteRook.movelist[i]
    for i in range(8):
      if piece == "P" + str(i):
        return WhitePawn.movelist[i]

  def get_piece(self, row, col):
    "Get piece (as a string) at (row, col)."
    piece = ""
    # King
    if WhiteKing.row == row and WhiteKing.col == col:
      piece = "K"
    # Queen
    for i in range(White.num_queens):
      if WhiteQueen.row[i] == row and WhiteQueen.col[i] == col:
        piece = "Q" + str(i)
    # Bishop, knight, rook
    for i in range(2):
      if WhiteBishop.row[i] == row and WhiteBishop.col[i] == col:
        piece = "B" + str(i)
      if WhiteKnight.row[i] == row and WhiteKnight.col[i] == col:
        piece = "N" + str(i)
      if WhiteRook.row[i] == row and WhiteRook.col[i] == col:
        piece = "R" + str(i)
    # Pawn
    for i in range(8):
      if WhitePawn.row[i] == row and WhitePawn.col[i] == col:
        piece = "P"+str(i)

    return piece if not None else None

  def move_piece(self, piece, row, col, sound):
    "Move piece to position (row, col)."
    moved = False
    killed = False
    self.reset_enpassant()
    if row > 7 or col > 7 or row < 0 or col < 0:
      print("(row, col) bad numbers!")
      return
    # King
    if piece == "K" and (row, col) in WhiteKing.movelist:
      killed = self.check_kill(row, col, sound)
      Board.moves["pos"].append((WhiteKing.row, WhiteKing.col))
      WhiteKing.Move(row, col)
      Board.moves["piece"].append("K")
      moved = True
    elif piece == "K" and (row, col) not in WhiteKing.movelist and sound:
      Sound.error.play()

    # Queen
    for i in range(White.num_queens):
      if piece == "Q" + str(i) and (row, col) in WhiteQueen.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((WhiteQueen.row[i], WhiteQueen.col[i]))
        WhiteQueen.Move(i, row, col)
        Board.moves["piece"].append("Q" + str(i))
        moved = True
      elif piece == "Q" + str(i) and (row, col) not in WhiteQueen.movelist[i] and sound:
        Sound.error.play()

    # Pawn
    for i in range(8):
      if piece == "P" + str(i) and (row, col) in WhitePawn.movelist[i]:
        if Black.en_passant[col] == 1 and WhitePawn.row[i] == 3:
          killed = self.check_kill(row + 1, col, sound)
        else:
          killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((WhitePawn.row[i], WhitePawn.col[i]))
        WhitePawn.Move(i, row, col)
        Board.moves["piece"].append("P" + str(i))
        moved = True
        if row == 0:
          self.promote(i)
      elif piece == "P" + str(i) and (row, col) not in WhitePawn.movelist[i] and sound:
        Sound.error.play()

    # Knight, bishop, rook
    for i in range(2):
      if piece == "N" + str(i) and (row, col) in WhiteKnight.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((WhiteKnight.row[i], WhiteKnight.col[i]))
        WhiteKnight.Move(i, row, col)
        Board.moves["piece"].append("N" + str(i))
        moved = True
      elif piece == "N" + str(i) and (row, col) not in WhiteKnight.movelist[i] and sound:
        Sound.error.play()
      if piece == "B" + str(i) and (row, col) in WhiteBishop.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((WhiteBishop.row[i], WhiteBishop.col[i]))
        WhiteBishop.Move(i, row, col)
        Board.moves["piece"].append("B" + str(i))
        moved = True
      elif piece == "B" + str(i) and (row, col) not in WhiteBishop.movelist[i] and sound:
        Sound.error.play()
      if piece == "R" + str(i) and (row, col) in WhiteRook.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((WhiteRook.row[i], WhiteRook.col[i]))
        WhiteRook.Move(i, row, col)
        Board.moves["piece"].append("R" + str(i))
        moved = True
      elif piece == "R" + str(i) and (row, col) not in WhiteRook.movelist[i] and sound:
        Sound.error.play()

    if moved:
      self.valid_move(killed, sound)

  def valid_move(self, killed, sound):
    """A valid move has been made. Update the board, check for pins,
    checkmate, stalemate,...etc.
    """
    Board.update_all_moves()
    self.check_black_pin()
    # check if black has been checked
    if self.check_black_check():
      if sound:
        Sound.check.play()
      self.Black_.update_check_movelists()
      # check if it is also a checkmate
      if self.Black_.check_no_moves_left():
        Board.checkmate = True
        Black.lose = True
    elif self.check_black_check() == False and not killed:
      if sound:
        Sound.move.play()
      # check if moving caused a stalemate
      if self.Black_.check_no_moves_left():
        Board.stalemate = True
    Board.check_draw()
    self.reset_enpassant()
    White.turn = False
    Black.turn = True
    Board.moves["color"].append("W")
    if Board.freeze != True:
      Board.total_moves += 1
    if testing:
      White.turn = True
      Black.turn = True

  def destroy(self, piece):
    "Destroy a piece."
    if piece == "K":
      WhiteKing.alive = 0
      WhiteKing.col = -1
      WhiteKing.row = -1
      WhiteKing.x = -1
      WhiteKing.y = -1
      WhiteKing.movelist.clear()
    # queen
    for i in range(White.num_queens):
      if piece == "Q" + str(i):
        WhiteQueen.alive[i] = 0
        WhiteQueen.col[i] = -1
        WhiteQueen.row[i] = -1
        WhiteQueen.x[i] = -1
        WhiteQueen.y[i] = -1
        WhiteQueen.movelist[i].clear()
        WhiteQueen.protecting_movelist[i].clear()
        WhiteQueen.pinned_movelist[i].clear()
        WhiteQueen.in_path[i] = 0
    # pawn
    for i in range(8):
      if piece == "P" + str(i):
        WhitePawn.alive[i] = 0
        WhitePawn.col[i] = -1
        WhitePawn.row[i] = -1
        WhitePawn.x[i] = -1
        WhitePawn.y[i] = -1
        WhitePawn.movelist[i].clear()
        WhitePawn.hit_movelist[i].clear()
    # bishop, rook, knight
    for i in range(2):
      if piece == "B" + str(i):
        WhiteBishop.alive[i] = 0
        WhiteBishop.col[i] = -1
        WhiteBishop.row[i] = -1
        WhiteBishop.x[i] = -1
        WhiteBishop.y[i] = -1
        WhiteBishop.movelist[i].clear()
        WhiteBishop.protecting_movelist[i].clear()
        WhiteBishop.pinned_movelist[i].clear()
        WhiteBishop.in_path[i] = 0
      if piece == "R" + str(i):
        WhiteRook.alive[i] = 0
        WhiteRook.col[i] = -1
        WhiteRook.row[i] = -1
        WhiteRook.x[i] = -1
        WhiteRook.y[i] = -1
        WhiteRook.movelist[i].clear()
        WhiteRook.protecting_movelist[i].clear()
        WhiteRook.pinned_movelist[i].clear()
        WhiteRook.in_path[i] = 0
      if piece == "N" + str(i):
        WhiteKnight.alive[i] = 0
        WhiteKnight.col[i] = -1
        WhiteKnight.row[i] = -1
        WhiteKnight.x[i] = -1
        WhiteKnight.y[i] = -1
        WhiteKnight.movelist[i].clear()
        WhiteKnight.protecting_movelist[i].clear()

  def check_kill(self, row, col, sound):
    """Once a white piece has moved to a new position, check
    if a black piece is already there. If so, kill it.
    """
    if Black.blocks[row][col] == 1:
      Black.blocks[row][col] = 0
      killed_piece = self.Black_.get_piece(row, col)
      # King
      if killed_piece == "K":
        Board.moves["killed"].append(True)
        Board.killed["piece"].append("K")
        Board.killed["pos"].append((BlackKing.row, BlackKing.col))
        BlackKing.alive = 0
        BlackKing.col = -1
        BlackKing.row = -1
        BlackKing.x = -1
        BlackKing.y = -1
        BlackKing.movelist.clear()
        if sound:
          Sound.kill.play()
        return True
      # queen
      for i in range(Black.num_queens):
        if killed_piece == "Q" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("Q" + str(i))
          Board.killed["pos"].append((BlackQueen.row[i], BlackQueen.col[i]))
          BlackQueen.alive[i] = 0
          BlackQueen.col[i] = -1
          BlackQueen.row[i] = -1
          BlackQueen.x[i] = -1
          BlackQueen.y[i] = -1
          BlackQueen.movelist[i].clear()
          BlackQueen.protecting_movelist[i].clear()
          BlackQueen.pinned_movelist[i].clear()
          BlackQueen.in_path[i] = 0
          if sound:
            Sound.kill.play()
          return True
      # pawn
      for i in range(8):
        if killed_piece == "P" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("P" + str(i))
          Board.killed["pos"].append((BlackPawn.row[i], BlackPawn.col[i]))
          BlackPawn.alive[i] = 0
          BlackPawn.col[i] = -1
          BlackPawn.row[i] = -1
          BlackPawn.x[i] = -1
          BlackPawn.y[i] = -1
          BlackPawn.movelist[i].clear()
          BlackPawn.hit_movelist[i].clear()
          if sound:
            Sound.kill.play()
          return True
      # bishop, rook, knight
      for i in range(2):
        if killed_piece == "B" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("B" + str(i))
          Board.killed["pos"].append((BlackBishop.row[i], BlackBishop.col[i]))
          BlackBishop.alive[i] = 0
          BlackBishop.col[i] = -1
          BlackBishop.row[i] = -1
          BlackBishop.x[i] = -1
          BlackBishop.y[i] = -1
          BlackBishop.movelist[i].clear()
          BlackBishop.protecting_movelist[i].clear()
          BlackBishop.pinned_movelist[i].clear()
          BlackBishop.in_path[i] = 0
          if sound:
            Sound.kill.play()
          return True
        if killed_piece == "R" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("R" + str(i))
          Board.killed["pos"].append((BlackRook.row[i], BlackRook.col[i]))
          BlackRook.alive[i] = 0
          BlackRook.col[i] = -1
          BlackRook.row[i] = -1
          BlackRook.x[i] = -1
          BlackRook.y[i] = -1
          BlackRook.movelist[i].clear()
          BlackRook.protecting_movelist[i].clear()
          BlackRook.pinned_movelist[i].clear()
          BlackRook.in_path[i] = 0
          if sound:
            Sound.kill.play()
          return True
        if killed_piece == "N" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("N" + str(i))
          Board.killed["pos"].append((BlackKnight.row[i], BlackKnight.col[i]))
          BlackKnight.alive[i] = 0
          BlackKnight.col[i] = -1
          BlackKnight.row[i] = -1
          BlackKnight.x[i] = -1
          BlackKnight.y[i] = -1
          BlackKnight.movelist[i].clear()
          BlackKnight.protecting_movelist[i].clear()
          if sound:
            Sound.kill.play()
          return True
    Board.moves["killed"].append(False)
    return False

  def check_black_check(self):
    """Check detection. If the black king's position is in the movelist
    of any white piece, then it is checked.
    """
    pos = (BlackKing.row, BlackKing.col)
    for i in range(White.num_queens):
      if pos in WhiteQueen.movelist[i]:
        White.checker = "Q" + str(i)
        return 1
    for i in range(8):
      if pos in WhitePawn.hit_movelist[i]:
        White.checker = "P" + str(i)
        return 1
    for i in range(2):
      if pos in WhiteBishop.movelist[i]:
        White.checker = "B" + str(i)
        return 1
      if pos in WhiteRook.movelist[i]:
        White.checker = "R" + str(i)
        return 1
      if pos in WhiteKnight.movelist[i]:
        White.checker = "N" + str(i)
        return 1
    White.checker = ""
    return 0

  def update_check_movelists(self):
    """White has been checked. Replace all white piece moves (except king)
    with moves such that white is not checked anymore.
    """
    # build check movelist from the white piece that is checking the black king
    movelist = []
    for i in range(Black.num_queens):
      if Black.checker == "Q" + str(i):
        movelist = BlackQueen.build_check_movelist().copy()
    for i in range(2):
      if Black.checker == "B" + str(i):
        movelist = BlackBishop.build_check_movelist().copy()
      elif Black.checker == "R" + str(i):
        movelist = BlackRook.build_check_movelist().copy()
      elif Black.checker == "N" + str(i):
        movelist = [(BlackKnight.row[i], BlackKnight.col[i])]
    for i in range(8):
      if Black.checker == "P" + str(i):
        movelist = [(BlackPawn.row[i], BlackPawn.col[i])]

    # now filter all white piece movelists with the new check movelist
    for i in range(White.num_queens):
      self.filter("Q" + str(i), movelist)
    for i in range(2):
      self.filter("B" + str(i), movelist)
      self.filter("R" + str(i), movelist)
      self.filter("N" + str(i), movelist)
    for i in range(8):
      self.filter("P" + str(i), movelist)

  def check_no_moves_left(self):
    "Returns true if White has no moves left to play."
    if WhiteKing.movelist != []:
      return 0
    for i in range(White.num_queens):
      if WhiteQueen.movelist[i] != []:
        return 0
    for i in range(2):
      if WhiteBishop.movelist[i] != [] or WhiteRook.movelist[i] != [] or \
      WhiteKnight.movelist[i] != []:
        return 0
    for i in range(8):
      if WhitePawn.movelist[i] != []:
        return 0
    return 1

  def check_black_pin(self):
    "Check if any black piece is pinned by a white bishop, rook, or queen."
    WhiteBishop.check_pin()
    WhiteQueen.check_pin()
    WhiteRook.check_pin()

  def reset_enpassant(self):
    "Reset opposite side's pawn en passant flags."
    for i in range(8):
      White.en_passant[i] = 0

  def promote(self, i):
    "Promote white pawn i to queen."
    White.num_queens += 1
    WhiteQueen.row.append(WhitePawn.row[i])
    WhiteQueen.col.append(WhitePawn.col[i])
    WhiteQueen.x.append(Piece.paddingx + WhitePawn.col[i]*UNIT)
    WhiteQueen.y.append(Piece.paddingy + WhitePawn.row[i]*UNIT)
    WhiteQueen.img.append(pg.image.load('../assets/sprites/whiteQueen.png'))
    WhiteQueen.img[-1] = pg.transform.scale(WhiteQueen.img[-1], (Piece.scale, Piece.scale))
    WhiteQueen.movelist.append([])
    WhiteQueen.protecting_movelist.append([])
    WhiteQueen.pinned_movelist.append([])
    WhiteQueen.alive.append(1)
    WhiteQueen.in_path.append(0)

    WhitePawn.alive[i] = 0
    WhitePawn.col[i] = -1
    WhitePawn.row[i] = -1
    WhitePawn.x[i] = -1
    WhitePawn.y[i] = -1
    WhitePawn.movelist[i].clear()

  def unpromote(self, i, row, col):
    # kill last queen
    White.num_queens -= 1
    WhiteQueen.row.pop(-1)
    WhiteQueen.col.pop(-1)
    WhiteQueen.x.pop(-1)
    WhiteQueen.y.pop(-1)
    WhiteQueen.img.pop(-1)
    WhiteQueen.movelist.pop(-1)
    WhiteQueen.protecting_movelist.pop(-1)
    WhiteQueen.pinned_movelist.pop(-1)
    WhiteQueen.alive.pop(-1)
    WhiteQueen.in_path.pop(-1)
    # revive last pawn
    WhitePawn.alive[i] = 1
    WhitePawn.col[i] = col
    WhitePawn.row[i] = row
    WhitePawn.x[i] = Piece.paddingx + col*UNIT
    WhitePawn.y[i] = Piece.paddingy + row*UNIT
    WhitePawn.movelist[i].clear()
    White.blocks[row][col] = 1

  def in_movelist(self, row, col):
    """Helper function which returns true if position (row, col) is in the movelist
    of any Black piece.
    """
    for i in BlackKing.movelist:
      if i == (row, col):
        return True
    for i in range(Black.num_queens):
      for k in BlackQueen.movelist[i]:
        if k == (row, col):
          return True
    for i in range(8):
      for k in BlackPawn.movelist[i]:
        if k == (row, col):
          return True
    for i in range(2):
      for k in BlackBishop.movelist[i]:
        if k == (row, col):
          return True
      for k in BlackRook.movelist[i]:
        if k == (row, col):
          return True
      for k in BlackKnight.movelist[i]:
        if k == (row, col):
          return True
    return False

  def castle_criteria_king(self):
    """Return true if king-side castling is allowed. i.e:
    - King & rook 1 have not moved
    - No pieces (white or black) between king and rook 1
    - King is not checked
    - Squares between rook 1 & king are not attacked
    - King does not end up in check
    """
    if WhiteKing.moved == True or WhiteRook.moved[1] == True:
      return False
    if Black.blocks[7][6] == 1 or Black.blocks[7][5] == 1 or White.blocks[7][6] == 1 \
    or White.blocks[7][5] == 1:
      return False
    if Black.checker != "":
      return False
    if self.in_movelist(7, 6) == True or self.in_movelist(7, 5) == True:
      return False
    return True

  def castle_criteria_queen(self):
    "Same as above but for queen-side castle (& rook 0)."
    if WhiteKing.moved == True or WhiteRook.moved[0] == True:
      return False
    if Black.blocks[7][1] == 1 or Black.blocks[7][2] == 1 or Black.blocks[7][3] == 1 \
    or White.blocks[7][1] == 1 or White.blocks[7][2] == 1 or White.blocks[7][3] == 1:
      return False
    if Black.checker != "":
      return False
    if self.in_movelist(7, 1) == True or self.in_movelist(7, 2) == True or self.in_movelist(7, 3):
      return False
    return True

  def castle_queen(self, sound):
    "Queen-side castle."
    Board.moves["pos"].append("CQ")
    WhiteKing.Move(7, 2)
    WhiteRook.Move(0, 7, 3)
    self.valid_move(False, sound)
    White.castled = 1
    Board.moves["piece"].append("CQ")
    Board.moves["killed"].append(False)

  def castle_king(self, sound):
    "King-side castle."
    Board.moves["pos"].append("CK")
    WhiteKing.Move(7, 6)
    WhiteRook.Move(1, 7, 5)
    self.valid_move(False, sound)
    White.castled = 1
    Board.moves["piece"].append("CK")
    Board.moves["killed"].append(False)

  def two_knights(self):
    "Below functions are used for draw by insufficient material."
    for i in range(White.num_queens):
      if WhiteQueen.alive[i] == 1:
        return False
    for i in range(8):
      if WhitePawn.alive[i] == 1:
        return False
    for i in range(2):
      if WhiteBishop.alive[i] == 1:
        return False
      if WhiteRook.alive[i] == 1:
        return False
    if WhiteKnight.alive[0] == 1 and WhiteKnight.alive[1] == 1:
      return True
    return False

  def one_knight(self):
    for i in range(White.num_queens):
      if WhiteQueen.alive[i] == 1:
        return False
    for i in range(8):
      if WhitePawn.alive[i] == 1:
        return False
    for i in range(2):
      if WhiteBishop.alive[i] == 1:
        return False
      if WhiteRook.alive[i] == 1:
        return False
    if WhiteKnight.alive[0] != WhiteKnight.alive[1]:
      return True
    return False

  def lone_king(self):
    for i in range(White.num_queens):
      if WhiteQueen.alive[i] == 1:
        return False
    for i in range(8):
      if WhitePawn.alive[i] == 1:
        return False
    for i in range(2):
      if WhiteBishop.alive[i] == 1:
        return False
      if WhiteRook.alive[i] == 1:
        return False
      if WhiteKnight.alive[i] == 1:
        return False
    return True

  def one_bishop(self):
    for i in range(White.num_queens):
      if WhiteQueen.alive[i] == 1:
        return False
    for i in range(8):
      if WhitePawn.alive[i] == 1:
        return False
    for i in range(2):
      if WhiteRook.alive[i] == 1:
        return False
      if WhiteKnight.alive[i] == 1:
        return False
    if WhiteBishop.alive[0] != WhiteBishop.alive[1]:
      return True
    return False

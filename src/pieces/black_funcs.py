from common import *

class Black_Funcs(object):
  "Methods relating to black pieces."

  def __init__(self, White_):
    self.White_ = White_
    self.piece = ""

  def destroy(self, piece):
    "Destroy a piece."
    if piece == "K":
      BlackKing.alive = 0
      BlackKing.col = -1
      BlackKing.row = -1
      BlackKing.x = -1
      BlackKing.y = -1
      BlackKing.movelist.clear()
    # queen
    for i in range(Black.num_queens):
      if piece == "Q" + str(i):
        BlackQueen.alive[i] = 0
        BlackQueen.col[i] = -1
        BlackQueen.row[i] = -1
        BlackQueen.x[i] = -1
        BlackQueen.y[i] = -1
        BlackQueen.movelist[i].clear()
        BlackQueen.protecting_movelist[i].clear()
        BlackQueen.pinned_movelist[i].clear()
        BlackQueen.in_path[i] = 0
    # pawn
    for i in range(8):
      if piece == "P" + str(i):
        BlackPawn.alive[i] = 0
        BlackPawn.col[i] = -1
        BlackPawn.row[i] = -1
        BlackPawn.x[i] = -1
        BlackPawn.y[i] = -1
        BlackPawn.movelist[i].clear()
        BlackPawn.hit_movelist[i].clear()
    # bishop, rook, knight
    for i in range(2):
      if piece == "B" + str(i):
        BlackBishop.alive[i] = 0
        BlackBishop.col[i] = -1
        BlackBishop.row[i] = -1
        BlackBishop.x[i] = -1
        BlackBishop.y[i] = -1
        BlackBishop.movelist[i].clear()
        BlackBishop.protecting_movelist[i].clear()
        BlackBishop.pinned_movelist[i].clear()
        BlackBishop.in_path[i] = 0
      if piece == "R" + str(i):
        BlackRook.alive[i] = 0
        BlackRook.col[i] = -1
        BlackRook.row[i] = -1
        BlackRook.x[i] = -1
        BlackRook.y[i] = -1
        BlackRook.movelist[i].clear()
        BlackRook.protecting_movelist[i].clear()
        BlackRook.pinned_movelist[i].clear()
        BlackRook.in_path[i] = 0
      if piece == "N" + str(i):
        BlackKnight.alive[i] = 0
        BlackKnight.col[i] = -1
        BlackKnight.row[i] = -1
        BlackKnight.x[i] = -1
        BlackKnight.y[i] = -1
        BlackKnight.movelist[i].clear()
        BlackKnight.protecting_movelist[i].clear()


  def get_freeze(self):
    return Board.freeze

  def play(self):
    if Board.stalemate or Board.checkmate or Board.insufficient_mat or Board.tfr:
      return
    if Black.ai:
      from black_ai import Black_AI
      AI = Black_AI()
      AI.generate_move()
      White.turn = True
      Black.turn = False
    else:
      if Black.blocks[Queue.row[-1]][Queue.col[-1]] == 1:
        self.piece = self.get_piece(Queue.row[-1], Queue.col[-1])
      # regular move
      if len(Queue.col) >= 2 and Black.blocks[Queue.row[0]][Queue.col[0]] == 1 \
      and Black.blocks[Queue.row[1]][Queue.col[1]] == 0:
        self.move_piece(self.piece, Queue.row[-1], Queue.col[-1], True)
      # queen side castle
      elif len(Queue.col) >= 2 and (Queue.row[0], Queue.col[0]) == (BlackKing.row, BlackKing.col) \
      and (Queue.row[1], Queue.col[1]) == (BlackRook.row[0], BlackRook.col[0]) and \
      self.castle_criteria_queen():
        self.castle_queen(True)
      # king side castle
      elif len(Queue.col) >= 2 and (Queue.row[0], Queue.col[0]) == (BlackKing.row, BlackKing.col) \
      and (Queue.row[1], Queue.col[1]) == (BlackRook.row[1], BlackRook.col[1]) and \
      self.castle_criteria_king():
        self.castle_king(True)

  def filter(self, piece, pinned_movelist):
    """Helper function which removes any coordinates in a black piece's movelist
    which is not contained in pinned_movelist. Used to assign pinned movelists to pieces.
    """
    new_movelist = []
    for i in range(Black.num_queens):
      if piece == "Q" + str(i):
        for k in BlackQueen.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        BlackQueen.movelist[i] = new_movelist.copy()
    for i in range(8):
      new_movelist.clear()
      if piece == "P" + str(i):
        for k in BlackPawn.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        BlackPawn.movelist[i] = new_movelist.copy()
    for i in range(2):
      new_movelist.clear()
      if piece == "R" + str(i):
        for k in BlackRook.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        BlackRook.movelist[i] = new_movelist.copy()
      elif piece == "B" + str(i):
        for k in BlackBishop.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        BlackBishop.movelist[i] = new_movelist.copy()
      elif piece == "N" + str(i):
        for k in BlackKnight.movelist[i]:
          if not (k not in pinned_movelist):
            new_movelist.append(k)
        BlackKnight.movelist[i] = new_movelist.copy()

  def get_pos(self, piece):
    """Getter for accessing black piece positions.
    Return coordinates of black piece.
    """
    if piece == "K":
      return (BlackKing.row, BlackKing.col)
    for i in range(Black.num_queens):
      if piece == "Q" + str(i):
        return (BlackQueen.row[i], BlackQueen.col[i])
    for i in range(8):
      if piece == "P" + str(i):
        return (BlackPawn.row[i], BlackPawn.col[i])
    for i in range(2):
      if piece == "P" + str(i):
        return (BlackBishop.row[i], BlackBishop.col[i])
      elif piece == "N" + str(i):
        return (BlackKnight.row[i], BlackKnight.col[i])
      elif piece == "R" + str(i):
        return (BlackRook.row[i], BlackRook.col[i])


  def get_movelist(self, piece):
    """Getter for accessing white piece movelist.
    Return movelist of white piece.
    """
    if piece == "K":
      return BlackKing.movelist
    for i in range(Black.num_queens):
      if piece == "Q" + str(i):
        return BlackQueen.movelist[i]
    for i in range(2):
      if piece == "B" + str(i):
        return BlackBishop.movelist[i]
      elif piece == "N" + str(i):
        return BlackKnight.movelist[i]
      elif piece == "R" + str(i):
        return BlackRook.movelist[i]
    for i in range(8):
      if piece == "P" + str(i):
        return BlackPawn.movelist[i]

  def get_piece(self, row, col):
    "Get black piece (as string) at position (row, col)."
    piece = ""
    # King
    if BlackKing.row == row and BlackKing.col == col:
      return "K"
    # Queen
    for i in range(Black.num_queens):
      if BlackQueen.row[i] == row and BlackQueen.col[i] == col:
        return "Q" + str(i)
    # Bishop, knight, rook
    for i in range(2):
      if BlackBishop.row[i] == row and BlackBishop.col[i] == col:
        return "B" + str(i)
      if BlackKnight.row[i] == row and BlackKnight.col[i] == col:
        return "N" + str(i)
      if BlackRook.row[i] == row and BlackRook.col[i] == col:
        return "R" + str(i)
    # Pawn
    for i in range(8):
      if BlackPawn.row[i] == row and BlackPawn.col[i] == col:
        return "P" + str(i)

  def move_piece(self, piece, row, col, sound):
    "Move piece to position (row, col)."
    moved = False
    killed = False
    self.reset_enpassant()
    if row > 7 or col > 7 or row < 0 or col < 0:
      print("(row, col) bad numbers!")
      return
    # King
    if piece == "K" and (row, col) in BlackKing.movelist:
      killed = self.check_kill(row, col, sound)
      Board.moves["pos"].append((BlackKing.row, BlackKing.col))
      moved = True
      Board.moves["piece"].append("K")
      BlackKing.Move(row, col)
    elif piece == "K" and (row, col) not in BlackKing.movelist and sound:
      Sound.error.play()

    # Queen
    for i in range(Black.num_queens):
      if piece == "Q" + str(i) and (row, col) in BlackQueen.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((BlackQueen.row[i], BlackQueen.col[i]))
        BlackQueen.Move(i, row, col)
        Board.moves["piece"].append("Q" + str(i))
        moved = True
      elif piece == "Q" + str(i) and (row, col) not in BlackQueen.movelist[i] and sound:
        Sound.error.play()

    # Pawn
    for i in range(8):
      if piece == "P" + str(i) and (row, col) in BlackPawn.movelist[i]:
        if BlackPawn.row[i] == 4 and White.en_passant[col] == 1:
          killed = self.check_kill(row - 1, col, sound)
        else:
          killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((BlackPawn.row[i], BlackPawn.col[i]))
        BlackPawn.Move(i, row, col)
        Board.moves["piece"].append("P" + str(i))
        moved = True
        if row == 7:
          self.promote(i)
      elif piece == "P" + str(i) and (row, col) not in BlackPawn.movelist[i] and sound:
        Sound.error.play()

    # Knight, bishop, rook
    for i in range(2):
      if piece == "N" + str(i) and (row, col) in BlackKnight.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((BlackKnight.row[i], BlackKnight.col[i]))
        BlackKnight.Move(i, row, col)
        Board.moves["piece"].append("N" + str(i))
        moved = True
      elif (piece == "N" + str(i) and (row, col) not in BlackKnight.movelist[i]) and sound:
        Sound.error.play()
      if piece == "B" + str(i) and (row, col) in BlackBishop.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((BlackBishop.row[i], BlackBishop.col[i]))
        BlackBishop.Move(i, row, col)
        Board.moves["piece"].append("B" + str(i))
        moved = True
      elif (piece == "B" + str(i) and (row, col) not in BlackBishop.movelist[i]) and sound:
        Sound.error.play()
      if piece == "R" + str(i) and (row, col) in BlackRook.movelist[i]:
        killed = self.check_kill(row, col, sound)
        Board.moves["pos"].append((BlackRook.row[i], BlackRook.col[i]))
        BlackRook.Move(i, row, col)
        Board.moves["piece"].append("R" + str(i))
        moved = True
      elif (piece == "R" + str(i) and (row, col) not in BlackRook.movelist[i]) and sound:
        Sound.error.play()

    if moved:
      self.valid_move(killed, sound)

  def valid_move(self, killed, sound):
    """A valid move has been made. Update the board, check for pins,
    checkmate, stalemate,...etc.
    """
    Board.update_all_moves()
    self.check_white_pin()
    # check if white has been checked
    if self.check_white_check():
      if sound:
        Sound.check.play()
      self.White_.update_check_movelists()
      # check if it is also a checkmate
      if self.White_.check_no_moves_left():
        Board.checkmate = True
        White.lose = True
    elif self.check_white_check() == False and not killed:
      if sound:
        Sound.move.play()
      # check if moving caused a stalemate
      if self.White_.check_no_moves_left():
        Board.stalemate = True
    Board.check_draw()
    White.turn = True
    Black.turn = False
    Board.moves["color"].append("B")
    if Board.freeze != True:
      Board.total_moves += 1
    if testing:
      White.turn = True
      Black.turn = True

  def check_kill(self, row, col, sound):
    """Once a black piece has moved to a new position, check
    if a white piece is already there. If so, kill it.
    """
    if White.blocks[row][col] == 1:
      White.blocks[row][col] = 0
      killed_piece = self.White_.get_piece(row, col)
      # King
      if killed_piece == "K":
        Board.moves["killed"].append(True)
        Board.killed["piece"].append("K")
        Board.killed["pos"].append((WhiteKing.row, WhiteKing.col))
        WhiteKing.alive = 0
        WhiteKing.col = -1
        WhiteKing.row = -1
        WhiteKing.x = -1
        WhiteKing.y = -1
        WhiteKing.movelist.clear()
        if sound:
          Sound.kill.play()
        return True
      # queen
      for i in range(White.num_queens):
        if killed_piece == "Q" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("Q" + str(i))
          Board.killed["pos"].append((WhiteQueen.row[i], WhiteQueen.col[i]))
          WhiteQueen.alive[i] = 0
          WhiteQueen.col[i] = -1
          WhiteQueen.row[i] = -1
          WhiteQueen.x[i] = -1
          WhiteQueen.y[i] = -1
          WhiteQueen.movelist[i].clear()
          WhiteQueen.protecting_movelist[i].clear()
          WhiteQueen.pinned_movelist[i].clear()
          WhiteQueen.in_path[i] = 0
          if sound:
            Sound.kill.play()
          return True
      # pawn
      for i in range(8):
        if killed_piece == "P" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("P"  + str(i))
          Board.killed["pos"].append((WhitePawn.row[i], WhitePawn.col[i]))
          WhitePawn.alive[i] = 0
          WhitePawn.col[i] = -1
          WhitePawn.row[i] = -1
          WhitePawn.x[i] = -1
          WhitePawn.y[i] = -1
          WhitePawn.movelist[i].clear()
          WhitePawn.hit_movelist[i].clear()
          if sound:
            Sound.kill.play()
          return True
      # bishop, rook, knight
      for i in range(2):
        if killed_piece == "B" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("B" + str(i))
          Board.killed["pos"].append((WhiteBishop.row[i], WhiteBishop.col[i]))
          WhiteBishop.alive[i] = 0
          WhiteBishop.col[i] = -1
          WhiteBishop.row[i] = -1
          WhiteBishop.x[i] = -1
          WhiteBishop.y[i] = -1
          WhiteBishop.movelist[i].clear()
          WhiteBishop.protecting_movelist[i].clear()
          WhiteBishop.pinned_movelist[i].clear()
          WhiteBishop.in_path[i] = 0
          if sound:
            Sound.kill.play()
          return True
        elif killed_piece == "R" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("R" + str(i))
          Board.killed["pos"].append((WhiteRook.row[i], WhiteRook.col[i]))
          WhiteRook.alive[i] = 0
          WhiteRook.col[i] = -1
          WhiteRook.row[i] = -1
          WhiteRook.x[i] = -1
          WhiteRook.y[i] = -1
          WhiteRook.movelist[i].clear()
          WhiteRook.protecting_movelist[i].clear()
          WhiteRook.pinned_movelist[i].clear()
          WhiteRook.in_path[i] = 0
          if sound:
            Sound.kill.play()
          return True
        elif killed_piece == "N" + str(i):
          Board.moves["killed"].append(True)
          Board.killed["piece"].append("N" + str(i))
          Board.killed["pos"].append((WhiteKnight.row[i], WhiteKnight.col[i]))
          WhiteKnight.alive[i] = 0
          WhiteKnight.col[i] = -1
          WhiteKnight.row[i] = -1
          WhiteKnight.x[i] = -1
          WhiteKnight.y[i] = -1
          WhiteKnight.movelist[i].clear()
          WhiteKnight.protecting_movelist[i].clear()
          if sound:
            Sound.kill.play()
          return True
    Board.moves["killed"].append(False)
    return False

  def check_white_check(self):
    """Check detection. If the white king's position is in the movelist
    of any black piece, then it is checked.
    """
    pos = (WhiteKing.row, WhiteKing.col)
    for i in range(Black.num_queens):
      if pos in BlackQueen.movelist[i]:
        Black.checker = "Q" + str(i)
        return 1
    for i in range(8):
      if pos in BlackPawn.hit_movelist[i]:
        Black.checker = "P" + str(i)
        return 1
    for i in range(2):
      if pos in BlackBishop.movelist[i]:
        Black.checker = "B" + str(i)
        return 1
      if pos in BlackRook.movelist[i]:
        Black.checker = "R" + str(i)
        return 1
      if pos in BlackKnight.movelist[i]:
        Black.checker = "N" + str(i)
        return 1
    Black.checker = ""
    return 0

  def update_check_movelists(self):
    """Black has been checked. Replace all black piece moves (except king)
    with moves such that black is not checked anymore.
    """
    # build check movelist from the white piece that is checking the black king
    movelist = []
    for i in range(White.num_queens):
      if White.checker == "Q" + str(i):
        movelist = WhiteQueen.build_check_movelist().copy()
    for i in range(2):
      if White.checker == "B" + str(i):
        movelist = WhiteBishop.build_check_movelist().copy()
      elif White.checker == "R" + str(i):
        movelist = WhiteRook.build_check_movelist().copy()
      elif White.checker == "N" + str(i):
        movelist = [(WhiteKnight.row[i], WhiteKnight.col[i])]
    for i in range(8):
      if White.checker == "P" + str(i):
        movelist = [(WhitePawn.row[i], WhitePawn.col[i])]

    # now filter all black piece movelists with the new check movelist
    for i in range(Black.num_queens):
      self.filter("Q" + str(i), movelist)
    for i in range(2):
      self.filter("B" + str(i), movelist)
      self.filter("R" + str(i), movelist)
      self.filter("N" + str(i), movelist)
    for i in range(8):
      self.filter("P" + str(i), movelist)

  def check_no_moves_left(self):
    "Returns true if Black has no moves left to play."
    if BlackKing.movelist != []:
      return 0
    for i in range(Black.num_queens):
      if BlackQueen.movelist[i] != []:
        return 0
    for i in range(2):
      if BlackBishop.movelist[i] != [] or BlackRook.movelist[i] != [] or \
      BlackKnight.movelist[i] != []:
        return 0
    for i in range(8):
      if BlackPawn.movelist[i] != []:
        return 0
    return 1

  def check_white_pin(self):
    "Check if any white piece is pinned by a black bishop, rook, or queen."
    BlackBishop.check_pin()
    BlackQueen.check_pin()
    BlackRook.check_pin()

  def reset_enpassant(self):
    "Reset opposite side's pawn en passant flags."
    for i in range(8):
      Black.en_passant[i] = 0

  def promote(self, i):
    "Promote black pawn i to queen."
    # new queen
    Black.num_queens += 1
    BlackQueen.row.append(BlackPawn.row[i])
    BlackQueen.col.append(BlackPawn.col[i])
    BlackQueen.x.append(Piece.paddingx + BlackPawn.col[i]*UNIT)
    BlackQueen.y.append(Piece.paddingy + BlackPawn.row[i]*UNIT)
    BlackQueen.img.append(pg.image.load('../assets/sprites/blackQueen.png'))
    BlackQueen.img[-1] = pg.transform.scale(BlackQueen.img[-1], (Piece.scale, Piece.scale))
    BlackQueen.movelist.append([])
    BlackQueen.protecting_movelist.append([])
    BlackQueen.pinned_movelist.append([])
    BlackQueen.alive.append(1)
    BlackQueen.in_path.append(0)
    # kill pawn
    BlackPawn.alive[i] = 0
    BlackPawn.col[i] = -1
    BlackPawn.row[i] = -1
    BlackPawn.x[i] = -1
    BlackPawn.y[i] = -1
    BlackPawn.movelist[i].clear()

  def unpromote(self, i, row, col):
    # kill last queen
    Black.num_queens -= 1
    BlackQueen.row.pop(-1)
    BlackQueen.col.pop(-1)
    BlackQueen.x.pop(-1)
    BlackQueen.y.pop(-1)
    BlackQueen.img.pop(-1)
    BlackQueen.movelist.pop(-1)
    BlackQueen.protecting_movelist.pop(-1)
    BlackQueen.pinned_movelist.pop(-1)
    BlackQueen.alive.pop(-1)
    BlackQueen.in_path.pop(-1)
    # revive last pawn
    BlackPawn.alive[i] = 1
    BlackPawn.col[i] = col
    BlackPawn.row[i] = row
    BlackPawn.x[i] = Piece.paddingx + col*UNIT
    BlackPawn.y[i] = Piece.paddingy + row*UNIT
    BlackPawn.movelist[i].clear()
    Black.blocks[row][col] = 1

  def in_movelist(self, row, col):
    """Helper function which returns true if position (row, col) is in the movelist
    of any White piece.
    """
    for i in WhiteKing.movelist:
      if i == (row, col):
        return True
    for i in range(White.num_queens):
      for k in WhiteQueen.movelist[i]:
        if k == (row, col):
          return True
    for i in range(8):
      for k in WhitePawn.movelist[i]:
        if k == (row, col):
          return True
    for i in range(2):
      for k in WhiteBishop.movelist[i]:
        if k == (row, col):
          return True
      for k in WhiteRook.movelist[i]:
        if k == (row, col):
          return True
      for k in WhiteKnight.movelist[i]:
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
    if BlackKing.moved == True or BlackRook.moved[1] == True:
      return False
    if Black.blocks[0][6] == 1 or Black.blocks[0][5] == 1 or White.blocks[0][6] == 1 \
    or White.blocks[0][5] == 1:
      return False
    if White.checker != "":
      return False
    if self.in_movelist(0, 6) == True or self.in_movelist(0, 5) == True:
      return False
    return True

  def castle_criteria_queen(self):
    "Same as above but for queen-side castle (& rook 0)."
    if BlackKing.moved == True or BlackRook.moved[0] == True:
      return False
    if Black.blocks[0][1] == 1 or Black.blocks[0][2] == 1 or Black.blocks[0][3] == 1 \
    or White.blocks[0][1] == 1 or White.blocks[0][2] == 1 or White.blocks[0][3] == 1:
      return False
    if White.checker != "":
      return False
    if self.in_movelist(0, 1) == True or self.in_movelist(0, 2) == True or self.in_movelist(0, 3):
      return False
    return True

  def castle_queen(self, sound):
    "Queen-side castle."
    Board.moves["pos"].append("CQ")
    BlackKing.Move(0, 2)
    BlackRook.Move(0, 0, 3)
    self.valid_move(False, sound)
    Black.castled = 1
    Board.moves["piece"].append("CQ")
    Board.moves["killed"].append(False)

  def castle_king(self, sound):
    "King-side castle."
    Board.moves["pos"].append("CK")
    BlackKing.Move(0, 6)
    BlackRook.Move(1, 0, 5)
    self.valid_move(False, sound)
    Black.castled = 1
    Board.moves["piece"].append("CK")
    Board.moves["killed"].append(False)

  def two_knights(self):
    "Below functions are used for draw by insufficient material."
    for i in range(Black.num_queens):
      if BlackQueen.alive[i] == 1:
        return False
    for i in range(8):
      if BlackPawn.alive[i] == 1:
        return False
    for i in range(2):
      if BlackBishop.alive[i] == 1:
        return False
      if BlackRook.alive[i] == 1:
        return False
    if BlackKnight.alive[0] == 1 and BlackKnight.alive[1] == 1:
      return True
    return False

  def one_knight(self):
    for i in range(Black.num_queens):
      if BlackQueen.alive[i] == 1:
        return False
    for i in range(8):
      if BlackPawn.alive[i] == 1:
        return False
    for i in range(2):
      if BlackBishop.alive[i] == 1:
        return False
      if BlackRook.alive[i] == 1:
        return False
    if BlackKnight.alive[0] != BlackKnight.alive[1]:
      return True
    return False

  def lone_king(self):
    for i in range(Black.num_queens):
      if BlackQueen.alive[i] == 1:
        return False
    for i in range(8):
      if BlackPawn.alive[i] == 1:
        return False
    for i in range(2):
      if BlackBishop.alive[i] == 1:
        return False
      if BlackRook.alive[i] == 1:
        return False
      if BlackKnight.alive[i] == 1:
        return False
    return True

  def one_bishop(self):
    for i in range(Black.num_queens):
      if BlackQueen.alive[i] == 1:
        return False
    for i in range(8):
      if BlackPawn.alive[i] == 1:
        return False
    for i in range(2):
      if BlackRook.alive[i] == 1:
        return False
      if BlackKnight.alive[i] == 1:
        return False
    if BlackBishop.alive[0] != BlackBishop.alive[1]:
      return True
    return False

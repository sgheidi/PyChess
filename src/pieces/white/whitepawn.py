from common import *

class White_Pawn(object):
  def __init__(self):
    self.img = [pg.image.load('../assets/sprites/whitePawn.png') for x in range(8)]
    self.img = [pg.transform.scale(self.img[x], (Piece.scale, Piece.scale)) for x in range(8)]
    self.col = [x for x in range(8)]
    self.row = [6 for x in range(8)]
    self.x = [Piece.paddingx]
    self.y = [Piece.paddingy + self.row[0]*UNIT]
    for i in range(8):
      self.x.append(self.x[0]+(UNIT*(i+1)))
      self.y.append(self.y[0])
    self.movelist = [[] for i in range(8)]
    self.hit_movelist = [[] for i in range(8)]
    for i in range(8):
      self.movelist[i].append((self.row[i]-1, self.col[i]))
      self.movelist[i].append((self.row[i]-2, self.col[i]))
    self.alive = [1 for i in range(8)]

  def show(self):
    "Show sprite."
    for i in range(8):
      if self.alive[i] == 1:
        win.blit(self.img[i],(self.x[i], self.y[i]))

  def Move(self, i, row, col):
    "Move pawn i to coordinates (row, col)."
    if abs(self.row[i] - row) == 2:
      White.en_passant[i] = 1
    if (self.row[i], self.col[i]) != (-1, -1):
      White.blocks[self.row[i]][self.col[i]] = 0
    White.blocks[row][col] = 1
    self.col[i] = col
    self.row[i] = row
    self.x[i] = Piece.paddingx + col*UNIT
    self.y[i] = Piece.paddingy + row*UNIT

  def update_movelist(self):
    from pieces.black_funcs import Black_Funcs
    Black_ = Black_Funcs(None)
    for i in range(8):
      self.movelist[i].clear()
      self.hit_movelist[i].clear()
      if self.alive[i] == 0:
        continue
      # normal move (1 forward)
      if self.row[i]-1 >= 0:
        if Black.blocks[self.row[i]-1][self.col[i]] == 0 and \
        White.blocks[self.row[i]-1][self.col[i]] == 0:
          self.movelist[i].append((self.row[i]-1, self.col[i]))
      # opponent on left
      if self.row[i]-1 >= 0 and self.col[i]-1 >= 0:
        self.hit_movelist[i].append((self.row[i]-1, self.col[i]-1))
        if Black.blocks[self.row[i]-1][self.col[i]-1] == 1:
          self.movelist[i].append((self.row[i]-1, self.col[i]-1))
      # opponent on right
      if self.row[i]-1 >= 0 and self.col[i]+1 <= 7:
        self.hit_movelist[i].append((self.row[i]-1, self.col[i]+1))
        if Black.blocks[self.row[i]-1][self.col[i]+1] == 1:
          self.movelist[i].append((self.row[i]-1, self.col[i]+1))
      # initial double-step
      if self.row[i] == 6 and Black.blocks[self.row[i]-1][self.col[i]] == 0 and \
      White.blocks[self.row[i]-1][self.col[i]] == 0 and \
      Black.blocks[self.row[i]-2][self.col[i]] == 0 and \
      White.blocks[self.row[i]-2][self.col[i]] == 0:
        self.movelist[i].append((self.row[i]-2, self.col[i]))
      # en passant
      if self.row[i] == 3:
        for k in range(len(Black.en_passant)):
          if Black.en_passant[k] == 1:
            pos = Black_.get_pos("P" + str(k))
            if abs(pos[1] - self.col[i]) == 1:
              self.movelist[i].append((pos[0] - 1, pos[1]))

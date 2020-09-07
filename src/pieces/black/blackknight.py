from common import *

class Black_Knight(object):
  def __init__(self):
    self.img = [pg.image.load('../assets/sprites/blackKnight.png') for x in range(2)]
    self.img = [pg.transform.scale(self.img[x], (Piece.scale, Piece.scale)) for x in range(2)]
    self.col = [1, 6]
    self.row = [0, 0]
    self.x = [Piece.paddingx + self.col[0]*UNIT, Piece.paddingx + self.col[1]*UNIT]
    self.y = [Piece.paddingy + self.row[0]*UNIT, Piece.paddingy + self.row[1]*UNIT]
    self.movelist = [[], []]
    self.protecting_movelist = [[], []]
    for i in range(2):
      self.movelist[i].append((self.row[i]-2, self.col[i]-1))
      self.movelist[i].append((self.row[i]-2, self.col[i]+1))
    self.alive = [1 for i in range(2)]

  def show(self):
    for i in range(2):
      if self.alive[i] == 1:
        win.blit(self.img[i],(self.x[i], self.y[i]))

  def Move(self, i, row, col):
    "Move knight i to coordinates (row, col)."
    if (self.row[i], self.col[i]) != (-1, -1):
      Black.blocks[self.row[i]][self.col[i]] = 0
    Black.blocks[row][col] = 1
    self.col[i] = col
    self.row[i] = row
    self.x[i] = Piece.paddingx + col*UNIT
    self.y[i] = Piece.paddingy + row*UNIT

  def update_movelist(self):
    for i in range(2):
      self.movelist[i].clear()
      self.protecting_movelist[i].clear()
      if self.alive[i] == 0:
        continue
      # vertical moves
      if self.row[i]-2 >= 0 and self.col[i]-1 >= 0:
        if Black.blocks[self.row[i]-2][self.col[i]-1] == 0:
          self.movelist[i].append((self.row[i]-2, self.col[i]-1))
        else:
          self.protecting_movelist[i].append((self.row[i]-2, self.col[i]-1))

      if self.row[i]-2 >= 0 and self.col[i]+1 <= 7:
        if Black.blocks[self.row[i]-2][self.col[i]+1] == 0:
          self.movelist[i].append((self.row[i]-2, self.col[i]+1))
        else:
          self.protecting_movelist[i].append((self.row[i]-2, self.col[i]+1))

      if self.row[i]+2 <= 7 and self.col[i]-1 >= 0:
        if Black.blocks[self.row[i]+2][self.col[i]-1] == 0:
          self.movelist[i].append((self.row[i]+2, self.col[i]-1))
        else:
          self.protecting_movelist[i].append((self.row[i]+2, self.col[i]-1))

      if self.row[i]+2 <= 7 and self.col[i]+1 <= 7:
        if Black.blocks[self.row[i]+2][self.col[i]+1] == 0:
          self.movelist[i].append((self.row[i]+2, self.col[i]+1))
        else:
          self.protecting_movelist[i].append((self.row[i]+2, self.col[i]+1))

      # horizontal moves
      if self.row[i]-1 >= 0 and self.col[i]-2 >= 0:
        if Black.blocks[self.row[i]-1][self.col[i]-2] == 0:
          self.movelist[i].append((self.row[i]-1, self.col[i]-2))
        else:
          self.protecting_movelist[i].append((self.row[i]-1, self.col[i]-2))

      if self.row[i]+1 <= 7 and self.col[i]-2 >= 0:
        if Black.blocks[self.row[i]+1][self.col[i]-2] == 0:
          self.movelist[i].append((self.row[i]+1, self.col[i]-2))
        else:
          self.protecting_movelist[i].append((self.row[i]+1, self.col[i]-2))

      if self.row[i]-1 >= 0 and self.col[i]+2 <= 7:
        if Black.blocks[self.row[i]-1][self.col[i]+2] == 0:
          self.movelist[i].append((self.row[i]-1, self.col[i]+2))
        else:
          self.protecting_movelist[i].append((self.row[i]-1, self.col[i]+2))

      if self.row[i]+1 <= 7 and self.col[i]+2 <= 7:
        if Black.blocks[self.row[i]+1][self.col[i]+2] == 0:
          self.movelist[i].append((self.row[i]+1, self.col[i]+2))
        else:
          self.protecting_movelist[i].append((self.row[i]+1, self.col[i]+2))

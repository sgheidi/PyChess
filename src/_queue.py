from common import *

class Click_Queue(object):
  """Class for processing row/column selections from
  mouse clicks onto the board.
  """

  def __init__(self):
    self.row = []
    self.col = []

  def enqueue(self):
    if len(self.col) >= 3:
      self.row.pop(0)
      self.col.pop(0)

  def printcontents(self):
    print("Row: %s Col: %s"%(self.row, self.col))

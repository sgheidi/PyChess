from common import *

class Game_Sound(object):
  def __init__(self):
    pg.mixer.init(22050, -16, 9, 251)
    self.move = pg.mixer.Sound("../assets/sounds/move.wav")
    self.error = pg.mixer.Sound("../assets/sounds/error.wav")
    self.kill = pg.mixer.Sound("../assets/sounds/kill.wav")
    self.check = pg.mixer.Sound("../assets/sounds/check.wav")

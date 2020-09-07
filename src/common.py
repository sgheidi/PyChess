import pygame as pg
import os
import sys
import random

RES = 800
UNIT = RES//8
OFFSET = 0
testing = False
undo_key = True
debug_key = True
verbose = False

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (RES, RES/6)
win = pg.display.set_mode((RES,RES+OFFSET))
pg.font.init()
font = pg.font.SysFont('Comic Sans MS', UNIT)

from sound import Game_Sound
from _queue import Click_Queue
from pieces.white_attr import White_Attr
from pieces.black_attr import Black_Attr
from pieces.piece import Piece_Attr
Queue = Click_Queue()
Sound = Game_Sound()
Piece = Piece_Attr()
White = White_Attr()
Black = Black_Attr()

from pieces.black.blackbishop import Black_Bishop
from pieces.black.blackpawn import Black_Pawn
from pieces.black.blackrook import Black_Rook
from pieces.black.blackknight import Black_Knight
from pieces.black.blackqueen import Black_Queen
from pieces.white.whitebishop import White_Bishop
from pieces.white.whitepawn import White_Pawn
from pieces.white.whiterook import White_Rook
from pieces.white.whiteknight import White_Knight
from pieces.white.whitequeen import White_Queen
BlackBishop = Black_Bishop()
BlackKnight = Black_Knight()
BlackPawn = Black_Pawn()
BlackQueen = Black_Queen()
BlackRook = Black_Rook()
WhiteBishop = White_Bishop()
WhitePawn = White_Pawn()
WhiteRook = White_Rook()
WhiteQueen = White_Queen()
WhiteKnight = White_Knight()

from pieces.black.blackking import Black_King
from pieces.white.whiteking import White_King
BlackKing = Black_King()
WhiteKing = White_King()

from board import Game_Board
Board = Game_Board()

from pieces.white_funcs import White_Funcs
from pieces.black_funcs import Black_Funcs
White_ = White_Funcs()
Black_ = Black_Funcs(White_)

from ai_helper import Helper
helper = Helper()
from black_ai import Black_AI
BlackAI = Black_AI()
from white_ai import White_AI
WhiteAI = White_AI()

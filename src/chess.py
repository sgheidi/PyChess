from common import *

def event_loop():
  "Enter game here."
  Board.update_all_moves()
  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        sys.exit()
      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_q or event.key == pg.K_ESCAPE:
          sys.exit()
        elif event.key == pg.K_a and undo_key:
          Board.undo()
        elif debug_key:
          if event.key == pg.K_w:
            for i in range(8):
              print(White.blocks[i])
            print("\n")
          elif event.key == pg.K_b:
            for i in range(8):
              print(Black.blocks[i])
            print("\n")
      elif event.type == pg.MOUSEBUTTONDOWN:
        pos = pg.mouse.get_pos()
        col = Board.get_col(pos[0])
        row = Board.get_row(pos[1])
        Queue.col.append(col)
        Queue.row.append(row)
        Queue.enqueue()
        if not Black.ai and not White.ai:
          if White.turn:
            White_.play()
          elif Black.turn:
            Black_.play()
          if testing:
            if White.turn:
              White_.play()
            if Black.turn:
              Black_.play()
        else:
          if White.turn:
            White_.play()
          elif Black.turn:
            Black_.play()

    Board.draw_board()
    if len(Queue.row) >= 1 and not (Black.ai and White.ai):
      Board.shade(Queue.row[-1],Queue.col[-1])
    Board.show_black()
    Board.show_white()
    Board.check_end()
    pg.display.update()
    if (Board.save_img and screen_capture):
      Board.capture_image()
    if White.ai:
      if White.turn:
        White_.play()
      if testing:
        White_.play()
    Board.draw_board()
    if len(Queue.row) >= 1:
      Board.shade(Queue.row[-1],Queue.col[-1])
    Board.show_black()
    Board.show_white()
    Board.check_end()
    pg.display.update()
    if (Board.save_img and screen_capture):
      Board.capture_image()
    if Black.ai:
      if Black.turn:
        Black_.play()
      if testing:
        Black_.play()


if __name__ == "__main__":
  pg.display.set_caption("PyChess")
  pg.init()
  event_loop()

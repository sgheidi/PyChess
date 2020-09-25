# ♚ PyChess

Fully-featured Chess game written using Pygame.

## Screenshots

![Alt text](screenshots/3r.png?raw=true "Screenshot 1") &nbsp; &nbsp; &nbsp; ![Alt text](screenshots/2rr.png?raw=true "Screenshot 2")

## How to play

To set up: clone repo & run ```pip install -r requirements.txt```
To run: run ```py chess.py```.

## Features
- Chess AI which uses minimax & alpha-beta pruning to search the game tree and find the best move (current AI ELO is around ~950)
- Pinning pieces
- Checking, checkmating
- En passant
- Castling
- Pawn promotion
- Movement animation
- Draw by:
  - Stalemate
  - Insufficient material
  - 3-fold repetition
  - 50-move rule

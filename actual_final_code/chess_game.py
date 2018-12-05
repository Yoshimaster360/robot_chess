import chess
import chess.uci
import sys
sys.path.append('neural-chessboard')
from analyze_board import capture_image
from process_board import identify_pieces_on_board
from read import *
from pylab import imshow, gray, show



#Play the welcome sequence
play('welcome.mp3')
successful_capture = False
while(not successful_capture):
	capture_image()
	current_board = identify_pieces_on_board()
	if(not current_board):
		play("breakdown_error.mp3")
	else:
		successful_capture = True





# board = chess.Board()
# print(board)






# engine = chess.uci.popen_engine("/Users/yashaektefaie/Dropbox/ee106a/robot_chess/actual_final_code/stockfish-10-mac/Mac/stockfish-10-64")
# engine.uci()
# engine.position(board)
# best_move = engine.go(movetime=2000).bestmove
# board.push(best_move)
# board
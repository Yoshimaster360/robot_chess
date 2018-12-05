import chess
import chess.uci
import sys
sys.path.append('neural-chessboard')
from analyze_board import capture_image
from process_board import identify_pieces_on_board
from read import *
from pylab import imshow, gray, show
from chess_api import *


#Display welcome 
play('welcome.mp3')
successful_capture = False
while(not successful_capture):
	capture_image()
	current_board, piece_mapping = identify_pieces_on_board()
	if(not current_board):
		play("breakdown_error.mp3")
	else:
		successful_capture = True
play('finished_analysis_help.mp3')
print(current_board)
current_board = display_fix_dialog(piece_mapping)
print(current_board)
play('thanks_move_time.mp3')
movement_strings = return_move_strings(current_board)



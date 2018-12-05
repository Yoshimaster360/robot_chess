import chess
from chess_gui import *
import chess.uci
import re

dummy_board = chess.Board()

square_name_index = {}
for i,v in zip(chess.SQUARE_NAMES, chess.SQUARES):
	square_name_index[i] = v

color_to_number = {'white':True, 'black': False}
piece_name_index = {}

for i,v in zip(['pawn','knight','bishop','rook','queen','king', 'blank'], [1,2,3,4,5,6, None]):
	piece_name_index[i] = v

def change_board(board):
	def board_changer():
		print("Hello Welcome to the board changer here you can correct any mistakes you think the Bot made")
		print("For reference we take commands as replacements so let me know what square, what piece, and what color to replace with")
		print("Possible Squares: {}".format(chess.SQUARE_NAMES))
		print("Possible Pieces: {}".format(['pawn','knight','bishop','rook','queen','king','blank']))
		print("Possible Colors is just white\tblack")
		print("when you are done just type in done")
		query = input('Put in an input in the form of square (space) piece (space) and color \n')
		while(query.rstrip().lower() != 'done'):
			square, piece, color = query.rstrip().split(' ')
			board.set_piece_at(square_name_index[square.lower()], chess.Piece(piece_name_index[piece.lower()], color_to_number[color.rstrip().lower()]))
			query = input('Put in an input in the form of square (space) piece (space) and color \n')
		return board
	return board_changer

def display_fix_dialog(board = None):
	print("OKAY SHOULD HAVE RECEIVED SSSHHHIIITTT")
	print(board)
	chessGui = QApplication(sys.argv)
	window = MainWindow(board)
	result = window.show()
	chessGui.exec_()	
	return result

def return_move_strings(board):
	engine = chess.uci.popen_engine("/Users/yashaektefaie/Dropbox/ee106a/robot_chess/actual_final_code/stockfish-10-mac/Mac/stockfish-10-64")
	engine.uci()
	engine.position(board)
	best_move = engine.go(movetime=2000).bestmove
	print(best_move)





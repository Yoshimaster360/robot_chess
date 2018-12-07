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
	engine = chess.uci.popen_engine("/home/cc/ee106a/fa18/class/ee106a-abh/ros_workspaces/lab5/src/ik/launch/lab5/robot_chess/actual_final_code/stockfish-10-linux/Linux/stockfish_10_x64")
	engine.uci()
	engine.position(board)
	best_move = engine.go(movetime=2000).bestmove
	print(best_move)
	start, end = re.findall('[a-z][0-9]', str(best_move))
	start, end = start[0].upper() + start[1], end[0].upper() + end[0]
	movement_string = 'M-{}-{}'.format(start, end)
	if(board.remove_piece_at(square_name_index[end])):
		remove_string = 'R-{}'.format(end[0].upper()+end[1])
	else:
		remove_string = None
	return movement_string, remove_string, best_move

class Piece(chess.Piece):
    def __init__(self, piece_type, color, location):
        super().__init__(piece_type, color)
        self.location = location
    
    def __str__(self):
        return "{}\t{}\t{}".format(self.piece_type, self.color, self.location)

    def __hash__(self):
        colour = 0
        if(self.color):
            colour = 1
        return (10**2)*self.piece_type+(10**1)*colour+self.location

def get_dictionary(board):
    pieces_to_index = {}
    for i in chess.SQUARES:
        found_piece = board.piece_at(i)
        if(found_piece):
            new_piece = Piece(found_piece.piece_type, found_piece.color, i)
            pieces_to_index[new_piece] = i
    return pieces_to_index


def get_difference_between_dictionary(dic1, dic2):
    new_dic1, new_dic2 = dict(dic1), dict(dic2)
    for piece in dic1:
        if(piece in dic2):
            del new_dic1[piece]
            del new_dic2[piece]
    return new_dic1, new_dic2

def decode_player_movement(dic_previous, dic_current):
    ##Here we go bois hold on to your fucking seatbelts
    dic_previous_mod, dic_current_mod = dict(dic_previous), dict(dic_current)
    moves_detected = []
    removes_detected = []
    for piece in dic_previous:
        for test in dic_current: 
            if(piece.piece_type == test.piece_type):
                moves_detected.append(chess.Move(piece.location, test.location))
                del dic_previous_mod[piece]
                del dic_current_mod[test]
    
    if(len(dic_previous_mod.keys()) > 1 or len(dic_current_mod.keys()) > 1):
        return False, False
    elif(len(dic_previous_mod.keys()) == 1):
        removes_detected.append('R-{}'.format(dict_previous_mod[list(dic_previous_mod.keys())[0]]))
        
    return moves_detected, removes_detected

def get_what_happened(previous_board, current_board):
	previous_boardd, current_boardd = get_difference_between_dictionary(get_dictionary(previous_board), get_dictionary(current_board))
	moves_detected, removes_detected =  decode_player_movement(previous_boardd, current_boardd)
	print("PREVIOUS BOARD: {}".format(previous_board))
	print("CURRENT BOARD: {}".format(current_board))
	print("MOVES DETECTED: {}".format(moves_detected))
	print("REMOVES DETECTED: {}".format(removes_detected))
	print(previous_board.legal_moves)
	for i in moves_detected:
		if(i not in previous_board.legal_moves):
			return False, False
	return moves_detected, removes_detected


import chess
import chess.uci
import sys
sys.path.append('neural-chessboard')
from analyze_board import capture_image
from process_board import identify_pieces_on_board
from read import *
from pylab import imshow, gray, show
from chess_api import *
from speech_recognition import *


def capture_current_image():
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
	return current_board

#Display welcome 
play('welcome.mp3')
current_board = capture_current_image()
play('thanks_move_time.mp3')
movement_strings, remove_string = return_move_strings(current_board)
print(movement_strings)
print(remove_string)
#Get rotation and translation stuff??
play('moving_time.mp3')
#######
#SEND INFORMATION OVER...?	
#Wait while waiting for robot to finish moving	
#######
play('waiting_for_you.mp3')
result = None
while(not result or (result != 'done' and result != 'finish')):
	print("Have not received anything yet result is {} right now".format(result))
	result = get_audio_input()
play('checking_you_out.mp3')
post_movement = capture_current_image()
print(post_movement)










#!/usr/bin/env python
import chess
import chess.uci
import sys
sys.path.append('neural-chessboard')
from analyze_board import capture_image
from process_board import identify_pieces_on_board
from read import *
from pylab import imshow, gray, show
from chess_api import *
from speechrecognition import *
import subprocess

print("HELLO")
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
print("TALKING")
#Display welcome
play('welcome.mp3')
current_board = capture_current_image()

while(not current_board.is_game_over()):
	#Display welcome 
	play('thanks_move_time.mp3')
	movement_strings, remove_string, move = return_move_strings(current_board.copy())
	file = open('data','w')
	if(not remove_string):
		file.write('{}\n{}\n'.format(remove_string,movement_strings.upper()))
	else:
		file.write('{}\n{}\n'.format(remove_string.upper()+'-00',movement_strings.upper()))
	file.close()
	print(current_board)
	print(movement_strings)
	print(remove_string)
	print(move)
	current_board.push(move)
	print(current_board)

	play('moving_time.mp3')
	print("NOW I AM WAITING FOR THE ROBOT TO MOVE")
	received_data = []
	while('FINISHED' not in received_data):
		file = open('data','r')
		received_data = [i.rstrip() for i in file.readlines()]
	print("WOOOO YOU FINISHED MOVING FUCKER")
	play('waiting_for_you.mp3')

	#######
	valid_move = False
	while(not valid_move):
		play('waiting_for_you.mp3')
		# result = None
		# while(not result or (result != 'done' and result != 'finish')):
		# 	print("Have not received anything yet result is {} right now".format(result))
		# 	result = get_audio_input()
		play('checking_you_out.mp3')
		post_movement = capture_current_image()
		print("OLD BOARD \n {}".format(current_board))
		print("NEW BOARD \n {}".format(post_movement))
		moves_detected, removes_detected = get_what_happened(current_board, post_movement)
		if(not moves_detected and not removes_detected):
			play('cheating.mp3')
		else:
			valid_move = True
	play('moving_on.mp3')
	current_board = post_movement.copy()
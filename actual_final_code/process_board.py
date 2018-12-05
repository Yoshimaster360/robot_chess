import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import mahotas as mh
from pylab import imshow, gray, show
from PIL import Image
import PIL.ImageOps
import imutils
import scipy.misc
import math
from skimage.measure import compare_ssim as ssim
from keras.models import load_model
from keras.preprocessing import image
import os 
import chess

#Load the color model
color = load_model('color_model.h5')

######################################################
#               LOCATION ORDERING                    #  
#               DIFFERENT BASED ON INPUT ANGLE       # 
#                                                    # 
######################################################

#TO DO-- change this ordering based on the rotation -- we assume no rotation is a8 facing you

total_squares = [chess.A8,chess.B8,chess.C8,chess.D8,chess.E8,chess.F8,chess.G8,chess.H8,chess.A7,chess.B7,chess.C7,chess.D7,chess.E7,chess.F7,chess.G7,chess.H7,chess.A6,chess.B6,chess.C6,chess.D6,
                 chess.E6,chess.F6,chess.G6,chess.H6,chess.A5,chess.B5,chess.C5,chess.D5,chess.E5,chess.F5,chess.G5,
                 chess.H5,chess.A4,chess.B4,chess.C4,chess.D4,chess.E4,chess.F4,chess.G4,chess.H4,
                 chess.A3,chess.B3,chess.C3,chess.D3,chess.E3,chess.F3,chess.G3,chess.H3,chess.A2,chess.B2,chess.C2,chess.D2,chess.E2,
                 chess.F2,chess.G2,chess.H2,chess.A1,chess.B1,chess.C1,chess.D1,chess.E1,chess.F1,chess.G1,chess.H1]


######################################################
#               COLOR BOUNDARIES FOR PIECES          #  
#                                                    # 
######################################################

king_boundaries = [
    ([50, 170, 80],  [60, 180, 90]),
    ([80, 150, 80],  [90, 160, 95]),
    ([40, 150, 85],  [60, 160, 95]),
    ([110, 180, 120],  [120, 190, 130]),
    ([110, 150, 120],  [120, 160, 130]),
    ([90, 130, 90],  [100, 140, 100]),
    ([150, 210, 140],  [160, 220, 150]),
    ([90, 135, 90],  [110, 150, 110]),
    ([129, 165, 120],  [160, 175, 130])
]

bishop_boundaries = [
    ([110, 70, 30],  [125, 80, 40]),
    ([120, 80, 50],  [130, 90, 60]),
    ([180, 110, 20],  [200, 140, 60]),
    ([140, 90, 20],  [150, 140, 60])
]

queen_boundaries = [
    ([150, 10, 20],  [190, 40, 60]),
    ([210, 30, 30],  [230, 50, 50]),
    ([170, 60, 60],  [190, 80, 80]),
    ([210, 90, 100],  [220, 100, 110]),
    ([80, 20, 20],  [90, 30, 30]),
    ([120, 35, 45],  [140, 50, 55])
]

rook_boundaries = [
    ([50, 90, 140],  [90, 130, 180]),
    ([30, 60, 90],  [50, 80, 110]),
    ([80, 140, 200],  [100, 1500, 210]),
    ([25, 36, 54],  [30, 41, 60])
]

black_boundaries = [
    ([0, 0, 0],  [50, 50, 50])
]

knight_boundaries = [
    ([240, 230, 60],  [255, 240, 80]),
    ([180, 160, 45],  [190, 170, 60]),
    ([120, 120, 20],  [150, 150, 50]),
    ([240, 240, 100],  [255, 250, 120]),
    ([210, 200, 120],  [220, 210, 130]),
    ([220, 180, 60],  [240, 210, 90]),
    ([160, 160, 50],  [180, 170, 65])
]

pawn_boundaries = [
    ([120, 100, 60],  [150, 130, 100]),
    ([170, 140, 120],  [190, 160, 130]),
    ([140, 140, 125],  [160, 150, 135])
#     ([170, 170, 145],  [190, 180, 165])
]

possible_pieces = [[king_boundaries, 'king'], [queen_boundaries, 'queen'], [bishop_boundaries, 'bishop'], [rook_boundaries, 'rook'], [knight_boundaries, 'knight'],
                  [pawn_boundaries, 'pawn']]
possible_color = [[black_boundaries, 'black']]

from skimage.measure import compare_ssim
from skimage.transform import resize
from scipy.misc import imsave
from scipy.ndimage import imread

def find_closest_letter(input_image3):
    test_image = image.load_img(input_image3, target_size=(84,84))

    
    # imagee = cv2.imread(input_image3)
    # imagee = cv2.cvtColor(imagee, cv2.COLOR_RGB2BGR)
    # imshow(imagee)
    # show()
    
    piece = None
    current_largest = 0
    colour = 'white'
    
    for boundry, name in possible_pieces:
        for (lower, upper) in boundry:
            imagee = cv2.imread(input_image3)
            imagee = cv2.cvtColor(imagee, cv2.COLOR_RGB2BGR)
            imagee = cv2.resize(imagee, (200,200))
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")

            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(imagee, lower, upper)
            output = cv2.bitwise_and(imagee, imagee, mask = mask)
            ret,thresh1 = cv2.threshold(output,1,1,cv2.THRESH_BINARY)
#             imshow(output)
#             show()
            summation = thresh1.sum().sum()
            if(summation > 10 and summation > current_largest):
                print(lower)
                print(upper)
                piece = name
                current_largest = summation
                # imshow(output)
                # show()
    for boundry, name in possible_color:
        for (lower, upper) in boundry:
            imagee = cv2.imread(input_image3)
            imagee = cv2.cvtColor(imagee, cv2.COLOR_RGB2BGR)
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")

            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(imagee, lower, upper)
            output = cv2.bitwise_and(imagee, imagee, mask = mask)
            ret,thresh1 = cv2.threshold(output,1,1,cv2.THRESH_BINARY)
            summation = thresh1.sum().sum()
            if(summation > 400):
                colour = 'black'
                # imshow(output)
                # show()
    
    test_image = image.img_to_array(test_image)*(1./255)
    test_image = np.expand_dims(test_image, axis = 0)
    color_prediction = color.predict(test_image, batch_size = 32)
    if(np.argmax(color_prediction) == 1 and not piece):
        return "BLANK"
    else:
        if(not piece):
            return "BLANK"
        else:
            if(colour == 'black'):
                return ['black', piece]
            else:
                return ['white', piece]
 
def breakdown_image(image):
    im = Image.open(image)
    im = im.resize((700,700))
    final_piece_mapping = {}

    def crop(im):
        imgwidth, imgheight = im.size
        imgwidth, imgheight = int(imgwidth), int(imgheight)
        height, width = imgheight/8, imgwidth/8
        count = 0
        #print(np.linspace(0,imgheight,9))
        #print("IMGWIDTH: {}\t IMGHEIGHT: {}\t WIDTH: {}\tHEIGHT: {}".format(imgwidth, imgheight, width, height))

        for i in np.linspace(0,imgheight,9):
            if(i == 700):
                break
            for j in np.linspace(0,imgwidth,9):
                if(j == 700):
                    break
                #print("{}\t{}\t{}\t{}".format(j, i, j+width, i+height))
                box = (j, i, j+width, i+height)
                pass_in = np.array(im.crop(box))

                cv2.imwrite('intermediate.png', cv2.cvtColor(pass_in, cv2.COLOR_RGB2BGR))
                result = find_closest_letter('intermediate.png')
                if(result == 'BLANK'):
                    print("LOCATION: {} PIECE: {}".format(total_squares[count],'Blank'))
                elif(result[0] == 'black'):
                    print("LOCATION: {} PIECE: {}".format(total_squares[count], 'black '+result[1]))
                    piece = result[1]
                    if(piece == 'pawn'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.PAWN,chess.BLACK)
                    elif(piece == 'bishop'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.BISHOP,chess.BLACK)
                    elif(piece == 'queen'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.QUEEN,chess.BLACK)
                    elif(piece == 'king'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.KING,chess.BLACK)
                    elif(piece == 'knight'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.KNIGHT,chess.BLACK)
                    elif(piece == 'rook'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.ROOK,chess.BLACK)
                elif(result[0] == 'white'):
                    print("LOCATION: {} PIECE: {}".format(total_squares[count], 'white '+result[1]))
                    piece = result[1]
                    if(piece == 'pawn'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.PAWN,chess.WHITE)
                    elif(piece == 'bishop'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.BISHOP,chess.WHITE)
                    elif(piece == 'queen'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.QUEEN,chess.WHITE)
                    elif(piece == 'king'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.KING,chess.WHITE)
                    elif(piece == 'knight'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.KNIGHT,chess.WHITE)
                    elif(piece == 'rook'):
                        final_piece_mapping[total_squares[count]] = chess.Piece(chess.ROOK,chess.WHITE)
                count += 1
    crop(im)
    return final_piece_mapping

def identify_pieces_on_board():

    # fig = plt.figure(figsize=(50, 50))  # width, height in inches


    try:
        final_piece_mapping = breakdown_image('board.jpg')
    except:
        return False
    board = chess.Board()
    board.set_piece_map(final_piece_mapping)
    print(board)
    return board, final_piece_mapping



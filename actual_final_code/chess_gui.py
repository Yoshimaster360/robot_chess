#! /usr/bin/env python

"""
This module is the execution point of the chess GUI application.
"""

import sys

import chess
from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtSvg import QSvgWidget
#from PyQt4.QtWidgets import QApplication
from PyQt4.QtGui import QWidget, QApplication

piece_name_index = {}
for i,v in zip(['pawn','knight','bishop','rook','queen','king', 'blank'], [1,2,3,4,5,6, None]):
    piece_name_index[i] = v

class MainWindow(QWidget):
    """
    Create a surface for the chessboard.
    """
    def __init__(self, board_configuration=None):
        """
        Initialize the chessboard.
        """
        super().__init__()

        self.setWindowTitle("Chess GUI")
        self.setGeometry(300, 300, 800, 800)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 600, 600)

        self.boardSize = min(self.widgetSvg.width(),
                             self.widgetSvg.height())
        self.coordinates = True
        self.margin = 0.05 * self.boardSize if self.coordinates else 0
        self.squareSize = (self.boardSize - 2 * self.margin) / 8.0
        self.pieceToMove = [None, None]
        self.pieceToInsert = [None, None]
        self.board = chess.Board()
        if(board_configuration):
            self.board.set_piece_map(board_configuration)
        self.drawBoard()


    @pyqtSlot(QWidget)
    def mousePressEvent(self, event):
        """
        Handle left mouse clicks and enable moving chess pieces by
        clicking on a chess piece and then the target square.

        Moves must be made according to the rules of chess because
        illegal moves are suppressed.
        """
        if event.x() <= self.boardSize and event.y() <= self.boardSize:
            # if event.buttons() == Qt.RightButton:
            if self.margin < event.x() < self.boardSize - self.margin and self.margin < event.y() < self.boardSize - self.margin:
                file = int((event.x() - self.margin) / self.squareSize)
                rank = 7 - int((event.y() - self.margin) / self.squareSize)
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                coordinates = "{}{}".format(chr(file + 97), str(rank + 1))
                if self.pieceToInsert[0] is not None and self.pieceToInsert[1] is not None:
                    print("INSERTING.....")
                    self.board.set_piece_at(square, chess.Piece(self.pieceToInsert[0], self.pieceToInsert[1]))
                    self.pieceToInsert = [None, None]
                elif self.pieceToMove[0] is not None:
                    #move = chess.Move.from_uci("{}{}".format(self.pieceToMove[1], coordinates))
                    # if move in self.board.legal_moves:
                    self.board.set_piece_at(square, self.pieceToMove[0])
                    self.board.set_piece_at(self.pieceToMove[1], None)
                    # self.board.push(move)
                    piece = None
                    coordinates = None
                
                self.pieceToMove = [piece, square]
                self.drawBoard()

    @pyqtSlot(QWidget)
    def keyPressEvent(self, event):
        """
        Handle left mouse clicks and enable moving chess pieces by
        clicking on a chess piece and then the target square.

        Moves must be made according to the rules of chess because
        illegal moves are suppressed.
        """
        pressed = event.key()
        print(pressed)
        if(pressed == 81):
            print("You want to insert a queen -- press q")
            self.pieceToInsert[0] = piece_name_index['queen']
        elif(pressed == 75):
            print("You want to insert a king -- press k")
            self.pieceToInsert[0] = piece_name_index['king']
        elif(pressed == 78):
            print("You want to insert a knight -- press n")
            self.pieceToInsert[0] = piece_name_index['knight']
        elif(pressed == 80):
            print("You want to insert a pawn -- press p")
            self.pieceToInsert[0] = piece_name_index['pawn']
        elif(pressed == 66):
            print("You want to insert a bishop -- press b")
            self.pieceToInsert[0] = piece_name_index['bishop']
        elif(pressed == 82):
            print("You want to insert a rook -- press r")
            self.pieceToInsert[0] = piece_name_index['rook']
        elif(pressed == 49):
            print("You want white")
            if(self.pieceToInsert[0]):
                self.pieceToInsert[1] = True
        elif(pressed == 48):
            print("You want black")
            if(self.pieceToInsert[0]):
                self.pieceToInsert[1] = False
        elif(pressed == 16777220):
            print("You are finished with the GUI")
            self.close()

    def drawBoard(self):
        global analyzed_board
        """
        Draw a chessboard with the starting position and then redraw
        it for every new move.
        """
        self.boardSvg = self.board._repr_svg_().encode("UTF-8")
        self.drawBoardSvg = self.widgetSvg.load(self.boardSvg)
        analyzed_board = self.board.copy()
        return self.drawBoardSvg

    def show(self):
        super().show()
        return self.board
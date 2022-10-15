from board.board import Board
from board_description import board_description
import random

# Dice rolls
ROLLS = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]

def main():
	# Create the game board
	board = Board(board_description, ROLLS)

	# Draw the network
	board.draw_network()

main()


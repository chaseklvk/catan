from board.tile import Tile
from board.space import Space
from board.board import Board
from board_description import board_description
import random

# Resources

# Spaces
NUM_SPACES = 54

# Dice rolls
ROLLS = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]

def create_tiles():

	tiles = []
	tile_id = 1
	for biome in board_description:
		print(f"Generating {biome['type'].upper()} Tiles")

		for i in range(biome['num_tiles']):
			# Create a new tile
			tile = Tile(tile_id, biome['type'], biome['resource'], ROLLS.pop())

			# Add the tile to the list of game tiles
			tiles.append(tile)
			
			tile_id += 1
			print(tile)

	# Create the desert tile
	tiles.append(Tile(0, "desert", "nothing", 7))

	# Make sure we have the right number of tiles
	assert(len(tiles) == 19)

	return tiles

def main():
	# Shuffle the list of dice rolls
	random.shuffle(ROLLS)

	# Create the game tiles
	tiles = create_tiles()

	# Create the game board
	board = Board(tiles)

	# Connect the tiles
	board.tile_graph()

	# Draw network
	board.draw_tile_network()




main()


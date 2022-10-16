import random
import os
from pyvis.network import Network

from .tile import Tile

class Board:
	def __init__(self, board_description, dice_rolls):
		# Shuffle dice rolls
		random.shuffle(dice_rolls)

		self._game_tiles = []
		self._game_tiles.append(Tile(0, "desert", "nothing", 7))
		tile_id = 1
		for biome in board_description:
			print(f"Generating {biome['type'].upper()} Tiles")

			for i in range(biome['num_tiles']):
				# Create tiles
				self._game_tiles.append(Tile(tile_id, biome['type'], biome['resource'], dice_rolls.pop()))
				tile_id += 1
		
		# Must have >= 7 tiles and in multiples of 6
		assert(len(self._game_tiles) >= 7 and len(self._game_tiles) % 6 == 1)

		# Connect tiles
		self._game_tiles[0].connect_tile(self._game_tiles[1])
		self._game_tiles[0].connect_tile(self._game_tiles[2])
		self._game_tiles[0].connect_tile(self._game_tiles[3])
		self._game_tiles[0].connect_tile(self._game_tiles[4])
		self._game_tiles[0].connect_tile(self._game_tiles[5])
		self._game_tiles[0].connect_tile(self._game_tiles[6])

	def draw_network(self):
		net = Network()

		space_id_to_int = lambda x: (int(str(x)[0]) * 6) + int(str(x)[1])

		node_set = set()
		for tile in self._game_tiles:
			for node in tile.ring():
				int_id = space_id_to_int(node.space_id())
				if int_id not in node_set:
					node_set.add(int_id)
					net.add_node(int_id, label=node.space_id())

		for tile in self._game_tiles:
			for node in tile.ring():
				node_int_id = space_id_to_int(node.space_id())
				for neighbor in node.neighbors():
					neighbor_int_id = space_id_to_int(neighbor.space_id())
					net.add_edge(node_int_id, neighbor_int_id)

		if not os.path.exists('./out'):
			os.makedirs('./out')

		net.show('out/board.html')




		
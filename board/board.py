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

		# Connect tiles (inner ring)
		self._game_tiles[0].connect_tile(self._game_tiles[1])
		self._game_tiles[0].connect_tile(self._game_tiles[2])
		self._game_tiles[0].connect_tile(self._game_tiles[3])
		self._game_tiles[0].connect_tile(self._game_tiles[4])
		self._game_tiles[0].connect_tile(self._game_tiles[5])
		self._game_tiles[0].connect_tile(self._game_tiles[6])

		# Connect tiles (outer ring)
		self._game_tiles[1].connect_tile(self._game_tiles[7])
		self._game_tiles[1].connect_tile(self._game_tiles[8])
		self._game_tiles[1].connect_tile(self._game_tiles[9])
		self._game_tiles[2].connect_tile(self._game_tiles[10])
		self._game_tiles[2].connect_tile(self._game_tiles[11])
		self._game_tiles[3].connect_tile(self._game_tiles[12])
		self._game_tiles[3].connect_tile(self._game_tiles[13])
		self._game_tiles[4].connect_tile(self._game_tiles[14])
		self._game_tiles[4].connect_tile(self._game_tiles[15])
		self._game_tiles[5].connect_tile(self._game_tiles[16])
		self._game_tiles[5].connect_tile(self._game_tiles[17])
		self._game_tiles[6].connect_tile(self._game_tiles[18])

		for tile in self._game_tiles: print(tile)

	def draw_network(self):
		net = Network(height="100vh")

		def space_id_to_int(x):
			if len(x) == 2:
				return (int(str(x)[0]) * 6) + int(str(x)[1])
			elif len(x) == 3:
				return (int(str(x)[0:2]) * 6) + int(str(x)[2])

		node_set = set()
		for tile in self._game_tiles:
			for node in tile.ring():
				int_id = space_id_to_int(node.space_id())
				if int_id not in node_set:
					print(node)
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




		
import random
import networkx as nx
import matplotlib.pyplot as plt
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
		G = nx.Graph()

		# Get all the edges
		edge_set = set()

		for tile in self._game_tiles:
			for node in tile.ring():
				for neighbor in node.neighbors():
					edge_set.add((node.space_id(), neighbor.space_id()))

		print(f"Number of edges: {len(edge_set)}")

		for edge in edge_set:
			G.add_edge(edge[0], edge[1])

		subax1 = plt.subplot(121)
		nx.draw(G, with_labels=True, font_weight='bold')

		plt.show()




		
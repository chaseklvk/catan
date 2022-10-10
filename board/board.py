import random
import networkx as nx
import matplotlib.pyplot as plt

class Board:
	def __init__(self, tiles):
		# Tiles represents the connected tiles
		self._tiles = []

		# Unconnected tiles represent tiles that have not been connected
		self._unconnected_tiles = tiles
	
	def num_rings(self):
		i = 0
		total_tiles = len(self._unconnected_tiles) - 1
		while (total_tiles > 0):
			total_tiles -= 6 * i
			i += 1
		
		return i

	def next_open_tile(self):
		# Next open tile is the tile with
		# least amount of open spaces not full
		least_tile = None
		least_spaces = -1
		for tile in self._tiles:
			# Don't consider filled tiles
			if (tile.open_sides() == 0): continue

			if (tile.open_sides() < least_spaces or least_spaces == -1):
				least_spaces = tile.open_sides()
				least_tile = tile
		
		return least_tile

	# NOTE: Graph connection scheme might not be fully correct
	# Sometimes graph drawing produces a bad image... not sure if its
	# the algorithm or the visualization tool
	def tile_graph(self):
		# Start with the desert tile, which should be last
		desert_tile = self._unconnected_tiles.pop()
		assert(desert_tile.biome() == "desert")
		self._tiles.append(desert_tile)

		# Shuffle the remaining tiles
		random.shuffle(self._unconnected_tiles)

		# Compute number of rings
		num_rings = self.num_rings()

		for ring in range(num_rings):
			print(f"Connecting ring {ring}")

			# Do nothing for first ring, basically just the desert
			if ring == 0: continue

			# Number of tiles to connect in this ring
			num_tiles_to_connect = 6 * ring

			# If we're on the first ring, we just connect all tiles to the desert
			next_tiles = []
			if ring == 1:
				for i in range(num_tiles_to_connect):
					tile = self._unconnected_tiles.pop()
					next_tiles.append(tile)
					
					print(f"Connecting {tile.tile_id()}")

					# Select the next open tile (which should be the desert tile)
					open_tile = self.next_open_tile()
					assert(open_tile == desert_tile)

					# If we have less than 6 open sides,
					# the next neighbor is also the neighbor of the 
					# last connected tile
					if open_tile.open_sides() < 6:
						open_tile.last_neighbor().add_neighbor(tile)
						tile.add_neighbor(open_tile.last_neighbor())
					
					# If we're adding the last tile, i.e. exactly 1 open
					# sides, then this tile must also be connected with the 
					# first tile to close the ring.
					if open_tile.open_sides() == 1:
						open_tile.first_neighbor().add_neighbor(tile)
						tile.add_neighbor(open_tile.first_neighbor())

					open_tile.add_neighbor(tile)
					tile.add_neighbor(open_tile)
				
			else:

				first_ring_tile = None
				second_to_last_ring_tile = None
				i = 0
				while (i < num_tiles_to_connect):
					# Select the next open tile (one with least open spaces)
					open_tile = self.next_open_tile()

					# Select the first and last tile of open tile
					sorted_neighbors = open_tile.neighbors(sort=True)
					first_tile = sorted_neighbors[0]
					last_tile = sorted_neighbors[1]

					if i == 0:
						# This is the first tile of the ring, take 3 tiles
						tiles = [self._unconnected_tiles.pop() for _ in range(3)]
						next_tiles.extend(tiles)

						# Set the first tile in the ring
						first_ring_tile = tiles[0]

						# Connect the tiles in a chain
						tiles[0].add_neighbor(tiles[1])
						tiles[1].add_neighbor(tiles[0])

						tiles[1].add_neighbor(tiles[2])
						tiles[2].add_neighbor(tiles[1])

						# Connect chain to the open tile
						open_tile.add_neighbor(tiles[0])
						tiles[0].add_neighbor(open_tile)
						
						open_tile.add_neighbor(tiles[1])
						tiles[1].add_neighbor(open_tile)

						open_tile.add_neighbor(tiles[2])
						tiles[2].add_neighbor(open_tile)

						# Connect the chain to the neighbors
						last_tile.add_neighbor(tiles[0])
						tiles[0].add_neighbor(last_tile)

						first_tile.add_neighbor(tiles[2])
						tiles[2].add_neighbor(first_tile)

						i += 3
					elif i > 1 and i < num_tiles_to_connect - 1:
						# Else, only pick 2 tiles
						tiles = [self._unconnected_tiles.pop() for _ in range(2)]
						next_tiles.extend(tiles)

						# Connect the tiles in a chain
						tiles[0].add_neighbor(tiles[1])
						tiles[1].add_neighbor(tiles[0])

						# Connect chain to open tile
						tiles[0].add_neighbor(open_tile)
						open_tile.add_neighbor(tiles[0])

						tiles[1].add_neighbor(open_tile)
						open_tile.add_neighbor(tiles[1])

						# Connect chain to the neighbors
						last_tile.add_neighbor(tiles[0])
						tiles[0].add_neighbor(last_tile)

						first_tile.add_neighbor(tiles[1])
						tiles[1].add_neighbor(first_tile)

						# Update the last tile in the ring
						second_to_last_ring_tile = tiles[1]

						i += 2
					else:
						last_tile = self._unconnected_tiles.pop()
						next_tiles.append(last_tile)

						# Connect last tile to open tile
						last_tile.add_neighbor(open_tile)
						open_tile.add_neighbor(last_tile)

						# Connect last tile with first 
						# in the ring and last in the ring
						first_ring_tile.add_neighbor(last_tile)
						last_tile.add_neighbor(first_ring_tile)

						second_to_last_ring_tile.add_neighbor(last_tile)
						last_tile.add_neighbor(second_to_last_ring_tile)

						i += 1

			self._tiles.extend(next_tiles)

	def draw_tile_network(self):
		G = nx.Graph()

		# Get all the edges
		edge_set = set()
		for tile in self._tiles:
			for neighbor in tile.neighbors():
				edge_set.add((tile.tile_id(), neighbor.tile_id()))

		print(f"Number of edges: {len(edge_set)}")

		for edge in edge_set:
			G.add_edge(edge[0], edge[1])

		subax1 = plt.subplot(121)
		nx.draw(G, with_labels=True, font_weight='bold')

		plt.show()




		
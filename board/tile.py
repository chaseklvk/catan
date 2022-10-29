from .space import Space

"""
Class representing a single tile on the board.
Tiles consist of a ring of spaces
"""
class Tile:
	def __init__(self, tile_id, biome, resource, roll):
		self._tile_id = tile_id
		self._biome = biome
		self._resource = resource
		self._roll = roll
		self._closed_sides = 0

		# Construct the tile ring
		self._ring = []
		
		start_space = Space(f"{tile_id}{0}", self)
		self._ring.append(start_space)
		current_space = start_space
		for i in range(5):
			next_space = Space(f"{tile_id}{i + 1}", self)
			self._ring.append(next_space)

			current_space.add_neighbor(next_space)
			next_space.add_neighbor(current_space)

			current_space = next_space
		
		# Connect the final to the estart
		current_space.add_neighbor(start_space)
		start_space.add_neighbor(current_space)
	
	def tile_id(self):
		return self._tile_id

	def ring(self):
		return self._ring
	
	def next_open_side(self):
		start_index = self._closed_sides % 6 
		end_index = (self._closed_sides + 1) % 6

		return (start_index, self._ring[start_index]), (end_index, self._ring[end_index])

	def set_space(self, space, i):
		self._ring[i] = space

	def connect_tile(self, tile):
		# Select the next open side
		(this_start_index, this_start), (this_end_index, this_end) = self.next_open_side()
		(other_start_index, other_start), (other_end_index, other_end) = tile.next_open_side()
		
		# Connect the sides by consolidating the spaces
		# and drawing the right edges... done by:
		# 1. Set the neighbors of the other side to be the neighbors of this side (except the other spaces themselves)
		# 2. Set the spaces of this side to the correct index in the other side's array
		# 3. Check for nodes with 4 edges and consolidate them

		# 1
		for osn in other_start.neighbors():
			if osn != other_end and (osn not in this_start.neighbors()):
				this_start.add_neighbor(osn)
				osn.add_neighbor(this_start)
		
		for osn in other_end.neighbors():
			if osn != other_start and (osn not in this_end.neighbors()):
				this_end.add_neighbor(osn)
				osn.add_neighbor(this_end)

		# Isolate spaces
		other_start.isolate()
		other_end.isolate()

		# 2
		tile.set_space(this_start, other_start_index)
		tile.set_space(this_end, other_end_index)

		# 3
		this_start.reduce_edges()
		this_end.reduce_edges()

		# We've closed a side
		self.close_side()
		tile.close_side()
	
	def close_side(self):
		self._closed_sides += 1

	def __repr__(self):
		return self.tile_id()

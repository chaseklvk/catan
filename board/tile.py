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
		
		start_space = Space(f"{tile_id}{0}")
		self._ring.append(start_space)
		current_space = start_space
		for i in range(5):
			next_space = Space(f"{tile_id}{i + 1}")
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
		return (self._closed_sides % 6, (self._closed_sides + 1) % 6)
	
	def space_at_index(self, i):
		return self._ring[i]

	def set_space(self, space, i):
		self._ring[i] = space

	def isolate_space(self, space_to_remove):
		# Removes space from all neighbors' lists
		# Effectively isolating it from the graph
		for neighbor in space_to_remove.neighbors():
			neighbor.neighbors().remove(space_to_remove)

	def connect_tile(self, tile):
		# Select the next open side
		this_open_side = self.next_open_side()
		other_open_side = tile.next_open_side()

		# Connect the sides by consolidating the spaces
		# and drawing the right edges... done by:
		# 1. Set the neighbors of the other side to be the neighbors of this side (except the other spaces themselves)
		# 2. Set the spaces of this side to the correct index in the other side's array

		# 1
		other_start = tile.space_at_index(other_open_side[0])
		other_end = tile.space_at_index(other_open_side[1])

		for osn in other_start.neighbors():
			if osn != other_end:
				self.space_at_index(this_open_side[0]).add_neighbor(osn)
				osn.add_neighbor(self.space_at_index(this_open_side[0]))
		
		for osn in other_end.neighbors():
			if osn != other_start:
				self.space_at_index(this_open_side[1]).add_neighbor(osn)
				osn.add_neighbor(self.space_at_index(this_open_side[1]))

		# Isolate spaces
		tile.isolate_space(other_start)
		tile.isolate_space(other_end)

		# 2
		tile.set_space(self.space_at_index(this_open_side[0]), other_open_side[0])
		tile.set_space(self.space_at_index(this_open_side[1]), other_open_side[1])

		# We've closed a side
		self._closed_sides += 1
		tile._closed_sides += 1
	
	def __repr__(self):
		return self.tile_id()

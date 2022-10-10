from .space import Space
from .edge import Edge
# Class representing a resource board tile

class Tile:

	def __init__(self, tile_id, biome, resource, roll):
		self._tile_id = tile_id
		self._biome = biome 
		self._resource = resource
		self._roll = roll
		self._neighbors = []
		self._open_sides = 6
	
	def add_space(self, space):
		self._spaces.append(space)
	
	def add_neighbor(self, tile):
		self._neighbors.append(tile)

		# Reduce number of open sides
		self._open_sides -= 1

	def last_neighbor(self):
		return self._neighbors[-1]

	def first_neighbor(self):
		return self._neighbors[0]
	
	def tile_id(self):
		return self._tile_id

	def resource(self):
		return self._resource
	
	def biome(self):
		return self._biome
	
	def roll(self):
		return self._roll
	
	def open_sides(self):
		return self._open_sides
	
	def neighbors(self, sort=False):
		if sort:
			return sorted(self._neighbors, key=lambda tile: len(tile._neighbors))
		
		return self._neighbors

	def __repr__(self):
		return f"{self._biome.upper()} tile producing {self._resource.upper()} ({self._roll})"

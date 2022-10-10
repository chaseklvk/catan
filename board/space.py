# Class representing a space on the board
class Space:
	def __init__(self, space_id, tiles):
		self._space_id = space_id
		self._tiles = tiles
		self._neighbors = []
		self._roads = []
		self._settlement = False
		self._city = False
		self._player = None
	
	def add_tile(self, tile):
		self._tiles.append(tile)
	
	def add_neighbor(self, space):
		self._neighbors.append(space)
	
	def has_resource(self, resouce):
		for tile in self._tiles:
			if tile._resource == resource:
				return True
	
	def all_resouces(self):
		resources = []
		for tile in self._tiles:
			resources.append(tile._resource)
		return resources

	def has_settlement(self):
		return self._settlement

	def has_city(self):
		return self._city
	
	def player(self):
		return self._player

	def __repr__(self):
		return f"{self._space_id}"


class Edge:
	def __init__(self, space1, space2):
		self._space1 = space1
		self._space2 = space2
		self._road = False
		self._player = None
	
	def has_road(self):
		return self._road
	
	def player(self):
		return self._player
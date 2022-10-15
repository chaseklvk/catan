"""
Class representing a single node in the graph
"""
class Space:
	def __init__(self, space_id):
		self._space_id = space_id
		self._neighbors = []
	
	def add_neighbor(self, node):
		self._neighbors.append(node)
	
	def neighbors(self):
		return self._neighbors

	def space_id(self):
		return self._space_id
	
	def __repr__(self):
		return self.space_id()
"""
Class representing a single node in the graph
"""

# TODO: How do we manage keeping track of tiles associated with each space?
class Space:
	def __init__(self, space_id, origin_tile):
		self._space_id = space_id
		self._neighbors = []
		self._current_tile = origin_tile
	
	def add_neighbor(self, node):
		self._neighbors.append(node)
	
	def reduce_edges(self):
		'''
		Check for neighbor list of size 4, if found reduce to 3 by combining
		the two neighbors with the least edges
		'''
		if self.num_neighbors() <= 3: return

		# Find the two neighbors with the least edges
		two_edge_neighbors = []
		for neighbor in self._neighbors:
			if neighbor.num_neighbors() == 2: 
				two_edge_neighbors.append(neighbor)

		# Combine two-edge neighbors into a single node
		node_1 = two_edge_neighbors.pop()
		node_2 = two_edge_neighbors.pop()

		for osn in node_2.neighbors():
			if osn != node_1 and (osn not in self.neighbors()):
				node_1.add_neighbor(osn)
				osn.add_neighbor(node_1)
		
		node_2.isolate()

		node_2.current_tile().set_space(node_1, node_2.current_tile().ring().index(node_2))

		# Close side on node 1's tile
		node_1.current_tile().close_side()
		node_2.current_tile().close_side()

	
	def isolate(self):
		# Removes space from all neighbors' lists
		# Effectively isolating it from the graph
		for neighbor in self.neighbors():
			neighbor.neighbors().remove(self)

	def current_tile(self):
		return self._current_tile
	
	def set_tile(self, tile):
		self._current_tile = tile

	def neighbors(self):
		return self._neighbors

	def num_neighbors(self):
		return len(self._neighbors)

	def space_id(self):
		return self._space_id
	
	def __repr__(self):
		return self.space_id()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Graph(object):
	#------------------------- nested Vertex class -------------------------
	class Vertex(object):
		'''Lightweight vertex structure of a graph.'''
		__slots__ = '_element'
		
		def __init__(self,x):
			'''Do not call constrctor directly. Use Graph's insert_vertex(x).'''
			self._element = x
		
		def element(self):
			'''Return element associated with this vertex.'''
			return self._element
		
		def __hash__(self):
			return hash(id(self))

	#------------------------- nested Edge class -------------------------
	class Edge(Vertex):
		'''Lightweight edge structure for a graph.'''
		__slots__ = '_origin', '_destination', '_element'
		
		def __init__(self, u, v, x):
			'''Do not call constructor diectly. Use Graph's insert_edge(u, v, x).'''
			self._origin = u
			self._destination = v
			self._element = x
		
		def endpoints(self):
			'''Return (u, v) tuple for vertices u and v.'''
			return (self._origin, self._destination)
		
		def opposite(self, v):
			'''Return the vertex that is opposite v on this edge.'''
			return self._destination if v is self._origin else self._origin
		
		def element(self):
			'''Return element associated with this edge.'''
			return self._element
		
		def __hash__(self):
			return hash((self._origin, self._destination))

	'''Representation of a simple graph using an adjacency map.'''
	def __init__(self, directed=False):
		'''Create an empty graph (undirected, by default).
		Graph is dirceted if optional paramter is set to True.
		'''
		self._outgoing = {}
		self._incoming = {} if directed else self._outgoing

	def is_directed(self):
		'''Return True if this is a dircted graph: False if undirected.
		Property is based on the original declaration of the graph, not its contents.
		'''
		return True if self._incoming is not self._outgoing else False

	def vertex_count(self):
		'''Return the number of vertices in the graph.'''
		return len(self._outgoing)
		
	def vertices(self):
		'''Return an iteration of all vertices of the graph.'''
		return self._outgoing.keys() 

	def edges_count(self):
		'''Return the number of edges in the graph.'''
		total = sum(len(self._outgoing[v]) for v in self._outgoing)
		return total if self.is_directed() else total // 2

	def edges(self):
		'''Return a set of all edges of the graph.'''
		result = set()
		for secondary_map in self._outgoing.values():
			result.update(secondary_map.values())
		return result

	def get_edge(self, u, v):
		'''Return the edge from u to v, or None if not adjacent.'''
		return self._outgoing[u].get(v)

	def degree(self, v, outgoing=True):
		'''Return number of (outgoing) edges incident to vertex v in the graph.
		If graph is directed, optional parameter used to count incoming edges.
		'''
		adj = self._outgoing if outgoing else self._incoming
		return len(adj[v])

	def incident_edges(self, v, outgoing=True):
		'''Return all (outgoing) edges incident to vertex v in the graph.
		If graph is directed, optional parameter used to request incoming edges.
		'''
		adj = self._outgoing if outgoing else self._incoming
		for edge in adj[v].values():
			yield edge

	def insert_vertex(self, x=None):
		'''Insert and return a new Vertex with element x.'''
		v = self.Vertex(x)
		self._outgoing[v] = {}
		if self.is_directed():
			self._incoming[v] = {}
		return v

	def insert_edge(self, u, v, x=None):
		'''Insert and return a new Edge from u to v with auxiliary element x.'''
		e = self.Edge(u, v, x)
		self._outgoing[u][v] = e
		self._incoming[v][u] = e

if __name__ == '__main__':
	# not directed
	g = Graph()
	print('is_directed', g.is_directed())
	print('#edge(s):', g.edges_count(), '#vertex(ies):', g.vertex_count())
	prev_v = None  # prev vertex
	for i in range(10):
		v = g.insert_vertex(i)  # vertex
		if prev_v is not None:
			g.insert_edge(v, prev_v, '%s<->%s' % (v.element(), prev_v.element()))  # vertex
		prev_v = v
	print('#edge(s):', g.edges_count(), '#vertex(ies):', g.vertex_count())
	for v in g.vertices():  # vertex
		print('vertex: %s' % v.element())
		for e in g.incident_edges(v):  # edge incident vertex
			print('  Edges: %s' % (e.element()),)

	# directed
	g = Graph(True)
	print('is_directed', g.is_directed())
	prev_v = None  # prev vertex
	for i in range(10):
		v = g.insert_vertex(i)  # vertex
		if prev_v is not None:
			g.insert_edge(v, prev_v, '%s->%s' % (v.element(), prev_v.element()))  # vertex
		prev_v = v
	print('#edge(s):', g.edges_count(), '#vertex(ies):', g.vertex_count())
	for v in g.vertices():  # vertex
		print('vertex: %s' % v.element())
		for e in g.incident_edges(v):  # edge incident vertex
			print('  Edges: %s' % (e.element()),)

import sys

# Check comments on query_conceptnet.cpp

class ConceptNet:
	def __init__(self, filename):
		self.inbonds = {}
		self.outbonds = {}
		self.edge_weights = {}
		self.relations = set()

		with open(filename) as ifp:
			line = ifp.readline()
			while line:
				elem = line.split('\t')

				if (elem[1],elem[0]) in self.outbonds:
					self.outbonds[(elem[1],elem[0])].add(elem[2]);
				else:
					self.outbonds[(elem[1],elem[0])] = {elem[2]};
				if (elem[2],elem[0]) in self.inbonds:
					self.inbonds[(elem[2],elem[0])].add(elem[1]);
				else:
					self.inbonds[(elem[2],elem[0])] = {elem[1]};

				if (elem[1],elem[0],elem[2]) in self.edge_weights:
					self.edge_weights[(elem[1],elem[0],elem[2])].append(float(elem[3]))
				else:
					self.edge_weights[(elem[1],elem[0],elem[2])] = [float(elem[3])]

				self.relations.add(elem[0])

				line = ifp.readline()

	def query_concept(self, concept, outbonds_only = False):
		r = []
		for rel in self.relations:
			if (concept,rel) in self.outbonds:
				for end in self.outbonds[(concept,rel)]:
					for w in self.edge_weights[(concept,rel,end)]:
						r.append((concept,rel,end,w))
			if not outbonds_only:
				if (concept,rel) in self.inbonds:
					for start in self.inbonds[(concept,rel)]:
						if start == concept:
							continue
						for w in self.edge_weights[(start,rel,concept)]:
							r.append((start,rel,concept,w))
		# 3/24/2020 6:47 PM
		#r = sorted(r, key=lambda tup: tup[3], reverse=True)
		return r

	def query_concept_relation(self, concept, relations, outbonds_only = False):
		r = []
		for rel in relations:
			if (concept,rel) in self.outbonds:
				for end in self.outbonds[(concept,rel)]:
					for w in self.edge_weights[(concept,rel,end)]:
						r.append((concept,rel,end,w))
			if not outbonds_only:
				if (concept,rel) in self.inbonds:
					for start in self.inbonds[(concept,rel)]:
						if start == concept:
							continue
						for w in self.edge_weights[(start,rel,concept)]:
							r.append((start,rel,concept,w))
		return r

	def query_edge(self, concept1, concept2):
		r = []
		for rel in self.relations:
			if (concept1,rel,concept2) in self.edge_weights:
				for w in self.edge_weights[(concept1,rel,concept2)]:
					r.append((concept1,rel,concept2,w))
			if (concept2,rel,concept1) in self.edge_weights:
				for w in self.edge_weights[(concept2,rel,concept1)]:
					r.append((concept2,rel,concept1,w))
		# 3/24/2020 6:50 PM
		#r = sorted(r, key=lambda tup: tup[3], reverse=True)
		return r

if __name__ == '__main__':
	if len(sys.argv) != 2:
		#print("Usage: " + sys.argv[0] + " [input_edges.csv]", file=sys.stderr)
		sys.exit(1)

	cnet = ConceptNet(sys.argv[1])

	edges = cnet.query_concept('banana')
	print(len(edges))
	print(edges)

	edges = cnet.query_edge('banana', 'food')
	print(len(edges))
	print(edges)

import matplotlib


def highlight_text(txt):
	return '\033[94m' + txt + '\033[0m'

def underline_text(txt):
	return '\033[4m' + txt + '\033[0m'

##Eulerian Graphs
	##A graph is *eulerian* if there exists a walk that uses every edge exactly once.
	##Equivalent: A graph is eulerian if and only if every node has even degree.
def assess_eulerian(G,hint_level):
	if hint_level==0:
		print(underline_text('Definition:') + ' Ein Graph G ist ' + highlight_text('eulersch') + ' wenn es einen Kantenzug gibt, in dem jede Kante von G genau einmal auftaucht.')
	if hint_level==1:
		print(underline_text('Charakterisierung:') + ' Ein Graph ist genau dann eulersch, wenn jeder Knoten eine gerade Anzahl von Nachbarn hat.')
	if hint_level==2:	##encode maximum hint_level -> when this is reached, print solution
		if G.is_eulerian():
			print('Der Graph ist eulersch.')
		else:
			print('Der Graph ist nicht eulersch.  Es gibt ' + str(len([v for v in G if G.degree(v)%2==1])) + ' Knoten mit ungeradem Grad.')

##Planar Graphs
	##A graph is *planar* if it can be drawn in the plane without any two edges crossing.
	##Equivalent: A graph is planar if it does not have a a subgraph isomorphic to a subdivision of K_3,3 or K_5.
	##Hint: A planar graph with n>2 vertices has at most 3n-6 edges.
def assess_planar(G,hint_level):
	if hint_level==0:
		print(underline_text('Definition:') + ' Ein Graph ist ' + highlight_text('planar') + ' wenn er so in der Ebene gezeichnet werden kann, dass sich keine zwei Kanten überkreuzen.')
	if hint_level==1:
		print(underline_text('Charakterisierung:') + ' Ein Graph ist genau dann planar, wenn er keinen Teilgraphen enthält, der isomorph zu einer Unterteilung des K_5 bzw. K_3,3 ist.')
	if hint_level==2:
		print(underline_text('Hinweis:') + ' Für n>2 gilt: ein planarer Graph mit n Knoten hat höchstens 3n-6 Kanten.')
	if hint_level==3:
		cert = G.is_planar(kuratowski=true)
		if cert[0]:	#the graph is planar
			print('Der Graph ist planar.')
		else:
			n = len(G.vertices())
			e = len(G.edges())
			if n>2 and e>3*n-6:
				print('Der Graph hat ' + str(n) + ' Knoten und ' + str(e) + ' Kanten.  Da ' + str(e) + ' > 3*' + str(n) + '-6 ' + ' = ' + str(3*n-6) + ' gilt, ist der Graph nicht planar.')
			else:
				vertex_colmap = dict()
				vertex_colmap['r'] = cert[1].vertices()
				vertex_colmap['w'] = [v for v in G if v not in cert[1]]
				edge_colmap = dict()
				edge_colmap['red'] = cert[1].edges()
				G.show(method='matplotlib',vertex_colors=vertex_colmap,edge_colors=edge_colmap)
				try:##this might take a while
					cert[1].minor(graphs.CompleteGraph(5))
					print('Der Graph ist nicht planar.  Die Knoten ' + str(cert[1].vertices()) + ' bilden eine Unterteilung des K_5.')
				except ValueError as veK5:
					try:
						cert[1].minor(graphs.CompleteBipartiteGraph(3,3))
						print('Der Graph ist nicht planar.  Die Knoten ' + str(cert[1].vertices()) + ' bilden eine Unterteilung des K_3,3.')
					except ValueError as veK33:
						print('Hmm, das sollte nicht passieren.')

##Bipartite Graphs
	##A graph is *bipartite* if its vertex set can be partitioned into two sets A and B such that no two vertices in A (resp. B) are connected by an edge.
	##Equivalent: A graph is bipartite if and only if its vertices can be colored with two colors so that no two adjacend vertices have the same color.
	##Equivalent: A graph is bipartite if and only if it does not have any cycles of odd length.
def assess_bipartite(G,hint_level):
	if hint_level==0:
		print(underline_text('Definition:') + ' Ein Graph G ist ' + highlight_text('bipartit') + ' wenn man die Knotenmenge V(G) so in zwei disjunkte Teilmengen A und B zerlegen kann, dass es keine Kante {u,v} gibt mit u,v in A bzw. u,v in B.')
	if hint_level==1:
		print(underline_text('Charakterisierung:') + ' Ein Graph ist genau dann bipartit, wenn er 2-färbbar ist.')
	if hint_level==2:
		print(underline_text('Charakterisierung:') + ' Ein Graph ist genau dann bipartit, wenn es keinen Kreis ungerader Länge gibt.')
	if hint_level==3:
		cert = G.is_bipartite(certificate=true)
		if cert[0]:	#the graph is bipartite
			A = [v for v in G if cert[1][v]==0]
			B = [v for v in G if cert[1][v]==1]
			print('Der Graph ist bipartit.  Eine mögliche Zerlegung der Knotenmenge ist A = ' + str(A) + ' und B = ' + str(B) + '.')	#perhaps color vertices in the drawing
			vertex_colmap = dict()
			vertex_colmap['b'] = A
			vertex_colmap['r'] = B
			G.show(method='matplotlib',vertex_colors=vertex_colmap)
		else:
			print('Der Graph ist nicht bipartit.  Die Knoten ' + str(cert[1]) + ' bilden einen Kreis der Länge ' + str(len(cert[1])) + '.')	#perhaps highlight this cycle in the drawing?!
			vertex_colmap = dict()
			vertex_colmap['r'] = cert[1]
			vertex_colmap['w'] = [v for v in G if v not in cert[1]]
			edge_colmap = dict()
			edge_colmap['red'] = [(cert[1][i],cert[1][i+1],None) for i in range(len(cert[1])-1)] + [(cert[1][-1],cert[1][0],None)]
			G.show(method='matplotlib',vertex_colors=vertex_colmap,edge_colors=edge_colmap)

##Prüfer Code

##Connectivity

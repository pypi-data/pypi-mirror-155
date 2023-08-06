import graphsp
from graphsp import *

graph = graphsp.Graph(5, "undirected")
graph.bulk_link([(0, 4, 5), (0, 1, 1), (1, 4, 3),
                 (1, 3, 1), (1, 2, 15), (2, 3, 2), (3, 4, 3)])


fw = FloydWarshall(5, graph)
print(fw.floyd_warshall())

from graphsp import *

n = 5
graph = Graph(5, "undirected")
graph.bulk_link([(0, 4, 5), (0, 1, 1), (1, 4, 3),
                 (1, 3, 1), (1, 2, 15), (2, 3, 2), (3, 4, 3)])


fw = FloydWarshall(n, graph)
print(fw.floyd_warshall())

dfs = DFS(n, graph)
print(dfs.dfs(0))

bfs = BFS(n, graph)
print(bfs.bfs(0))

dj = Dijkstra(n, graph)
print(dj.dijkstra(0))

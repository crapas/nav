import sys
sys.path.append('..')
from lib.weighted_graph import WeightedGraph

# 방향성 그래프 객체를 초기화한다.
graph = WeightedGraph(is_directed=True)

graph.add_edge(0, 1, 80)  # 0 -> 1
graph.add_edge(1, 0, 80)  # 1 -> 0
graph.add_edge(1, 2, 100)  # 1 -> 2
graph.add_edge(2, 1, 100)  # 2 -> 1
graph.add_edge(0, 2, 190)  # 0 -> 2
graph.add_edge(2, 0, 190)  # 2 -> 0
graph.add_edge(2, 3, 50)  # 2 -> 3
graph.add_edge(3, 4, 55)  # 3 -> 4
graph.add_edge(4, 2, 40)  # 4 -> 2
# 그래프를 출력한다.
graph.print_graph()

# graph.remove_vertex(2)
# graph.print_graph()
# graph.remove_vertex(4)
# graph.print_graph()

# graph.remove_edge(2, 3)
# graph.print_graph()
# graph.remove_edge(3, 4)
# graph.print_graph()

graph.remove_edge(1, 2)
graph.print_graph()

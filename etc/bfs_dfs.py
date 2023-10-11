import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad

simple_road = SeoulRoad(False)
simple_road.add_section(1220022800, 1220016500, 1220012000)
simple_road.add_section(1220016500, 1220022800, 1220012100)
simple_road.add_section(1220022800, 1220017700, 1220012600)
simple_road.add_section(1220016500, 1220019400, 1220011100)
simple_road.add_section(1220016500, 1220003700, 1220008600)
simple_road.add_section(1220016500, 1220003500, 1220008200)
simple_road.add_section(1220017700, 1220022800, 1220012700)
simple_road.add_section(1220017700, 1220015300, 1220009400)
simple_road.add_section(1220015300, 1220017700, 1220009500)
simple_road.add_section(1220015300, 1220000300, 1220000500)
simple_road.add_section(1220000300, 1220015300, 1220000600)
simple_road.add_section(1220000300, 1220003700, 1220007500)
simple_road.add_section(1220013900, 1220000300, 1220000400)
simple_road.add_section(1220003500, 1220013900, 1220006800)
simple_road.add_section(1220003700, 1220016500, 1220008700)
simple_road.add_section(1220003700, 1220000300, 1220007400)
simple_road.add_section(1220024700, 1220022800, 1220015000)
simple_road.add_section(1220028000, 1220024700, 1220018200)
simple_road.add_section(1220028000, 1220024100, 1220018400)
simple_road.add_section(1220024100, 1220019400, 1220014000)
simple_road.add_section(1220024100, 1220028000, 1220018500)
simple_road.add_section(1220019400, 1220024100, 1220014100)
simple_road.add_section(1220019400, 1220016500, 1220011000)


start_spot = 1220028000
end_spot = 1220015300


print("---------BFS 탐색 결과-----------")

all_path = simple_road.bfs_find_all_path(start_spot, end_spot)
for path in all_path:
    path_by_spot_name = [simple_road.get_db_spot_name(spot) for spot in path]
    print(path_by_spot_name)

print("---------DFS 탐색 결과-----------")

all_path = simple_road.dfs_find_all_path(
    start_spot, end_spot, path=[start_spot])
for path in all_path:
    path_by_spot_name = [simple_road.get_db_spot_name(spot) for spot in path]
    print(path_by_spot_name)


# import networkx as nx
# import matplotlib.pyplot as plt
# plt.rc("font", family="AppleGothic")

# spot_dict = {}
# spot_dict  1220019400, 영동4교
# spot_dict  1220022800, 개포동역
# spot_dict  1220016500, 개포고교
# spot_dict  1220017700, 경기여고앞
# spot_dict  1220015300, 개포3,4단지
# spot_dict  1220000300, 구룡마을입구
# spot_dict  1220013900, 구룡터널
# spot_dict  1220003500, 구룡초교
# spot_dict  1220003700, 개포시립도서관입구
# spot_dict  1220024700, 영동5교
# spot_dict  1220028000, 대치역
# spot_dict  1220024100, 도곡역

# G = nx.DiGraph()
# G.add_edge(spot_dict[1220022800], spot_dict[1220016500])
# G.add_edge(spot_dict[1220016500], spot_dict[1220022800])
# G.add_edge(spot_dict[1220022800], spot_dict[1220017700])
# G.add_edge(spot_dict[1220016500], spot_dict[1220019400])
# G.add_edge(spot_dict[1220016500], spot_dict[1220003700])
# G.add_edge(spot_dict[1220016500], spot_dict[1220003500])
# G.add_edge(spot_dict[1220017700], spot_dict[1220022800])
# G.add_edge(spot_dict[1220017700], spot_dict[1220015300])
# G.add_edge(spot_dict[1220015300], spot_dict[1220017700])
# G.add_edge(spot_dict[1220015300], spot_dict[1220000300])
# G.add_edge(spot_dict[1220000300], spot_dict[1220015300])
# G.add_edge(spot_dict[1220000300], spot_dict[1220003700])
# G.add_edge(spot_dict[1220013900], spot_dict[1220000300])
# G.add_edge(spot_dict[1220003500], spot_dict[1220013900])
# G.add_edge(spot_dict[1220003700], spot_dict[1220016500])
# G.add_edge(spot_dict[1220003700], spot_dict[1220000300])
# G.add_edge(spot_dict[1220024700], spot_dict[1220022800])
# G.add_edge(spot_dict[1220028000], spot_dict[1220024700])
# G.add_edge(spot_dict[1220028000], spot_dict[1220024100])
# G.add_edge(spot_dict[1220024100], spot_dict[1220019400])
# G.add_edge(spot_dict[1220024100], spot_dict[1220028000])
# G.add_edge(spot_dict[1220019400], spot_dict[1220024100])
# G.add_edge(spot_dict[1220019400], spot_dict[1220016500])
# nx.draw(G, with_labels=True)
# plt.savefig('graph.png')

# 0spot_dict  1220019400, 영동4교
# 1spot_dict  1220022800, 개포동역
# 2spot_dict  1220016500, 개포고교
# 3spot_dict  1220017700, 경기여고앞
# 4spot_dict  1220015300, 개포3,4단지
# 5spot_dict  1220000300, 구룡마을입구
# 6spot_dict  1220013900, 구룡터널
# 7spot_dict  1220003500, 구룡초교
# 8spot_dict  1220003700, 개포시립도서관입구
# 9spot_dict  1220024700, 영동5교
# 10spot_dict  1220028000, 대치역
# 11spot_dict  1220024100, 도곡역

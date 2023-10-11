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
min_path_cost = sys.maxsize
# 같은 경로 비용의 둘 이상의 최단 경로가 존재할 수 있으므로
# 최단 경로를 모두 찾는다.
min_paths = []
for path, path_cost in all_path.items():
    if path_cost < min_path_cost:
        min_path_cost = path_cost
        min_paths = [path]
    elif path_cost == min_path_cost:
        min_paths.append(path)

for min_path in min_paths:
    path_by_spot_name = [
        simple_road.get_db_spot_name(spot) for spot in min_path]
    print(f"최소 경로 : {path_by_spot_name}, 경로 비용 : {min_path_cost}m")

print("---------DFS 탐색 결과-----------")

all_path = simple_road.dfs_find_all_path(start_spot, end_spot)
min_path_cost = sys.maxsize
# 같은 경로 비용의 둘 이상의 최단 경로가 존재할 수 있으므로
# 최단 경로를 모두 찾는다.
min_paths = []
for path, path_cost in all_path.items():
    if path_cost < min_path_cost:
        min_path_cost = path_cost
        min_paths = [path]
    elif path_cost == min_path_cost:
        min_paths.append(path)

for min_path in min_paths:
    path_by_spot_name = [
        simple_road.get_db_spot_name(spot) for spot in min_path]
    print(f"최소 경로 : {path_by_spot_name}, 경로 비용 : {min_path_cost}m")


# all_path = simple_road.dfs_find_all_path(
#     start_spot, end_spot, path=[start_spot])
# for path in all_path:
#     path_by_spot_name = [simple_road.get_db_spot_name(spot) for spot in path]
#     print(path_by_spot_name)

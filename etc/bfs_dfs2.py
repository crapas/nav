import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad

simple_road = SeoulRoad()

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

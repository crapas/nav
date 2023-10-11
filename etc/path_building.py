import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad

seoul_road = SeoulRoad()

# 1220022800(개포동역)으로부터 5개의 구간을 지나 도착하는 모든 지점들의 목록
result_spots = seoul_road.get_neighbors_with_step(1220022800, 4)
# 지점의 목록으로 지점 이름의 목록을 생성
result_spots_with_spot_name = [
    seoul_road.get_db_spot_name(spot) for spot in result_spots]
# 출력
print("-----------------------------------------------")
print("개포동역으로부터 4개의 구간을 지나 도착하는 모든 지점들의 목록")
print("-----------------------------------------------")
print(result_spots_with_spot_name)

# 1220022800(개포동역)에서 시작해 구간이 5개인 모든 경로의 목록
paths = seoul_road.get_paths_with_step(1220022800, 4)
print("------------------------------------------------")
print("개포동역에서 시작하는 4개의 구간으로 이루어진 모든 경로들의 목록")
print("------------------------------------------------")

for path in paths:
    # 지점으로 구성된 경로로 지점 이름으로 구성된 경로를 생성해 출력
    path_by_spot_name = [seoul_road.get_db_spot_name(spot) for spot in path]
    path_cost = seoul_road.validation(path, 'distance')
    print(f"경로 {path_by_spot_name}의 경로비용 : {path_cost}m")

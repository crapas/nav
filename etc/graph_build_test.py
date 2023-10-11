import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad

# 그래프를 구성한다.
seoul_road = SeoulRoad()
# 그래프의 정보를 출력한다.
seoul_road.print_road_info()


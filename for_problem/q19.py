import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad
from psycopg_pool import ConnectionPool
from lib.db_util import *


def find_n_neighbor(graph, current, path, n):
    if n == 0:
        return [path]
    neighbors = []
    for neighbor in graph[current]:
        if neighbor not in path:
            new_path = path + [neighbor]
            neighbors += find_n_neighbor(graph, neighbor, new_path, n - 1)
    return neighbors


db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

# Connection pool에서 connection을 가져온다.
# with 구문을 사용하면 connection을 사용한 후 자동으로 반환한다.
with db_pool.connection() as conn:
    # 그래프를 구성한다.
    seoul_road = SeoulRoad(conn)
    # 그래프의 정보를 출력한다.
    seoul_road.print_road_info()

paths = find_n_neighbor(seoul_road.graph, 1210000700, [1210000700], 10
                        )
for path in paths:
    for spot in path:
        print(spot, get_spot_name(conn, spot), end=' ')
    print()


# Connection Pool을 반환한다.
db_pool.close()

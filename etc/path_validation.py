import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad
from lib.db_util import *
from psycopg_pool import ConnectionPool

db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

# 검증해야 할 경로의 리스트
path_candidates = [[1210000700, 1210002500, 1210002700, 1210003000, 1210003200, 1210018900, 1210024100, 1210028900, 1220006300, 1220006600, 1220029000],
                   [1210000700, 1210002500, 1210002700, 1210003000, 1210003200, 1210018900,
                       1210024100, 1210028900, 1220023900, 1220025900, 1220029000],
                   [1210000700, 1210002500, 1210002700, 1210003000, 1210003200,
                       1210018900, 1210024100, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1210002500, 1210002700, 1210003000, 1210003200,
                    1210018900, 1210020600, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1210002500, 1210002700, 1210003000, 1210019000, 1220003500,
                    1220016400, 1220021100, 1220027600, 1220031100, 1220029000],
                   [1210000700, 1210002500, 1210002700, 1210003000, 1210019000, 1220003500,
                    1220016400, 1220021100, 1220027600, 1220025900, 1220029000],
                   [1210000700, 1210002500, 1210002700, 1210003000, 1210019000,
                    1220003400, 1210020600, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016500, 1220019400,
                    1220024100, 1220029300, 1220027600, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016500, 1220019400,
                    1220024100, 1220029300, 1220027600, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016500, 1220019400,
                    1220024100, 1220029300, 1220007700, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016500, 1220019400,
                    1220024100, 1220021100, 1220027600, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016500, 1220019400,
                    1220024100, 1220021100, 1220027600, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1210019000,
                    1220003400, 1210020600, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400,
                    1220021100, 1220017900, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400, 1220021100,
                    1220027600, 1220029300, 1220007700, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400,
                    1220021100, 1220027600, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400, 1220021100,
                    1220027600, 1220031100, 1220034100, 1220032700, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400,
                    1220021100, 1220027600, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400, 1220021100,
                    1220024100, 1220029300, 1220027600, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400, 1220021100,
                    1220024100, 1220029300, 1220027600, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1220013900, 1220003500, 1220016400, 1220021100,
                    1220024100, 1220029300, 1220007700, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1210003000, 1210003200,
                    1210018900, 1210024100, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1210003000, 1210003200,
                    1210018900, 1210020600, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1220003500, 1220016400,
                    1220021100, 1220017900, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1220003500,
                    1220016400, 1220021100, 1220027600, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1220003500,
                    1220016400, 1220021100, 1220027600, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1220003400, 1210020600,
                    1210018900, 1210024100, 1210026200, 1220025900, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1220003400, 1210020600,
                    1210026200, 1220025900, 1220027600, 1220031100, 1220029000],
                   [1210000700, 1220000100, 1210016400, 1210019000, 1220003400, 1210020600, 1210026200, 1220025900, 1220029000]]

with db_pool.connection() as conn:
    seoul_road = SeoulRoad(conn)
    min_cost = sys.maxsize
    max_cost = 0
    min_cost_path = path_candidates[0]
    max_cost_path = path_candidates[0]
    # 각 경로에 대해
    for path in path_candidates:
        result = seoul_road.validation(conn, path, 'distance')
        if result != None:
            if result < min_cost:
                min_cost = result
                min_cost_path = path
            if result > max_cost:
                max_cost = result
                max_cost_path = path

    # 최단/최장 경로의 각 지점의 이름
    min_path_by_spot_name = [get_spot_name(
        conn, spot) for spot in min_cost_path]
    max_path_by_spot_name = [get_spot_name(
        conn, spot) for spot in max_cost_path]

    print(f"최단 경로 : {min_path_by_spot_name} (총 거리 : {min_cost})")
    print(f"최장 경로 : {max_path_by_spot_name} (총 거리 : {max_cost})")

# Connection Pool을 반환한다.
db_pool.close()
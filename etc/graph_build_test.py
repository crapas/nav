import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad

from psycopg_pool import ConnectionPool

# connection을 필요할 때 생성하는 대신 connection pool을 사용해서
# connection을 생성할 때 발생하는 시스템 부하를 줄인다.
# 항상 min_size(1) 만큼의 connection을 유지하고
# 필요에 따라 max_size(10)개 까지의 connection을 생성한다.
db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

# Connection pool에서 connection을 가져온다.
# with 구문을 사용하면 connection을 사용한 후 자동으로 반환한다.
with db_pool.connection() as conn:
    # 그래프를 구성한다.
    seoul_road = SeoulRoad(conn)
    # 그래프의 정보를 출력한다.
    seoul_road.print_road_info()

# Connection Pool을 반환한다.
db_pool.close()

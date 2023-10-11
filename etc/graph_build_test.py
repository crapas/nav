import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad
from lib.db_util import *
from psycopg_pool import ConnectionPool

# connection을 필요할 때 생성하는 대신 connection pool을 사용해서
# connection을 생성할 때 발생하는 시스템 부하를 줄인다.
# 항상 min_size(1) 만큼의 connection을 유지하고
# 필요에 따라 max_size(10)개 까지의 connection을 생성한다.
db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

paths_for_validation = [
    ['개포동역', '개포고교', '개포시립도서관입구', '구룡마을입구', '구룡터널', '구룡초교',
        '영동3교(남단)', '매봉터널', '강남세브란스', '도곡1동주민센터', '구역삼세무서', '역삼역', '차병원', '구경복아파트', '센터필드', '선릉역', '도성초교', '대치사거리', '포스코사거리', '삼성중앙역'],
    ['개포동역', '개포고교', '개포시립도서관입구', '구룡마을입구', '구룡터널', '구룡사앞', '염곡사거리', '내곡IC', '세곡동사거리', '수서역',
     '가락시장역', '경찰병원', '가락2동주민센터', '오금역', '개롱역', '거여동사거리', '송파소방서', '마천사거리', '거여역', '송파공고앞'],
    ['개포동역', '개포고교', '개포시립도서관입구', '구룡마을입구', '구룡터널', '구룡사앞', '국악고교앞', '신진빌딩', '금호빌딩', '양일초등학교',
     'aT센터', '염곡사거리', '내곡IC', '세곡동사거리', '복정교차로', '복정역', '장지교', '건영아파트앞', '문정역', '문덕초교'],
    ['개포동역', '개포고교', '개포시립도서관입구', '구룡마을입구', '구룡터널', '구룡초교',
     '영동3교(남단)', '매봉터널', '강남세브란스', '한치역', '개나리아파트', '구역삼세무서', '역삼역', '센터필드', '구경복아파트', '선정릉역', '삼성중앙역', '코엑스', '삼성역', '휘문고교']
]

# Connection pool에서 connection을 가져온다.
# with 구문을 사용하면 connection을 사용한 후 자동으로 반환한다.
with db_pool.connection() as conn:
    # 그래프를 구성한다.
    seoul_road = SeoulRoad(conn)
    # 그래프의 정보를 출력한다.
    seoul_road.print_road_info()

    for path_for_validation in paths_for_validation:
        result = 0
        path = []
        for spot_name in path_for_validation:
            spot = get_spot(conn, spot_name)
            if spot == None:
                result = None
                break
            path.append(spot)
        if result != None:
            result = seoul_road.validation(conn, path, 'distance')

        if result != None:
            print(f"{path_for_validation} : 유효한 경로이며, 경로 비용은 {result}입니다.")
        else:
            print(f"{path_for_validation} : 유효하지 않은 경로입니다.")


# Connection Pool을 반환한다.
db_pool.close()

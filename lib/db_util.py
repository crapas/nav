import sys
sys.path.append('..')
import lib.constant
from psycopg_pool import ConnectionPool


# section 테이블에서 구간 정보 목록을 만들어 반환한다.
#   conn : DB 연결 객체
#   Return Value : 구간 정보 목록 또는 None (DB 오류)
def get_all_sections(conn):
    try:
        rows = conn.execute(
            "select id, start_id, end_id from section").fetchall()
    except Exception as e:
        return None
    return rows


def get_sections(conn, start_spot, end_spot):
    try:
        rows = conn.execute(
            f"SELECT id FROM section WHERE start_id = {start_spot} AND end_id = {end_spot}").fetchall()
    except Exception as e:
        return None
    return [row[0] for row in rows]

# 주어진 구간의 거리를 반환한다.
#   conn : DB 연결 객체
#   section : 구간 고유번호
#   Return Value : 구간의 거리 또는 None (DB 오류)


def get_section_distance(conn, section, current_distance=None):
    try:
        rows = conn.execute(
            f"select distance from section where id = {section}").fetchall()
    except Exception as e:
        return None
    # 주어진 구간이 DB에 존재하지 않는 경우
    if len(rows) == 0:
        return None
    return rows[0][0]

# 지점의 이름을 반환한다.
#   conn : DB 연결 객체
#   spot : 지점 고유번호
#   Return Value : 지점의 이름 또는 None (DB 오류)


def get_spot_name(conn, spot):
    try:
        rows = conn.execute(
            f"SELECT name FROM spot WHERE id = {spot}").fetchall()
    except Exception as e:
        return None
    # 주어진 지점이 DB에 존재하지 않는 경우
    if len(rows) == 0:
        return None
    return rows[0][0]


def get_spot_info(conn, spot):
    try:
        rows = conn.execute(
            f"SELECT name, coord_y, coord_x FROM spot WHERE id = {spot}").fetchall()
    except Exception as e:
        return None
    # 주어진 지점이 DB에 존재하지 않는 경우
    if len(rows) == 0:
        return None
    return rows[0]

# 지점의 고유번호를 반환한다.
#   conn : DB 연결 객체
#   spot_name : 지점 이름
#   Return Value : 지점의 고유번호 또는 None (DB 오류)


def get_spots(conn, spot_name):
    try:
        rows = conn.execute(
            f"SELECT id FROM spot WHERE name = '{spot_name}'").fetchall()
    except Exception as e:
        return None
    # 주어진 이름의 지점이 DB에 존재하지 않는 경우
    if len(rows) == 0:
        return []
    return [row[0] for row in rows]


def get_section_time_by_limit(conn, section):
    # 임시로 nav 데이터베이스를 사용한다.
    temp_db_pool = ConnectionPool(
        "dbname=nav host=localhost user=postgres password=1234")

    with temp_db_pool.connection() as temp_conn:
        try:
            max_speed_rows = temp_conn.execute(
                f"SELECT distance, max_speed FROM section WHERE id = {section}").fetchall()
        except Exception as e:
            return None
        if len(max_speed_rows) != 1:
            return None
        distance = max_speed_rows[0][0]
        # change km/h to m/s
        max_speed = max_speed_rows[0][1] / 3.6
        if max_speed == 0:
            return lib.constant.LARGE_WEIGHT
        return distance / max_speed


def get_average_speed_by_hour(conn, section, hour):
    try:
        rows = conn.execute(
            f"SELECT AVG(speed) FROM past_speed WHERE section_id = {section} AND record_hour = {hour}").fetchall()
    except Exception as e:
        return None
    # 주어진 구간이 DB에 존재하지 않는 경우
    if len(rows) == 0:
        return None
    return rows[0][0]


def get_average_speed(conn, section, hour, min):
    current_hour_speed = get_average_speed_by_hour(conn, section, hour)
    next_hour_speed = get_average_speed_by_hour(
        conn, section, (hour + 1) % 24)
    if current_hour_speed is None or next_hour_speed is None:
        return None
    return (current_hour_speed * (60 - min) + next_hour_speed * min) / 60


# 임시
def get_average_speed_wday(conn, section, hour, min):
    current_hour_speed = get_average_speed_by_hour(conn, section, hour)
    next_hour_speed = get_average_speed_by_hour(
        conn, section, (hour + 1) % 24)
    if current_hour_speed is None or next_hour_speed is None:
        return None
    return (current_hour_speed * (60 - min) + next_hour_speed * min) / 60


# 시작 지점과 끝 지점의 ID로 두 구간 사이의 최소 비용을 반환한다.
#   최소 비용, 최소비용 구간
def get_min_cost(conn, start_spot, end_spot, weight_name, path_type, current_cost):
    weight_function = None
    if path_type == 'static':
        if weight_name == 'distance':
            weight_function = get_section_distance
        elif weight_name == 'time_by_limit_speed':
            weight_function = get_section_time_by_limit
        elif weight_name == 'time_by_avg_speed1':
            weight_function = get_average_speed
        elif weight_name == 'time_by_avg_speed2':
            weight_function = get_average_speed_wday
    if weight_function == None:
        return None, None

#        return {'result': False, 'cause': 'weight_name is not valid'}

    # start_spot과 end_spot으로 두 지점 사이의 구간의 목록을 가져온다.
    sections = get_sections(conn, start_spot, end_spot)
    if len(sections) == 0:
        return None, None
#        return {'result': False, 'cause': 'no section between start_spot and end_spot'}
    if sections == None:
        return None, None
#        return {'result': False, 'cause': 'some db error occured'}

    min_section = 0
    min_cost = lib.constant.LARGE_WEIGHT
    for section in sections:
        weight = weight_function(conn, section, current_cost)
        if weight == None:
            weight = lib.constant.LARGE_WEIGHT
        if weight < min_cost:
            min_cost = weight
            min_section = section
    return min_cost, min_section
#    return {'result': True, 'min_cost': min_cost, 'min_section': min_section}

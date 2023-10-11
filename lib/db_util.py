
# section 테이블에서 구간 정보 목록을 만들어 반환한다.
#   conn : DB 연결 객체
#   Return Value : 구간 정보 목록 또는 None (DB 오류)
def get_db_sections(conn):
    try:
        rows = conn.execute(
            "select id, start_id, end_id from section").fetchall()
    except Exception as e:
        return None
    return rows

# 주어진 구간의 거리를 반환한다.
#   conn : DB 연결 객체
#   section : 구간 고유번호
#   Return Value : 구간의 거리 또는 None (DB 오류)


def get_db_section_distance(conn, section):
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


def get_db_spot_name(conn, spot):
    try:
        rows = conn.execute(
            f"SELECT name FROM spot WHERE id = {spot}").fetchall()
    except Exception as e:
        return None
    # 주어진 지점이 DB에 존재하지 않는 경우
    if len(rows) == 0:
        return None
    return rows[0][0]

# 지점의 고유번호를 반환한다.
#   conn : DB 연결 객체
#   spot_name : 지점 이름
#   Return Value : 지점의 고유번호 또는 None (DB 오류)


def get_db_spots(conn, spot_name):
    try:
        rows = conn.execute(
            f"SELECT id FROM spot WHERE name = '{spot_name}'").fetchall()
    except Exception as e:
        return None
    # 주어진 이름의 지점이 DB에 존재하지 않는 경우
    if len(rows) == 0:
        return []
    return [row[0] for row in rows]

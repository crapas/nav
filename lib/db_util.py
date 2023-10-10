
# section 테이블에서 구간 정보 목록을 만들어 반환한다.
#   conn : DB 연결 객체
#   Return Value : 구간 정보 목록 또는 None (DB 오류)
def get_db_sections(conn):
    try:
        rows = conn.execute("select id, start_id, end_id from section").fetchall()
    except Exception as e:
        return None
    return rows


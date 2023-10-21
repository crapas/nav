'''
 CREATE TABLE past_speed_stat (
      id SERIAL PRIMARY KEY,
      section_id BIGINT REFERENCES section(id),
      record_wday INT,
      record_hour INT,
      speed NUMERIC(5, 2)
 );

CREATE UNIQUE INDEX past_speed_idx ON past_speed(id);
CREATE INDEX past_speed_section_id ON past_speed(section_id);
CREATE INDEX past_speed_date_id ON past_speed(record_date);
CREATE INDEX past_speed_hour_idx ON past_speed(record_hour);
'''
# section table에서 id를 가지고 온다.

# 각 section 별로
#   past_speed에 해당 section의 data가 있는지 확인한다. 없으면 continue
#   시간 별로 loop
#    past_speed에서 해당 section, 시간대의 data의 avg를 구한다.
#    이 데이터를 past_speed_stat에 insert 한다. (wday = 7)
#    wday 별로 loop
#     past_speed에서 해당 section, 시간대, wday의 data의 avg를 구한다.
#     이 데이터를 past_speed_stat에 insert 한다. (wday = wday)

from psycopg_pool import ConnectionPool
import random
from time import time

db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

with db_pool.connection() as conn:
    sections = [sample_section[0] for sample_section in conn.execute(
        "SELECT id FROM section order by id asc").fetchall()]
    #    "SELECT id FROM section where id = 1000002900 order by id asc").fetchall()]
    for section in sections:
        print(section)
        data_length_result = conn.execute(
            f"SELECT count(*) FROM past_speed where section_id={section}").fetchall()
        data_length = data_length_result[0][0]
        if data_length == 0:
            print("No data")
            continue
        for h in range(24):
            avg_result = conn.execute(
                f"SELECT avg(speed) FROM past_speed where section_id={section} and record_hour={h}").fetchall()

            average_sampled = avg_result[0][0]
            if average_sampled is None:
                continue
            conn.execute(
                f"insert into past_speed_stat (section_id, record_wday, record_hour, speed) values ({section}, 7, {h}, {average_sampled});")
            for wday in range(7):
                avg_result = conn.execute(
                    f"SELECT avg(speed) FROM past_speed where section_id={section} and record_hour={h} and EXTRACT(DOW FROM TO_DATE(CAST(record_date AS TEXT), 'YYYYMMDD')) = {wday}").fetchall()
                # f"SELECT speed FROM past_speed where section_id={section} and record_hour={h} and EXTRACT(DOW FROM TO_DATE(CAST(record_date A TEXT), 'YYYYMMDD')) = {wday}").fetchall()]

                average_sampled = avg_result[0][0]
                if average_sampled is None:
                    continue
                conn.execute(
                    f"insert into past_speed_stat (section_id, record_wday, record_hour, speed) values ({section}, {wday}, {h}, {average_sampled});")
            print(f"section {section}, hour {h} done")
        print(f"section {section} done")
    conn.commit()
    # conn.rollback()
    print("Commit done")

import pandas as pd
import os
from psycopg_pool import ConnectionPool
import math
'''
    id    | section_id | record_date | record_hour | speed
----------+------------+-------------+-------------+--------
  2711230 | 1010015900 |    20210101 |          16 |  17.86
  2711231 | 1010015900 |    20210101 |          17 |  19.17
Table "public.past_speed"
   Column    |     Type     | Collation | Nullable |                Default
-------------+--------------+-----------+----------+----------------------------------------
 id          | integer      |           | not null | nextval('past_speed_id_seq'::regclass)
 section_id  | bigint       |           |          |
 record_date | integer      |           |          |
 record_hour | integer      |           |          |
 speed       | numeric(5,2) |           |          |
Indexes:
    "past_speed_pkey" PRIMARY KEY, btree (id)
    "past_speed_date_id" btree (record_date)
    "past_speed_hour_idx" btree (record_hour)
    "past_speed_idx" UNIQUE, btree (id)
    "past_speed_section_id" btree (section_id)
Foreign-key constraints:
    "past_speed_section_id_fkey" FOREIGN KEY (section_id) REFERENCES section(id)

 CREATE TABLE past_speed (
      id SERIAL PRIMARY KEY,
      section_id BIGINT REFERENCES section(id),
      record_date INT,
      record_hour INT,
      speed NUMERIC(5, 2)
 );

'''

# id : pk, auto increment
# section_id : 구간 id (Big INT)
# record_date : string (YYYYMMDD)
# record_hour :


def insert_past_speed(conn, file_path):
    print("file into pandas dataframe")
    df = pd.read_excel(file_path)
    print("file into pandas dataframe done")
    num_rows, _ = df.shape
    date_colume_index = 0
    section_id_index = 3
    time_start_index = 12
    i = 0
    for row_index in range(num_rows):
        i += 1
        if i % 1500 == 0:
            print(f"{i}/{num_rows} ({i / num_rows * 100}%) processed ({file_path})")
        date = df.iat[row_index, date_colume_index]
        section_id = df.iat[row_index, section_id_index]
        for h in range(24):
            try:
                speed = float("{:.2f}".format(
                    df.iat[row_index, time_start_index + h]))
                if math.isnan(speed):
                    continue
                with conn.cursor() as cur:
                    cur.execute(
                        f"insert into past_speed (section_id, record_date, record_hour, speed) values ({section_id}, '{date}', {h}, {speed});")
            except Exception as e:
                print(e)
                conn.rollback()
                exit(-1)
    print("Insert data done, so will commit")
    conn.commit()
    print("Commit done")


db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

data_path = '/Users/edbergbak/work/nav/data/past_speed'

# data_path 디렉토리 내의 파일 중 확장자가 xlsx인 파일의 목록을 가져온다.
file_list = [file_name for file_name in os.listdir(
    data_path) if file_name.endswith('.xlsx')]

i = 0
for file_name in file_list:
    i += 1
    print(f"Process file {file_name} ({i}/{len(file_list)})")
    with db_pool.connection() as conn:
        insert_past_speed(conn, os.path.join(data_path, file_name))

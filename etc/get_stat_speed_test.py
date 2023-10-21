import sys
sys.path.append('..')
from lib.db_util import *
from psycopg_pool import ConnectionPool
import datetime

db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

now = datetime.datetime.now()
hour = now.hour
minute = now.minute
with db_pool.connection() as conn:
    print(get_average_speed(conn, 1050018700, hour, minute))
# 1050018700
#    def get_average_speed(conn, section, hour, min):

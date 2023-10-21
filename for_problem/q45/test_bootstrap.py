from psycopg_pool import ConnectionPool
import random
from time import time

db_pool = ConnectionPool(
    "dbname=testdatabase host=localhost user=postgres password=1234", min_size=1, max_size=10)

without_weekday_result = {}
with_weekday_result = {}
all_without_cnt = 0
error_without_cnt = 0
all_with_cnt = 0
error_with_cnt = 0
no_data = False
with db_pool.connection() as conn:
    sections = [sample_section[0] for sample_section in conn.execute(
        "SELECT * FROM section ORDER BY random() LIMIT 5").fetchall()]
    for section in sections:
        for h in range(24):
            print(f"for {section}, {h}")
            sampled_past_speed = [sample_speed[0] for sample_speed in conn.execute(
                f"SELECT speed FROM past_speed where section_id={section} and record_hour={h}").fetchall()]

            data_length = len(sampled_past_speed)
            print(data_length)

            if data_length == 0:
                print("No data")
                no_data = True
                break
            all_without_cnt += 1
            average_sampled = sum(sampled_past_speed) / data_length
            avg_list = []
            for i in range(1000):
                average_resampled = sum(sample for sample in random.choices(
                    sampled_past_speed, k=data_length)) / data_length
                avg_list.append(average_resampled)

            # avg_list를 오름차순 정렬한다.
            avg_list.sort()

            # avg_list에서 average_sampled의 위치를 찾는다.
            index = 0
            for i in range(1000):
                if avg_list[i] < average_sampled:
                    index += 1
                else:
                    break

            lower = avg_list[3]
            upper = avg_list[996]
            if average_resampled < lower or average_resampled > upper:
                error_without_cnt += 1
                print("####################### Outlier!!! #######################")

            print(f"{h}, {lower} - {average_sampled} - {upper}, {index}")
            without_weekday_result[(section, h)] = (lower, upper, index)

            for wday in range(7):
                print(f"for {section}, wday-{wday}, hour-{h}")
                sampled_past_speed = [sample_speed[0] for sample_speed in conn.execute(
                    f"SELECT speed FROM past_speed where section_id={section} and record_hour={h} and EXTRACT(DOW FROM TO_DATE(CAST(record_date AS TEXT), 'YYYYMMDD')) = {wday}").fetchall()]
                data_length = len(sampled_past_speed)
                print(data_length)

                if data_length == 0:
                    print("No data")
                    continue
                all_with_cnt += 1
                average_sampled = sum(sampled_past_speed) / data_length
                avg_list = []
                for i in range(1000):
                    average_resampled = sum(sample for sample in random.choices(
                        sampled_past_speed, k=data_length)) / data_length
                    avg_list.append(average_resampled)

                # avg_list를 오름차순 정렬한다.
                avg_list.sort()

                # avg_list에서 average_sampled의 위치를 찾는다.
                index = 0
                for i in range(1000):
                    if avg_list[i] < average_sampled:
                        index += 1
                    else:
                        break
                lower = avg_list[3]
                upper = avg_list[996]
                if average_resampled < lower or average_resampled > upper:
                    error_with_cnt += 1
                    print("####################### Outlier!!! #######################")
                print(f"{h}, {lower} - {average_sampled} - {upper}, {index}")
                with_weekday_result[(section, wday, h)] = (lower, upper, index)
        if no_data:
            no_data = True
            break
        # print(average_sampled, average_resampled)
# normal range for 95% :
print("------ without weekday")
for key, value in without_weekday_result.items():
    print(key, value)

print("------ with weekday")
for key, value in with_weekday_result.items():
    print(key, value)

print(
    f"all_without_cnt: {all_without_cnt}, error_without_cnt: {error_without_cnt}")
print(f"all_with_cnt: {all_with_cnt}, error_with_cnt: {error_with_cnt}")
# avg = sum(sample[0] for sample in random.sample(conn.execute("SELECT speed FROM past_speed limit 100").fetchall(), k=100)) / 100

#

import pandas as pd
import os

data_path = '/Users/edbergbak/work/pbl4_cp/master/file_data'
file2101 = "2021년 01월 서울시 차량통행속도.xlsx"
file2102 = "2021년 02월 서울시 차량통행속도.xlsx"
file2103 = "2021년 03월 서울시 차량통행속도.xlsx"

print("Read file 1")
df2101 = pd.read_excel(os.path.join(data_path, file2101))
print("Read file 2")
df2102 = pd.read_excel(os.path.join(data_path, file2102))
print("Read file 3")
df2103 = pd.read_excel(os.path.join(data_path, file2103))

def write_speed_data_list(df, f, key):
    num_rows, _ = df.shape
    date_colume_index = 0
    section_id_index = 3
    time_start_index = 12
    i = 0
    for row_index in range(num_rows):
        i += 1
        if i % 1500 == 0:
            print(f"{i}/{num_rows} ({i / num_rows * 100}%) processed ({key})")
        date = df.iat[row_index, date_colume_index]
        section_id = df.iat[row_index, section_id_index]
        for h in range(24):
            speed = float("{:.2f}".format(df.iat[row_index, time_start_index + h]))    
            f.write(f"insert into past_speed (section_id, record_date, record_hour, speed) values ({section_id}, {date}, {h}, {speed});\n")

with open("speed.sql", "w") as f:
    f.write("section_id,record_date,record_hour,speed\n")
    print("insert_data_1")
    write_speed_data_list(df2101, f, '1')
    print("insert_data_2")
    write_speed_data_list(df2102, f, '2')
    print("insert_data_3")
    write_speed_data_list(df2103, f, '3')

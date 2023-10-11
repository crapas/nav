import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad


seoul_road = SeoulRoad()

section_with_gpdy = seoul_road.get_connected_sections(1220022800)
# print(section_with_gpdy)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220016500)
# print(section_with_gpdy)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220024700)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220017700)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220005300)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220003500)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220015300)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220013900)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220003700)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220028000)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
print("-----------------------------------------------")
section_with_gpdy = seoul_road.get_connected_sections(1220024100)
for sections in section_with_gpdy:
    for section in sections:
        print(f"{section[0]}: {seoul_road.get_db_spot_name(section[0])} -> {section[1]}: {seoul_road.get_db_spot_name(section[1])} : {section[2]}")
test_road = SeoulRoad(False)
spots_for_test = [1220019400,
                  1220022800,
                  1220016500,
                  1220017700,
                  1220015300,
                  1220000300,
                  1220013900,
                  1220003500,
                  1220003700,
                  1220024700,
                  1220028000,
                  1220024100]

spot_dict = {}
spot_dict[1220019400] = "영동4교"
spot_dict[1220022800] = "개포동역"
spot_dict[1220016500] = "개포고교"
spot_dict[1220017700] = "경기여고앞"
spot_dict[1220015300] = "개포3,4단지"
spot_dict[1220000300] = "구룡마을입구"
spot_dict[1220013900] = "구룡터널"
spot_dict[1220003500] = "구룡초교"
spot_dict[1220003700] = "개포시립도서관입구"
spot_dict[1220024700] = "영동5교"
spot_dict[1220028000] = "대치역"
spot_dict[1220024100] = "도곡역"

# 0, 영동4교, 1220019400
# 1, 개포동역, 1220022800
# 2, 개포고교, 1220016500
# 3, 경기여고앞, 1220017700
# 4, 개포3,4단지, 1220015300
# 5, 구룡마을입구, 1220000300
# 6, 구룡터널, 1220013900
# 7, 구룡초교, 1220003500
# 8, 개포시립도서관입구, 1220003700
# 9, 영동5교, 1220024800
# 10, 대치역, 1220028000
# 11, 도곡역, 1220024100
sections_for_test = [
    (1, 2),
    (2, 1),
    #    (1, 9),
    (1, 3),
    (2, 0),
    (2, 8),
    (2, 7),
    (3, 1),
    (3, 4),
    (4, 3),
    (4, 5),
    (5, 4),
    (5, 8),
    (6, 5),
    (7, 6),
    (8, 2),
    (8, 5),
    (9, 1),
    #    (9, 10),
    (10, 9),
    (10, 11),
    (11, 0),
    (11, 10),
    (0, 11),
    (0, 2)]
for section_for_test in sections_for_test:
    # print(section_for_test)
    start_spot = spots_for_test[section_for_test[0]]
    end_spot = spots_for_test[section_for_test[1]]
    section = seoul_road.get_sections(
        start_spot, end_spot)
    print(f"test_road.add_section({start_spot}, {end_spot}, {section[0]})")


test_road.add_section(1220022800, 1220016500, 1220012000)
test_road.add_section(1220016500, 1220022800, 1220012100)
test_road.add_section(1220022800, 1220017700, 1220012600)
test_road.add_section(1220016500, 1220019400, 1220011100)
test_road.add_section(1220016500, 1220003700, 1220008600)
test_road.add_section(1220016500, 1220003500, 1220008200)
test_road.add_section(1220017700, 1220022800, 1220012700)
test_road.add_section(1220017700, 1220015300, 1220009400)
test_road.add_section(1220015300, 1220017700, 1220009500)
test_road.add_section(1220015300, 1220000300, 1220000500)
test_road.add_section(1220000300, 1220015300, 1220000600)
test_road.add_section(1220000300, 1220003700, 1220007500)
test_road.add_section(1220013900, 1220000300, 1220000400)
test_road.add_section(1220003500, 1220013900, 1220006800)
test_road.add_section(1220003700, 1220016500, 1220008700)
test_road.add_section(1220003700, 1220000300, 1220007400)
test_road.add_section(1220024700, 1220022800, 1220015000)
test_road.add_section(1220028000, 1220024700, 1220018200)
test_road.add_section(1220028000, 1220024100, 1220018400)
test_road.add_section(1220024100, 1220019400, 1220014000)
test_road.add_section(1220024100, 1220028000, 1220018500)
test_road.add_section(1220019400, 1220024100, 1220014100)
test_road.add_section(1220019400, 1220016500, 1220011000)
test_road.print_road_graph()
test_road.print_road_info()

start_spot = spots_for_test[10]
end_spot = spots_for_test[4]
print(start_spot, end_spot)
print("-----------------------------------------------")

all_path = test_road.bfs_find_all_path(start_spot, end_spot)
for path in all_path:
    path_number = [spots_for_test.index(spot) for spot in path]
    print(path_number)

print("-----------------------------------------------")


all_path = test_road.dfs_find_all_path(start_spot, end_spot)
for path in all_path:
    path_number = [spots_for_test.index(spot) for spot in path]
    print(path_number)

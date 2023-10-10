import sys
sys.path.append('..')
from lib.seoul_road_graph import SeoulRoad

# 그래프 객체를 생성한다.
graph = SeoulRoad()

# 그래프에 8개의 구간을 추가한다.
graph.add_section('경기여고앞', '개포3.4단지', 1220009400)
graph.add_section('개포동역', '개포고교', 1220012000)
graph.add_section('경기여고앞', '개포동역', 1220012700)
graph.add_section('개포동역', '개포2동주민센터', 1220013700)
graph.add_section('개포동역', '영동5교', 1220015100)
graph.add_section('개포동역', '경기여고앞', 1220012600)
graph.add_section('개포동역', '경기여고앞', 1220012601)
graph.add_section('영동5교', '경기여고앞', 1220015101)

# 그래프 객체에서 몇 가지 정보를 확인한다.
print("### 만들어진 그래프의 정보 :")
graph.print_road_info()
print("----------------------------------------")

print("### 만들어진 그래프의 구조 :")
graph.print_road_graph()
print("----------------------------------------")

print("### 영동5교와 연결된 구간들")
start_from_yd5, end_to_yd5 = graph.get_connected_sections('영동5교')
print("### 영동5교에서 시작하는 구간들 :")
for section in start_from_yd5:
    print(f'    {section[0]} -> {section[1]} : {section[2]}')
print("### 영동5교에서 끝나는 구간들 :")
for section in end_to_yd5:
    print(f'    {section[0]} -> {section[1]} : {section[2]}')
print("----------------------------------------")

print("### 개포동역에서 시작해서 경기여고앞에서 끝나는 구간들 : ")
sections_gpdy_to_ggyg = graph.get_sections('개포동역', '경기여고앞')
for section in sections_gpdy_to_ggyg:
    print(f'    {section}')
print("----------------------------------------")

spots = graph.get_spots(1220012600)
print(f"구간 1220012600은 {spots[0]}에서 {spots[1]}로 가는 구간입니다.")
print("----------------------------------------")

# 그래프에서 구간을 삭제하면서 정상 동작하는지 확인해본다.
if graph.remove_section(1220015101):
    print("### 구간 1220015101을 삭제했습니다.")
else:
    print("### 구간 1220015101을 삭제하지 못했습니다.")
print("### 삭제 시도 후 그래프의 정보 :")
graph.print_road_info()
print("----------------------------------------")

if graph.remove_section(1220015101):
    print("### 구간 1220015101을 삭제했습니다.")
else:
    print("### 구간 1220015101을 삭제하지 못했습니다.")
print("### 삭제 시도 후 그래프의 정보 :")
graph.print_road_info()
print("----------------------------------------")

if graph.remove_section(1220015100):
    print("### 구간 1220015100을 삭제했습니다.")
else:
    print("### 구간 1220015100을 삭제하지 못했습니다.")
print("### 삭제 시도 후 그래프의 정보 :")
graph.print_road_info()
print("----------------------------------------")

graph.remove_section(1220012600)
print("### 1220012600 구간 삭제 후 그래프의 정보 :")
graph.print_road_info()
print("----------------------------------------")

graph.remove_section(1220012601)
print("### 1220012601 삭제 후 그래프의 정보 :")
graph.print_road_info()
print("### 1220012601 삭제 후 그래프의 구조 :")
graph.print_road_graph()

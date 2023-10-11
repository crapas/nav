# from db_util import get_db_sections
from .db_util import *
from .common_util import *
import sys
from psycopg_pool import ConnectionPool
import queue


class SeoulRoad:
    # 생성자 메소드
    def __init__(self, build_graph=True):
        self.graph = {}
        self.section_count = 0
        self.spot_count = 0
        # DB Connection pool을 생성한다.
        try:
            self.db_pool = ConnectionPool(
                "dbname=testdatabase \
                host=localhost \
                user=postgres \
                password=1234",
                min_size=1,
                max_size=10)
            # DB connection pool이 만들어지고 min_size 만큼의 connection이 생성될 때 까지 대기
            self.db_pool.wait()
        except Exception as e:  # DB 연결 오류
            sys.stderr.write(f"DB Connection Pool이 준비되지 않았습니다. : {e}")
            sys.exit(1)

        # DB의 정보를 사용해 그래프를 구성한다.
        if build_graph:
            result = self.__build_graph()
            # 그래프가 구성되지 않으면 None을 반환한다.
            if result == False:
                return None

    # 소멸자 메소드 - DB Connection Pool을 닫는다.
    def __del__(self):
        self.db_pool.close()

    # Database의 정보로 그래프를 구성하는 Private 메소드
    #   Return Value : 그래프 구성 성공 여부
    def __build_graph(self):
        # 클래스가 가지고 있는 DB connection pool에서 connection을 가져온다.
        with self.db_pool.connection() as conn:
            # 구간 정보를 가져온다.
            sections_info = get_db_sections(conn)
        if sections_info == None:
            # DB 오류가 발생하면 False를 반환한다.
            return False
        # 각 구간의 정보를 사용해 그래프에 변을 추가한다.
        for section_info in sections_info:
            self.add_section(section_info[1],
                             section_info[2],
                             section_info[0])
        # 그래프에 추가된 변이 없다면 False를 반환한다.
        if self.section_count == 0:
            return False
        return True

    # 구간을 추가하는 메소드
    #   spot1 : 구간의 시작지점 고유번호
    #   spot2 : 구간의 끝지점 고유번호
    #   section : 구간의 고유번호
    def add_section(self, spot1, spot2, section):
        # 그래프에 두 지점을 추가한다. 이미 존재하는 지점이라면 추가하지 않는다.
        self.__add_spots([spot1, spot2])
        if spot2 not in self.graph[spot1].keys():
            # 그래프 딕셔너리의 시작지점에서 끝지점으로 가는 구간이 존재하지 않는다면
            # {끝지점 : [구간]}을 딕셔너리에 추가한다.
            self.graph[spot1][spot2] = [section]
        else:
            # 그래프 딕셔너리에 시작지점에서 끝지점으로 가는 구간이 이미 존재한다면
            # 구간 리스트에 추가하고자 하는 구간을 추가한다.
            self.graph[spot1][spot2].append(section)
        # 구간의 수를 1 증가시킨다.
        self.section_count += 1

    # 지점을 추가하는 Private 메소드
    #   spots : 추가할 지점들의 리스트
    #   만약 그래프에 이미 해당 지점이 존재한다면, 추가하지 않는다. (오류 상황이 아님)

    def __add_spots(self, spots):
        for spot in spots:
            if spot not in self.graph:
                self.graph[spot] = {}
                self.spot_count += 1

    # 구간을 삭제하는 메소드
    #   section : 삭제할 구간의 고유번호
    #   Return Value : 삭제 성공 여부
    def remove_section(self, section):
        # 구간을 삭제한 후 필요한 경우 지점도 삭제해야 하므로 시작점과 끝점을 구한다.
        spots = self.get_spots(section)
        # 삭제하고자 하는 구간이 존재하지 않는다면 False를 반환한다.
        if spots == None:
            return False
        # 같은 시작점과 끝점을 가지는 구간들의 리스트를 구한다.
        sections = self.graph[spots[0]][spots[1]]
        if len(sections) == 1:
            # 구간이 하나 뿐이라면 그래프 딕셔너리에서 해당 구간을 삭제하고
            # 시작점과 끝점을 가지는 구간이 하나도 없다면 지점도 삭제한다.
            del self.graph[spots[0]][spots[1]]
            self.__remove_spot([spots[0], spots[1]])
        else:
            # 구간이 여러개 있다면, 주어진 구간만 리스트에서 삭제한다.
            sections.remove(section)
        # 구간의 수를 1 감소시킨다.
        self.section_count -= 1
        return True

    # 지점을 삭제하는 Private 메소드
    #   spots : 삭제할 지점들의 리스트
    # 주어진 리스트 내의 지점 중 시작지점 또는 끝지점으로 구간에 연결되어 있지 않은 경우
    # 그래프에서 해당 지점을 삭제한다. 하나라도 연결이 되어 있다면 삭제하지 않는다.
    def __remove_spot(self, spots):
        for spot in spots:
            # 연결 정보를 구한다.
            sections_from_spot, sections_to_spot = self.get_connected_sections(
                spot)
            # 연결된 구간이 하나도 없다면 그래프 딕셔너리에서 해당 지점을 삭제한다.
            if len(sections_from_spot) == 0 and len(sections_to_spot) == 0:
                del self.graph[spot]
                # 지점의 수를 1 감소시킨다.
                self.spot_count -= 1

    # 지점과 연결된 구간들을 구하는 메소드
    #   spot : 지점의 고유번호
    #   Return Value : (spot, 끝지점, 구간)의 리스트, (시작지점, spot, 구간)의 리스트의 튜플
    # 어떤 지점과 연결된 구간을 주어진 지점이
    # 시작지점인지, 끝지점인지에 따라 2개의 리스트를 각각 구성해 튜플로 반환한다.
    def get_connected_sections(self, spot):
        # 존재하지 않은 지점이라면 None을 반환한다.
        if spot not in self.graph.keys():
            return None

        # spot이 시작점인 section들
        sections_from_spot = []
        for end_spot, sections in self.graph[spot].items():
            for section in sections:
                sections_from_spot.append((spot, end_spot, section))

        # spot이 끝점인 section들
        sections_to_spot = []
        for start_spot, end_spots in self.graph.items():
            if spot in end_spots.keys():
                sections = end_spots[spot]
                for section in sections:
                    sections_to_spot.append((start_spot, spot, section))

        return (sections_from_spot, sections_to_spot)

    # 시작지점과 끝지점으로 구간을 구하는 메소드
    #   start_spot : 시작지점의 고유번호
    #   end_spot : 끝지점의 고유번호
    #   Return Value : 구간의 리스트, 구간이 존재하지 않으면 빈 리스트를 반환한다.
    def get_sections(self, spot1, spot2):
        if spot1 in self.graph.keys() and spot2 in self.graph.keys():
            if spot2 in self.graph[spot1].keys():
                return self.graph[spot1][spot2]
        return []

    # 구간의 시작지점과 끝지점을 구하는 메소드
    #   section : 구간의 고유번호
    #   Return Value : (시작지점, 끝지점)의 튜플
    def get_spots(self, section):
        for start_spot, end_spots in self.graph.items():
            for end_spot, sections in end_spots.items():
                if section in sections:
                    return (start_spot, end_spot)
        return None

    # 그래프의 정보를 출력하는 메소드
    def print_road_info(self):
        print(f"구간의 수는 {self.section_count}개이고, 지점의 수는 {self.spot_count}개입니다.")

    # 그래프의 구조를 출력하는 메소드
    def print_road_graph(self):
        for start_spot, end_spots in self.graph.items():
            for end_spot, sections in end_spots.items():
                print(f"{start_spot} -> {end_spot} : {sections}")

    # 그래프를 검증하고 유효한 경우 경로 비용을 출력하는 메소드
    #   conn : DB 연결 객체
    #   path : 경로를 구성하는 지점들의 리스트
    #   weight_name : 가중치의 종류
    #   Return Value : 경로 비용 또는 None (경로가 유효하지 않은 경우)
    def validation(self, path, weight_name):
        # 주어진 가중치 이름(weight_name)으로 가중치 함수를 가져온다.
        weight_function = get_weight_provider(weight_name)
        path_cost = 0
        for i in range(len(path) - 1):
            # 구간을 가져온다.
            sections = self.get_sections(path[i], path[i + 1])

            if len(sections) == 0:   # 구간이 존재하지 않는다면
                return None

            # 두 지점 사이의 구간이 여러 개라면 그 중 가장 작은 값의 가중치를 사용한다.
            min_weight = sys.maxsize
            # DB Connection을 가지고 온다.
            with self.db_pool.connection() as conn:
                for section in sections:
                    weight = weight_function(conn, section)
                    if weight < min_weight:
                        min_weight = weight
            path_cost += min_weight

        return path_cost

    # DB Connection Pool을 반환하는 메소드
    def get_db_pool(self):
        return self.db_pool

    # 현재 그래프 상의 spot_name의 지점 고유번호를 반환하는 메소드
    def get_db_spots(self, spot_name):
        with self.db_pool.connection() as conn:
            return get_db_spots(conn, spot_name)

    # 현재 그래프 상의 spot의 지점 이름을 반환하는 메소드
    def get_db_spot_name(self, spot):
        with self.db_pool.connection() as conn:
            return get_db_spot_name(conn, spot)


############### For Exercise ###############

    # step 만큼의 구간을 지나 도착하는 지점들을 반환하는 메소드
    #   spot : 시작 지점
    #   step : 구간 수
    #   Return Value : step 만큼의 구간을 지나 도착하는 지점들의 리스트


    def get_neighbors_with_step(self, spot, step):
        # 만약 더 이상 step이 남아있지 않다면 현재 지점을 반환한다.
        if step == 0:
            return [spot]
        neighbors = []
        # 이웃 지점의 목록을 구한 후
        for neighbor in self.graph[spot].keys():
            # 각 이웃 지점에서 step - 1 만큼의 구간을 지나 도착하는 지점들을 구하도록 재귀호출한다.
            # 결과를 neighbors에 추가하는데, 이 메소드는 중복이 없는 메소드가 되어야 하므로
            # set으로 변환한 후 다시 리스트로 변환하는 방식으로 중복을 제거한다.
            neighbors = list(
                set(neighbors + self.get_neighbors_with_step(neighbor, step - 1)))
        return neighbors

    # 주어진 spot으로부터 출발해 step 만큼의 구간으로 구성된 모든 경로를 반환하는 메소드
    #   spot : 시작 지점
    #   step : 구간 수
    #   Return Value : step 만큼의 구간으로 구성된 모든 경로들의 리스트
    #
    #   매 재귀 호출 마다 반환되는 값은 다음과 같다.
    #       만약 step이 0인 경우 [spot]을 반환한다.
    #       만약 step이 0이 아닌데 더 이상 이웃 지점이 없다면 빈 리스트를 반환한다.
    #       만약 step이 0이 아니고 이웃 지점이 있다면 이웃 지점과 step - 1로 재귀 호출한 후
    #           모든 반환된 결과 리스트의 가장 앞에 spot을 추가한 리스트를 반환한다.
    #           step이 0이 아니고 재귀호출이 종료된 경우는 빈 리스트를 반환하므로, 이 때
    #           결과에 추가되지 않는다.
    def get_paths_with_step(self, spot, step):
        # 만약 더 이상 step이 남아있지 않다면 현재 지점만으로 구성된 경로를 반환한다.
        if step == 0:
            return [[spot]]
        paths = []
        # step이 남아 있으면 이웃 지점들을 구한 후
        for neighbor in self.graph[spot].keys():
            # 각각의 이웃, step - 1로 재귀 호출한다.
            followed_paths = self.get_paths_with_step(neighbor, step - 1)
            # 모든 재귀 호출의 결과를 취합하되,
            #   현재 지점이 포함되지 않은 경로만을 대상으로
            #   현재 지점을 경로의 앞에 추가한다.
            #   빈 리스트([])가 반환되는 경우, 아래의 루프에 들어가지 않으므로 배제된다.
            for followed_path in followed_paths:
                if spot not in followed_path:
                    paths.append([spot] + followed_path)
        return paths

    # bfs를 사용해 start_spot에서 end_spot까지의 모든 경로를 찾는 메소드
    #   start_spot : 시작 지점
    #   end_spot : 목표 지점
    #   Return Value : 모든 경로들의 리스트
    # 재귀 호출을 사용하는 대신 큐를 사용해 현재 경로에서 추가할 수 있는 모든 경로를 큐에 추가한다.
    # 루프에서는 큐에서 가장 먼저 들어간 경로를 꺼내고, 해당 경로의 마지막 지점을 확인한다.
    # 해당 경로의 마지막 지점이 목표 지점이면, 경로가 완성된 것이므로, 해당 경로를 결과리스트에 추가한다.
    # 큐의 모든 경로를 확인해서 큐가 빌 때 까지 루프를 반복한다.
    # 큐의 가장 앞 경로는 항상 너비를 기준으로 먼저 들어간 경로이므로 BFS 방식의 탐색이 된다.
    def bfs_find_all_path(self, start_spot, end_spot):
        results = []
        q = queue.Queue()
        # 큐에 시작 지점으로 구성된 경로를 추가한다.
        q.put([start_spot])

        while not q.empty():            # 큐가 빌 때까지 반복
            path = q.get()              # 큐의 첫 번째 경로를 꺼낸다.
            vertex = path[-1]           # 경로의 마지막은 현재 탐색하고 있는 지점이며

            if vertex == end_spot:      # 현재 지점 = 목표 지점 : 경로 완성
                results.append(path)
                continue
            # 경로가 완성되지 않았으면, 다음 구간으로의 경로를 만들어 각각을 큐에 추가한다.
            for next in self.graph[vertex].keys():
                # 다음 탐색할 지점이 이미 지나온 지점이면 큐에 추가하지 않는다.
                if next not in path:
                    q.put(path + [next])
        return results

    # dfs를 사용해 start_spot에서 end_spot까지의 모든 경로를 찾는 메소드
    #   start_spot : 시작 지점
    #   end_spot : 목표 지점
    #   Return Value : 모든 경로들의 리스트
    # 현재 경로에서 추가할 수 있는 모든 경로 중 하나를 선택해 재귀 호출한다.
    # 이러한 방식으로 재귀 호출을 하면, 너비보다 깊이를 우선으로 경로를 탐색하게 된다.
    def dfs_find_all_path(self, start_spot, end_spot, path=None):
        # 탐색을 시작할 때, 즉 path가 None인 경우 현재 지점으로 구성된 경로를 생성한다.
        if path is None:
            path = [start_spot]

        # 재귀 호출 시점의 시작 지점이 목표 지점과 동일하면 경로가 완성된 것이다.
        if start_spot == end_spot:
            return [path]

        results = []
        # 현재 지점에서 이동 가능한 모든 다른 지점에 대해서
        for next in self.graph[start_spot].keys():
            # 다음 탐색할 지점이 이미 지나온 지점이면 해당 경로는 배제한다.
            if next not in path:
                # 다음 탐색 지점의 경로를 만들어 재귀 호출한다.
                result = self.dfs_find_all_path(
                    next, end_spot, path + [next])
                # 재귀 호출의 결과를 취합한다.
                results += result
        return results

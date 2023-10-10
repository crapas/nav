from db import get_db_sections

class WeightedGraph:
    # 초기화 메소드
    #   is_directed: 방향성 여부를 나타내는 boolean 값
    def __init__(self, is_directed):
        # 그래프를 표현하는 딕셔너리로 Key는 꼭짓점, Value는 인접한 꼭짓점들의 리스트
        self.vertices = {}
        # 방향성
        self.is_directed = is_directed
        # 변의 수
        self.edge_count = 0
        # 꼭짓점의 수
        self.vertex_count = 0
        # 가중치 룩업 딕셔너리
        #   룩업 딕셔너리는 Key가 (꼭짓점1, 꼭짓점2)인 튜플이고,
        #   Value는 2개 이상의 가중치를 저장할 수 있도록 가중치들의 리스트로 구성된다.
        self.weight_lookup = {}



    # 변을 추가하는 메소드
    #   vertex1 : 변의 한쪽 끝 꼭짓점이며, 방향성 그래프의 경우 시작점을 의미한다.
    #   vertex2 : 변의 다른쪽 끝 꼭짓점이며, 방향성 그래프의 경우 끝점을 의미한다.
    def add_edge(self, vertex1, vertex2, weight):
        # 가중치의 값이 양의 숫자인지 확인
        if weight <= 0:
            print("가중치는 양의 숫자여야 합니다.")
            return False
        # 그래프에 꼭짓점 추가
        self.__add_vertices([vertex1, vertex2])
        # 변 추가
        if self.is_directed:
            # 그래프가 방향성 그래프라면 지정된 순서의 방향의 변만 추가한다.
            # 만약 변이 이미 존재하면 변은 추가하지 않고 가중치 룩업 테이블에만 이를 추가한다.
            if vertex2 not in self.vertices[vertex1]:
                self.vertices[vertex1].append(vertex2)
            # 가중치 추가
            self.__add_weight(vertex1, vertex2, weight)
        else:
            # 그래프가 비방향성 그래프라면 양쪽 방향의 변을 모두 추가한다.
            # 이때 변이 이미 존재하면 변은 추가하지 않고 가중치 룩업 테이블에만 이를 추가한다.
            if vertex2 not in self.vertices[vertex1]:
                self.vertices[vertex1].append(vertex2)
                self.vertices[vertex2].append(vertex1)
            # 가중치 추가
            #   그래프 딕셔너리와 달리 룩업 테이블은 비방향성 그래프에서는
            #   꼭짓점1과 꼭짓점2의 순서와 무관하게 하나만 저장한다.
            self.__add_weight(max(vertex1, vertex2),
                              min(vertex1, vertex2), weight)

        # 방향성 여부에 따라 변을 몇 개 추가했던 간에 실질적으로 변은 1개 추가되었다.
        self.edge_count += 1
        return True

    def __add_weight(self, vertex1, vertex2, weight):
        if (vertex1, vertex2) not in self.weight_lookup:
            self.weight_lookup[(vertex1, vertex2)] = [weight]
        else:
            self.weight_lookup[(vertex1, vertex2)].append(weight)

    # 꼭짓점을 추가하는 Private 메소드
    #   vertices : 추가할 꼭짓점들의 리스트
    #   만약 그래프에 이미 해당 꼭짓점이 존재한다면, 추가하지 않는다.
    def __add_vertices(self, vertices):
        for vertex in vertices:
            if vertex not in self.vertices:
                self.vertex_count += 1
                self.vertices[vertex] = []

    # 가중치를 반환하는 메소드
    #   vertex1 : 꼭짓점1
    #   vertex2 : 꼭짓점2
    def get_weight(self, vertex1, vertex2):
        # 꼭짓점1과 꼭짓점2가 유효한지 확인
        if vertex1 not in self.vertices or vertex2 not in self.vertices:
            print("유효하지 않은 꼭짓점입니다.")
            return None
        # 꼭짓점1과 꼭짓점2가 연결되어 있는지 확인
        if vertex2 not in self.vertices[vertex1]:
            print("꼭짓점1과 꼭짓점2가 연결되어 있지 않습니다.")
            return None
        # 꼭짓점1과 꼭짓점2 사이의 가중치를 반환
        if self.is_directed:
            return self.weight_lookup[(vertex1, vertex2)]
        else:
            return self.weight_lookup[(max(vertex1, vertex2), min(vertex1, vertex2))]

    # 그래프를 출력하는 메소드
    def print_graph(self):
        for vertex1, edges in self.vertices.items():
            result = f"{vertex1} : ["
            for vertex2 in edges:
                weight = self.get_weight(vertex1, vertex2)
                result += f"{vertex2} : {weight}, "
            if len(edges) > 0:
                result = result[:-2] + "]"
            else:
                result += "]"
            print(result)
        print(f"변의 수 : {self.edge_count}")
        print(f"꼭짓점의 수 : {self.vertex_count}")
        print(f"가중치 룩업 테이블 : {self.weight_lookup}")

    # 경로 검증 메소드
    def validatation(self, path):
        cost = 0
        for i in range(len(path) - 1):
            # 경로 상의 두 꼭짓점 사이의 변이 없으면 경로는 유효하지 않다.
            if path[i + 1] not in self.vertices[path[i]]:
                return None
            # 두 꼭짓점 사이에 변이 여러 개 있을 경우, 가중치가 가장 작은 변의 가중치를 선택한다.
            cost += min(self.get_weight(path[i], path[i + 1]))
        return cost

    # 변을 삭제한다.
    def remove_edge(self, vertex1, vertex2):
        # 꼭짓점1과 꼭짓점2가 유효한지 확인
        if vertex1 not in self.vertices or vertex2 not in self.vertices:
            print("유효하지 않은 꼭짓점입니다.")
            return False
        # 꼭짓점1과 꼭짓점2가 연결되어 있는지 확인
        if vertex2 not in self.vertices[vertex1]:
            print("꼭짓점1과 꼭짓점2가 연결되어 있지 않습니다.")
            return False
        # 방향성 그래프의 경우 꼭짓점1에서 꼭짓점2로 가는 변만 삭제한다.
        if self.is_directed:
            self.vertices[vertex1].remove(vertex2)
            self.weight_lookup.pop((vertex1, vertex2))
        # 비방향성 그래프의 경우 양쪽 방향의 변을 모두 삭제한다.
        else:
            self.vertices[vertex1].remove(vertex2)
            self.vertices[vertex2].remove(vertex1)
            self.weight_lookup.pop(
                (max(vertex1, vertex2), min(vertex1, vertex2)))
        # 변의 수를 1 감소시킨다.
        self.edge_count -= 1
        # 꼭짓점1과 꼭짓점2가 더 이상 연결되어 있지 않으면 꼭짓점1과 꼭짓점2를 삭제한다.
        if self.is_alone(vertex1):
            self.remove_vertex(vertex1)
        if self.is_alone(vertex2):
            self.remove_vertex(vertex2)
        return True

    # 꼭짓점이 혼자인지 확인하는 메소드
    def is_alone(self, vertex):
        # vertex를 시작점으로 하는 꼭짓점이 있는 경우
        if len(self.vertices[vertex]) != 0:
            return False
        # vertex를 끝점으로 하는 꼭짓점이 있는 경우
        for _, edges in self.vertices.items():
            if vertex in edges:
                return False
        # vertex를 시작점이나 끝점으로 하는 꼭짓점이 없는 경우
        return True

    # 꼭짓점을 삭제하는 메소드
    def remove_vertex(self, vertex):
        # vertex와 연결된 변을 찾는다.
        connected_edge = []
        # vertex를 시작점으로 하는 변을 찾는다.
        if vertex in self.vertices:
            for end_vertex in self.vertices[vertex]:
                connected_edge.append((vertex, end_vertex))
        else:
            # 만약 vertex가 그래프에 없다면 삭제할 수 없다.
            print("유효하지 않은 꼭짓점입니다.")
            return False
        # vertex를 끝점으로 하는 변을 찾는다.
        for start_vertex, edges in self.vertices.items():
            if vertex in edges:
                connected_edge.append((start_vertex, vertex))
        # 찾은 변을 삭제한다.
        for edge in connected_edge:
            self.remove_edge(edge[0], edge[1])
        # vertex를 삭제한다.
        if vertex in self.vertices:
            self.vertices.pop(vertex)
            self.vertex_count -= 1
        return True

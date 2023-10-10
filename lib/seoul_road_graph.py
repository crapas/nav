class SeoulRoad:
    # 초기화 메소드
    def __init__(self):
        self.graph = {}
        self.section_count = 0
        self.spot_count = 0        

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
            sections_from_spot, sections_to_spot = self.get_connected_sections(spot)
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
from .db_util import *

# weight_name에 해당하는 가중치 함수를 반환한다.
#   weight_name : 가중치 종류의 이름
#   Return Value : 가중치 함수 또는 None (사용할 수 없는 가중치 이름)


def get_weight_provider(weight_name):
    if weight_name == 'distance':       # 가중치 'distance'의 경우
        # db_util.get_section_distance 함수를 반환한다.
        return get_section_distance
    # if weight_name == 'time':         # 가중치 'time'이 만약 존재한다면
    #   return get_section_time         # 이와 같이 가중치의 종류에 맞는 함수를 추가하면 된다.
    else:                               # 가중치 이름이 유효하지 않을 때
        return None

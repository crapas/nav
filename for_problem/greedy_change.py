# 그리디 알고리즘으로 최소한의 동전 숫자로 금액을 구성하는 방법을 반환하는 함수
#   n: 금액
#   Return Value : (동전의 최소 개수, 각 동전의 개수를 나타내는 딕셔너리)
def greedy_change(n):
    # 동전의 종류를 내림차순으로 정렬
    coins = [100, 50, 25, 10, 5, 1]
    coin_count = 0
    coin_used = {}

    for coin in coins:
        # 해당 동전으로 얼마나 많이 줄 수 있는지 계산
        if n >= coin:
            num = n // coin
            n -= num * coin
            coin_count += num
            coin_used[coin] = num

    return coin_count, coin_used

# 그리디 알고리즘으로 제한된 동전으로 최소한의 동전 숫자로 금액을 구성하는 방법을 반환하는 함수
#   n: 금액
#   Return Value : (동전의 최소 개수, 각 동전의 개수를 나타내는 딕셔너리)
#                   만약 금액을 만들 수 없다면 (None, None)을 반환


def limited_greedy_change(n):
    coins = [100, 50, 25, 10, 5, 1]

    # 각 동전의 최대 사용 가능 개수를 설정
    max_coins = {
        100: float('inf'),  # 무한대
        50: float('inf'),
        25: 0,
        10: 1,
        5: float('inf'),
        1: 3
    }

    coin_count = 0
    coin_used = {}

    for coin in coins:
        if n >= coin:
            # 가능한 많이 사용되는 동전의 수와 제한된 동전의 수 중 작은 것을 선택
            num = min(n // coin, max_coins[coin])
            n -= num * coin
            coin_count += num

            # 사용한 동전의 개수를 업데이트
            if coin in coin_used:
                coin_used[coin] += num
            else:
                coin_used[coin] = num
    if n != 0:  # 더 이상 사용할 수 있는 동전이 없는데 남은 금액이 있는 경우
        return None, None
    return coin_count, coin_used


print("----- 398센트를 제한없이 만드는 방법 -----")
count, used = greedy_change(398)
print(f"필요한 동전의 최소 개수: {count}")
for coin, num in used.items():
    print(f"{coin}센트: {num}개")

print("----- 398센트를 일부 제한된 동전으로 만드는 방법 -----")
count, used = limited_greedy_change(398)
if count is None:
    print("해당 금액을 만들 수 없습니다.")
else:
    print(f"필요한 동전의 최소 개수: {count}")
    for coin, num in used.items():
        print(f"{coin}센트: {num}개")

print("----- 399센트를 일부 제한된 동전으로 만드는 방법 -----")
count, used = limited_greedy_change(399)
if count is None:
    print("해당 금액을 만들 수 없습니다.")
else:
    print(f"필요한 동전의 최소 개수: {count}")
    for coin, num in used.items():
        print(f"{coin}센트: {num}개")

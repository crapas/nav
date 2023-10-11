# 단순 재귀 호출로 fibonacci 수열을 구하는 함수
#   n: fibonacci 수열의 n번째 수
def fib(n):
    # n == 1 또는 n == 2인 경우 1을 반환
    if n <= 2:
        return 1
    else:
        # 재귀 호출을 사용해 n-1번째와 n-2번째의 합을 반환
        return fib(n - 1) + fib(n - 2)

# 하향식 다이나믹 프로그래밍으로 fibonacci 수열을 구하는 함수
#   n: fibonacci 수열의 n번째 수
#   memo: n번째 fibonacci 수열의 값을 저장하는 딕셔너리
#   Return Value: n번째 fibonacci 수열의 값
# n으로부터 아래 방향으로 재귀 호출하되, 한 번 계산한 값은 memo에 저장해 두었다가 재활용한다.


def fib_top_down(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_top_down(n - 1, memo) + fib_top_down(n - 2, memo)
    return memo[n]

# 상향식 다이나믹 프로그래밍으로 fibonacci 수열을 구하는 함수
#   n: fibonacci 수열의 n번째 수
#   Return Value: n번째 fibonacci 수열의 값
# 1부터 차례로 올라가면서 n번째 fibonacci 수열의 값을 계산하고, 이를 배열에 저장하여
# 한 번 계산한 값을 재활용한다.


def fib_bottom_up(n):
    if n <= 1:
        return n

    fib = [0] * (n + 1)
    fib[1] = 1

    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]

    return fib[n]


import time


def fib_with_time(n, fib_function):
    start = time.time()
    result = fib_function(n)
    end = time.time()
    print(f"fib({n})의 값은 {result}이며, 계산하는 데 걸린 시간은 {end - start}초 입니다.")


print("----- 단순 재귀 호출 -----")
fib_with_time(10, fib)
fib_with_time(20, fib)
fib_with_time(30, fib)
fib_with_time(40, fib)

print("----- 하향식 다이나믹 프로그래밍 -----")
fib_with_time(10, fib_top_down)
fib_with_time(20, fib_top_down)
fib_with_time(30, fib_top_down)
fib_with_time(40, fib_top_down)

print("----- 상향식 다이나믹 프로그래밍 -----")
fib_with_time(10, fib_bottom_up)
fib_with_time(20, fib_bottom_up)
fib_with_time(30, fib_bottom_up)
fib_with_time(40, fib_bottom_up)

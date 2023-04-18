import random
import copy
import datetime
import math

# 8-queens 문제(n-queens 문제)
class Problem:
    def __init__(self):
        self.n = 8         # 8-queens
        self.max_exe_time = 30  # 최대 수행 시간 30초

    def GetInitialSolution(self):
        # 1~n까지의 값들을 무작위로 Shuffle
        solution = [i for i in range(1, self.n + 1)]
        random.shuffle(solution)
        return solution, self.ObjectiveFunction(solution)

    def GetANeighbor(self, state):
        neighbor = copy.copy(state)
        index_list = [i for i in range(self.n)]
        i, j = random.sample(index_list, 2)    # index 중에 2개 선택
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]     # i번째, j번째 교환
        obj_value = self.ObjectiveFunction(neighbor)

        return neighbor, obj_value

    def ObjectiveFunction(self, state):
        straight_line_count = 0

        for i in range(0, self.n - 1):
            for j in range(i + 1, self.n):
                if j - i == abs(state[i] - state[j]):   # 대각선 위치
                    straight_line_count += 1

        return straight_line_count

problem = Problem()

# start_time으로부터 max_time이 경과하였는지 검사
def TimeOver(start_time, max_time):
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    return True if elapsed >= max_time else False

# 온도(T) 스케줄링 함수
def Schedule(T):
    T = T * 0.9
    if T < 0.00001:
        T = 0.00001
    return T

# Simulated Annealing
def SimulatedAnnealing():
    current, cur_obj_value = problem.GetInitialSolution()
    best, best_obj_value = current, cur_obj_value
    print(">>> 초기해 목적 함수값 :", cur_obj_value)
    print(">>> 초기해 :", current)
    start_time = datetime.datetime.now()        # 탐색 시작 시간 저장

    T = 10

    while True:
        neighbor, neigbor_obj_value = problem.GetANeighbor(current)
        deltaE = neigbor_obj_value - cur_obj_value
        if neigbor_obj_value <= cur_obj_value:
            current, cur_obj_value = neighbor, neigbor_obj_value
            print(f"{cur_obj_value}, {T}")
            if cur_obj_value < best_obj_value:
                best, best_obj_value = current, cur_obj_value
        else:
            move_probability = math.exp(-deltaE / T)
            if random.random() < move_probability:
                current, cur_obj_value = neighbor, neigbor_obj_value
                print(f"{cur_obj_value}, {T}")

        T = Schedule(T)

        if cur_obj_value == 0:      # 최적해의 값을 미리 알고 있다면
            print("최적해 발견!!!")
            break

        if TimeOver(start_time, problem.max_exe_time):
            print("실행 시간 초과")
            break

    return best, best_obj_value

best_solution, best_obj_value = SimulatedAnnealing()
print(">>> Best 목적 함수값 :", best_obj_value)
print(">>> Best 해 :", best_solution)

import random
import copy
import datetime
import math

# One Max Problem : 20개의 변수(0 또는 1의 값을 가짐)들의 합을 최대화
class Problem:
    def __init__(self):
        self.n = 20         # 20개의 변수 존재
        self.max_exe_time = 30  # 최대 수행 시간 30초

    def GetInitialSolution(self):
        # n개의 무작위 0 또는 0의 값을 갖는 리스트 생성
        solution = [random.randint(0, 1) for i in range(self.n)]
        return solution, self.ObjectiveFunction(solution)

    def GetANeighbor(self, state):
        neighbor = copy.copy(state)
        pos = random.randint(0, self.n - 1)
        neighbor[pos] = 1 if neighbor[pos] == 0 else 0
        obj_value = self.ObjectiveFunction(neighbor)

        return neighbor, obj_value

    def ObjectiveFunction(self, state):
        return sum(state)

problem = Problem()

# start_time으로부터 max_time이 경과하였는지 검사
def TimeOver(start_time, max_time):
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    return True if elapsed >= max_time else False

# 온도(T) 스케줄링 함수
def Schedule(T):
    T = T * 0.999
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
        if neigbor_obj_value >= cur_obj_value:
            current, cur_obj_value = neighbor, neigbor_obj_value
            print(f"{cur_obj_value}, {T}")
            if cur_obj_value > best_obj_value:
                best, best_obj_value = current, cur_obj_value
        else:
            move_probability = math.exp(deltaE / T)
            if random.random() < move_probability:
                current, cur_obj_value = neighbor, neigbor_obj_value
                print(f"{cur_obj_value}, {T}")

        T = Schedule(T)

        if TimeOver(start_time, problem.max_exe_time):
            print("실행 시간 초과")
            break

    return best, best_obj_value

best_solution, best_obj_value = SimulatedAnnealing()
print(">>> Best 목적 함수값 :", best_obj_value)
print(">>> Best 해 :", best_solution)

import random
import copy
import datetime

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

# First-choice Hill-climbing Search
def FirstChoiceHillClimbingSearch():
    current, cur_obj_value = problem.GetInitialSolution()
    print(">>> 초기해 목적 함수값 :", cur_obj_value)
    print(">>> 초기해 :", current)
    start_time = datetime.datetime.now()        # 탐색 시작 시간 저장

    while True:
        neighbor, neigbor_obj_value = problem.GetANeighbor(current)
        if neigbor_obj_value >= cur_obj_value:
            current, cur_obj_value = neighbor, neigbor_obj_value
            print(cur_obj_value)

        if TimeOver(start_time, problem.max_exe_time):
            print("실행 시간 초과")
            break

    return current, cur_obj_value

best_solution, best_obj_value = FirstChoiceHillClimbingSearch()
print(">>> Best 목적 함수값 :", best_obj_value)
print(">>> Best 해 :", best_solution)

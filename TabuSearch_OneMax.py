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

    def GetHighestValuedNeighbor(self, state, tabu_list, best_obj_value):
        highest_solutions = []
        highest_value = -10000

        for i in range(self.n):
            state[i] = 1 if state[i] == 0 else 0    # 1개 비트 변경
            obj_value = self.ObjectiveFunction(state)
            # tabu_list에 없거나 aspiration 기준(best보다 좋음)을 만족한다면
            if tabu_list[i] == 0 or obj_value > best_obj_value:
                if obj_value > highest_value:
                    highest_solutions = [[copy.copy(state), i]]
                    highest_value = obj_value
                elif obj_value == highest_value:
                    highest_solutions.append([copy.copy(state), i])
            state[i] = 1 if state[i] == 0 else 0    # 복구

        return_solution = random.choice(highest_solutions)
        return return_solution[0], highest_value, return_solution[1]

    def ObjectiveFunction(self, state):
        return sum(state)

problem = Problem()

# start_time으로부터 max_time이 경과하였는지 검사
def TimeOver(start_time, max_time):
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    return True if elapsed >= max_time else False

# Tabu Search
def TabuSearch():
    tabu_list = [0 for i in range(problem.n)]
    current, cur_obj_value = problem.GetInitialSolution()
    best, best_obj_value = current, cur_obj_value
    print(">>> 초기해 목적 함수값 :", cur_obj_value)
    print(">>> 초기해 :", current)
    start_time = datetime.datetime.now()        # 탐색 시작 시간 저장

    while True:
        neighbor, neigbor_obj_value, pos = \
            problem.GetHighestValuedNeighbor(current, tabu_list, best_obj_value)
        current, cur_obj_value = neighbor, neigbor_obj_value
        print(cur_obj_value)
        if cur_obj_value > best_obj_value:
            best, best_obj_value = current, cur_obj_value

        for i in range(problem.n):
            tabu_list[i] = max(0, tabu_list[i] - 1)
            tabu_list[pos] =3

        if TimeOver(start_time, problem.max_exe_time):
            print("실행 시간 초과")
            break

    return best, best_obj_value

best_solution, best_obj_value = TabuSearch()
print(">>> Best 목적 함수값 :", best_obj_value)
print(">>> Best 해 :", best_solution)

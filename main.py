import random
import copy
import datetime
import math

# One Max Problem : 20개의 변수(0 또는 1의 값을 가짐)들의 합을 최대화
class Problem:
    def __init__(self):
        infile = open("tsp299.txt", "r")
        data = infile.read().split()
        data = [eval(x) for x in data]
        self.city_count = data[0]  # 5 [0, 1, 2, 3, 도시가 개라면 도시 번호는 4]
        data.pop(0)
        pos_x = []
        pos_y = []
        for i in range(0, self.city_count * 3, 3):
            pos_x.append(data[i + 1])
            pos_y.append(data[i + 2])
        self.distance = []
        for i in range(self.city_count):
            self.distance.append([])
            for j in range(self.city_count):
                self.distance[i].append(0)
        for i in range(self.city_count - 1):
            for j in range(i + 1, self.city_count):
                self.distance[i][j] = int(math.sqrt((pos_x[i] - pos_x[j]) ** 2 + (pos_y[i] - pos_y[j]) ** 2))
                self.distance[j][i] = self.distance[i][j]
        self.max_exe_time = 600  # 최대 수행 시간 30초

    def Swap(self, state, i, j):
        # 주어진 순열에서 i번째와 j번째 요소를 교환한 새로운 순열 생성
        neighbor = copy.copy(state)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    def GetInitialSolution(self):
        # 0부터 n-1까지의 순열 생성
        solution = list(range(self.city_count))
        random.shuffle(solution)
        return solution, self.ObjectiveFunction(solution)

    def GetHighestValuedNeighbor(self, state, tabu_list, best_obj_value):
        highest_solutions = []
        highest_value = math.inf

        for i in range(self.city_count - 1):
            for j in range(1 + i, self.city_count):
                neighbor = self.Swap(state, i, j)
                obj_value = self.ObjectiveFunction(neighbor)
                # tabu_list에 없거나 aspiration 기준(best보다 좋음)을 만족한다면
                if tabu_list[i][j] == 0 or obj_value < best_obj_value:
                    if obj_value < highest_value:
                        highest_solutions = [[copy.copy(neighbor), i, j]]
                        highest_value = obj_value
                    elif obj_value == highest_value:
                        highest_solutions.append([copy.copy(neighbor), i, j])

        return_solution = random.choice(highest_solutions)
        return return_solution[0], highest_value, return_solution[1], return_solution[2]

    def ObjectiveFunction(self, state):
        # 주어진 순열에 대한 비용 계산SS
        cost = 0
        for i in range(self.city_count - 1):
            cost += self.distance[state[i]][state[i+1]]
        cost += self.distance[state[self.city_count-1]][state[0]]
        return cost


problem = Problem()


# start_time으로부터 max_time이 경과하였는지 검사
def TimeOver(start_time, max_time):
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    return True if elapsed >= max_time else False


# Tabu Search
def TabuSearch():
    tabu_list = [[0 for j in range(problem.city_count)] for i in range(problem.city_count)]
    current, cur_obj_value = problem.GetInitialSolution()
    best, best_obj_value = current, cur_obj_value
    print(">>> 초기해 목적 함수값 :", cur_obj_value)
    print(">>> 초기해 :", current)
    start_time = datetime.datetime.now()  # 탐색 시작 시간 저장

    while True:
        neighbor, neigbor_obj_value, i, j = problem.GetHighestValuedNeighbor(current, tabu_list, best_obj_value)
        current, cur_obj_value = neighbor, neigbor_obj_value
        print(cur_obj_value)
        if cur_obj_value < best_obj_value:
            best, best_obj_value = current, cur_obj_value

        for i in range(problem.city_count):
            for j in range(problem.city_count):
                tabu_list[i][j] = max(0, tabu_list[i][j] - 1)
                if i == j:
                    continue
                if [i, j] in [[ii, jj] for ii, jj in enumerate(best)]:
                    tabu_list[i][j] = 3

        if TimeOver(start_time, problem.max_exe_time):
            print("실행 시간 초과")
            break

    return best, best_obj_value


best_solution, best_obj_value = TabuSearch()
print(">>> Best 목적 함수값 :", best_obj_value)
print(">>> Best 해 :", best_solution)

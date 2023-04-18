import random
import copy
import datetime
import math

def GetDistance(coord1, coord2):  # 두 도시간의 거리
    # 첫번째 튜플의 x축과 y축, 두번째 튜플의 x축과 y축을 이용해 거리 계산
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# One Max Problem : 20개의 변수(0 또는 1의 값을 가짐)들의 합을 최대화
class Problem:
    def __init__(self):
        file = open("tsp299.txt", "r", encoding="UTF-8")
        numbers = file.read().split()  # 파일 내용을 공백단위로 나눠서 저장
        numbers = [eval(i) for i in numbers]  # 믄자열로 들어온 numbers를 eval로 int형으로 변환

        city_count = numbers[0]
        # city_count = 15 #도시 개수
        cities = []  # 도시 좌표(x, y)

        for i in range(2, len(numbers), 3):
            coord = (numbers[i], numbers[i + 1])  # 각 도시의 x축,y축를 튜플로 변환
            cities.append(coord)  # 각 도시의 좌표를 (x,y)형식으로 저장

        # 행렬 생성(city_count * city_count)
        distance = [[0 for i in range(city_count)] for j in range(city_count)]

        for i in range((city_count - 1)):
            for j in range(i + 1, city_count):
                distance[i][j] = GetDistance(cities[i], cities[j])  # i번째 x축과 j번째 y축을 얻어와 거리 계산
                distance[j][i] = distance[i][j]  # 행렬 밑부분

        self.n = city_count      # 20개의 변수 존재
        self.max_exe_time = 600  # 최대 수행 시간 30초
        self.distance = distance
    def GetInitialSolution(self):
        solution = list(range(self.n))
        return solution, self.ObjectiveFunction(solution)

    def GetANeighbor(self, state):
        neighbor = copy.copy(state)
        pos1 = random.randint(0, self.n - 1)
        pos2 = random.randint(0, self.n - 1)
        neighbor[pos1], neighbor[pos2] = neighbor[pos2], neighbor[pos1]
        obj_value = self.ObjectiveFunction(neighbor)

        return neighbor, obj_value

    def ObjectiveFunction(self, state):
        cost = 0
        for i in range(self.n):
            cost += self.distance[state[i]][state[(i + 1) % self.n]]
        return cost

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
        if neigbor_obj_value < cur_obj_value:
            current, cur_obj_value = neighbor, neigbor_obj_value
            print(cur_obj_value)

        if TimeOver(start_time, problem.max_exe_time):
            print("실행 시간 초과")
            break

    return current, cur_obj_value

best_solution, best_obj_value = FirstChoiceHillClimbingSearch()
print(">>> Best 목적 함수값 :", int(best_obj_value+5))
print(">>> Best 해 :", best_solution)

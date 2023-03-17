"""
2주차 - 과제 : 순회 외판원 문제
"""

import math
import itertools
import tkinter as tk
import threading
import time

file = open("point20.txt", "r", encoding="UTF-8")
numbers = file.read().split() #파일 내용을 공백단위로 나눠서 저장
numbers = [eval(i) for i in numbers] #믄자열로 들어온 numbers를 eval로 int형으로 변환
print(numbers)

#city_count = numbers[0]
city_count = 8 #도시 개수
cities = [] #도시 좌표(x, y)

for i in range(1, len(numbers), 2):
    coord = (numbers[i], numbers[i+1]) #각 도시의 x축,y축를 튜플로 변환
    cities.append(coord) #각 도시의 좌표를 (x,y)형식으로 저장

#print(cities)

def GetDistance(coord1, coord2): #두 도시간의 거리
    #첫번째 튜플의 x축과 y축, 두번째 튜플의 x축과 y축을 이용해 거리 계산
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

#행렬 생성(city_count * city_count)
distance = [[0 for i in range(city_count)] for j in range(city_count)]

for i in range(city_count - 1) :
    for j in range(i + 1, city_count) :
        distance[i][j] = GetDistance(cities[i], cities[j]) #i번째 x축과 j번째 y축을 얻어와 거리 계산
        distance[j][i] = distance[i][j] #행렬 밑부분
        # 추가설명 : city_count = 7일때를 가정
        # 7*7행렬을 만들되, U부분과 D부분은 대칭되게 한다.
        # 즉, U부분을 작성하고 D부분은 distance[j][i] = distance[i][j]를 해주면 대칭이 된다
        # U부분은 i와 j는 두 도시들을 대표하는데, 만약 i와 j가 같은 도시이면 distance는 0이 된다.
        # 이를 통해 i번째 도시와 j번째 도시의 거리는 행렬 [i][j]번째를 확인하면 된다.

#print(distance)

def GetTourDistance(path):
    # 총 여행한 길이
    dist = distance[0][path[0]] #전체 첫 도시와 매개변수의 첫 도시의 거리

    #모든 도시를 순회했을때의 길이
    for i in range(len(path) - 1):
        dist += distance[path[i]][path[i + 1]] #두번째와 세번째, 세번째랑 네번째, ...

    dist += distance[path[-1]][0] #마지막도시와 다시 첫번째도시의 거리
    return dist

#시작 도시를 제외한 처음부터 4번째까지의 도시의 거리
#print(GetTourDistance([1,2,3,4]))

def FindShortestPath():
    start = time.time()
    math.factorial(100000)
    # 최단 경로 찾기
    # itertools : 효울적인 반복을 위한 함수

    # permutation : 반복 가능 개체 중에서 r개를 선택한 순열을 반환한 것
    iter = itertools.permutations(range(1, city_count))
    min_tour_length = math.inf  # 최단시간값을 무한으로 설정
    shortest_path = None

    for path in iter:
        length = GetTourDistance(path)  # 총 거리 계산

        if length < min_tour_length:  # 총 거리 계산이 최소값이 되도록
            print(length, path)
            min_tour_length = length
            shortest_path = path
            DrawTour([0] + list(path))  # canvas에 첫도시부터 순서대로 그리기
            lb.config(text=length)
    print("탐색 끝")
    end = time.time()
    lb2.config(text=f"{end - start:.5f} sec")

def DrawTour(path):
    canvas.delete(tk.ALL) #기존 그림 삭제
    for i in range(len(path)):
        x, y = cities[path[i]] #경로
        if path[i] == 0:
            color = "red"
        else:
            color = "blue"
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color)

        if i == city_count - 1:
            next_x, next_y = cities[0]
        else:
            next_x, next_y = cities[path[i + 1]]
        canvas.create_line(x, y, next_x, next_y)

window = tk.Tk()
canvas = tk.Canvas(window, width = 600, height = 600, bg = "white")
canvas.pack(expand = 1, fill = tk.BOTH)
lb = tk.Label(window, text = 0)
lb.pack(fill=tk.X)
lb2 = tk.Label(window, text = 0)
lb2.pack(fill=tk.X)
btn = tk.Button(window, text="Start", command=lambda: threading.Thread(target=FindShortestPath).start())
btn.pack(fill=tk.X, side="right", expand=True)
btn2 = tk.Button(window, text = "Step")
btn2.pack(fill=tk.X, side="right", expand=True)
DrawTour(list(range(city_count))) #city_count만큼 도시 점 생성

window.mainloop()



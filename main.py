"""
2주차 - 실습 : 숫자 데이터 쓰기 및 읽기
"""

import math
import itertools
import tkinter as tk
import threading

file = open("point20.txt", "r", encoding="UTF-8")
numbers = file.read().split()
numbers = [eval(i) for i in numbers]
print(numbers)

#city_count = numbers[0]
city_count = 10 #도시 개수
cities = [] #도시 좌표(x, y)

for i in range(1, len(numbers), 2):
    coord = (numbers[i], numbers[i+1]) #각 도시의 x축,y축
    cities.append(coord)#각 도시의 좌표를 (x,y)형식으로 저장

#print(cities)

def GetDistance(coord1, coord2): #두 도시간의 거리
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

distance = [[0 for i in range(city_count)] for j in range(city_count)] #행렬 생성
for i in range(city_count - 1) :
    for j in range(i + 1, city_count) :
        distance[i][j] = GetDistance(cities[i], cities[j]) #i번째 x축과 j번째 y축을 얻어와 거리 계산
        distance[j][i] = distance[i][j] #행렬 밑부분

#print(distance)

def GetTourDistance(tour):
    dist = distance[0][tour[0]]

    for i in range(len(tour) - 1):
        dist += distance[tour[i]][tour[i+1]]

    dist += distance[tour[-1]][0]
    return dist

print(GetTourDistance([1,2,3,4]))

def GetOptimalPath():
    iter = itertools.permutations(range(1, city_count))
    min_tour_length = math.inf

    for tour in iter:
        length = GetTourDistance(tour)

        if length < min_tour_length:
            print(length)
            min_tour_length = length
            DrawTour(tour)

"""
def DrawFirstTour():
    tour = list(range(city_count))
    for i in tour:
        x,y = cities[i]
        if i == 0:
            color = "red"
        else:
            color = "blue"
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill = color)

        if i == city_count - 1:
            next_x, next_y = cities[0]
        else:
            next_x,next_y = cities[i + 1]
        canvas.create_line(x, y, next_x, next_y)
"""

def DrawTour(tour):
    canvas.delete(tk.ALL)
    x, y = cities[0]
    canvas.create_oval(x-3,y-3,x+3,y+3, fill="red")
    for i in range(len(tour)):
        prev_x = x
        prev_y = y
        x,y = cities[tour[i]]
        color = "blue"
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill = color)
        canvas.create_line(prev_x, prev_y, x, y)
    prev_x = x
    prev_y = y
    x, y = cities[0]
    canvas.create_line(prev_x, prev_y, x, y)

window = tk.Tk()
canvas = tk.Canvas(window, width = 600, height = 600, bg = "white")
canvas.pack()
btn = tk.Button(window, text = "Start", command = lambda : threading.Thread(target=GetOptimalPath()).start())
btn.pack(fill=tk.BOTH)
DrawTour(list(range(city_count)))

window.mainloop()

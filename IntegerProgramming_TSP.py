import math

class Problem:
    def __init__(self):
        infile = open("tsp_data.txt", "r")
        data = infile.read().split()
        data = [eval(x) for x in data]
        self.city_count = data[0]  # 도시가 5개라면 도시 번호는 [0, 1, 2, 3, 4]
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

tsp = Problem()

from docplex.mp.model import Model

model = Model("Traveling Salesman Problem")

city_range = range(0, tsp.city_count)
x = model.binary_var_matrix(city_range, city_range, name = "X")
model.minimize(model.sum(tsp.distance[i][j] * x[i, j]
                         for i in city_range for j in city_range))
model.add_constraints(x[i, i] == 0 for i in city_range)     # 반드시 들어가야 되는 듯 ???
model.add_constraints(model.sum(x[i, j] for j in city_range) == 1 for i in city_range)
model.add_constraints(model.sum(x[i, j] for i in city_range) == 1 for j in city_range)

u = model.continuous_var_list(tsp.city_count, 0, model.infinity, name = "U")
for i in range(1, tsp.city_count):
    for j in range(1, tsp.city_count):
        if i != j:
            model.add_constraint(u[i] + 1 <= u[j] + tsp.city_count * (1 - x[i, j]))

msol = model.solve(log_output = False)
print(msol)

solution_list = [0]
current_city = 0
distance = 0
while True:
    for i in city_range:
        if msol.get_value(x[current_city, i]) == 1:
            next_city = i
            break
    distance += tsp.distance[current_city][next_city]
    solution_list.append(next_city)
    current_city = next_city
    if current_city == 0:
        break

print("solution :", solution_list)
print("distance :", distance)

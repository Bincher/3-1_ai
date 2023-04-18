class Problem:
    def __init__(self):
        infile = open("knapsack_data.txt", "r")
        data = infile.read().split()
        data = [eval(x) for x in data]
        self.item_count = data[0]
        data.pop(0)
        self.max_weight = data[0]
        data.pop(0)
        self.item_data = []
        for i in range(0, len(data), 2):
            temp = [data[i], data[i + 1]]
            self.item_data.append(temp)
        infile.close()

problem = Problem()

from docplex.mp.model import Model

model = Model("Knapsack Problem")

x = model.binary_var_list(problem.item_count, name = "X")

obj_expr = 0
constraint_expr = 0
for i in range(problem.item_count):
    obj_expr += problem.item_data[i][0] * x[i]
    constraint_expr += problem.item_data[i][1] * x[i]
model.maximize(obj_expr)
model.add_constraint(constraint_expr <= problem.max_weight)

msol = model.solve(log_output = True)
print(f'objective : {msol.get_objective_value()}')
for i in range(problem.item_count):
    print(f'x[{i}] = {msol.get_value(x[i])}')
print()
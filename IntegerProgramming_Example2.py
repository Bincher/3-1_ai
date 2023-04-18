from docplex.mp.model import Model

model = Model("test")

x = model.binary_var_list(4, name = "X")

model.maximize(7 * x[0] + 6 * x[1] + 2 * x[2] + 3 * x[3])
model.add_constraint(10 * x[0] + 76 * x[1] + 774 * x[2] + 42 * x[3] <= 875)
model.add_constraint(794 * x[0] + 27 * x[1] + 67 * x[2] + 53 * x[3] <= 875)

msol = model.solve()
print(f'objective : {msol.get_objective_value()}')
for i in range(4):
    print(f'x[{i}] = {msol.get_value(x[i])}')


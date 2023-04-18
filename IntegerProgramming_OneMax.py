from docplex.mp.model import Model

model = Model("test")

x = model.binary_var_list(20, name = "X")

expr = 0
for i in range(20):
    expr += x[i]
model.maximize(expr)

msol = model.solve()
print(f'objective : {msol.get_objective_value()}')
for i in range(20):
    print(f'x[{i}] = {msol.get_value(x[i])}')


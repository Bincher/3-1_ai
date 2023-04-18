# 목적함수   : Minimize x1 - x2 + 2x3 - 3x4
# 제약조건 1 : 2x1 + 3x2 - 2x3 >= -1
# 제약조건 2 : x2 - 2x3 + 1.5x4 <= 8
# 제약조건 3 : -x1 + x2 + 3x3 + x4 <= 12
#            x1, x2, x3, x4 >= 0
from docplex.mp.model import Model

model = Model("test")

x = model.continuous_var_list(4, lb = 0, name = "X")

expr = 0
expr += x[0] - x[1]
expr += 2 * x[2] - 3 * x[3]
model.minimize(expr)
model.add_constraint(2 * x[0] + 3 * x[1] - 2 * x[2] >= -1)
model.add_constraint(x[1] - 2 * x[2] + 1.5 * x[3] <= 8)
model.add_constraint((-1) * x[0] + x[1] + 3 * x[2] + x[3] <= 12)

msol = model.solve()
#print(msol)
print(f'objective : {msol.get_objective_value()}')
for i in range(4):
    print(f'x[{i}] = {msol.get_value(x[i])}')


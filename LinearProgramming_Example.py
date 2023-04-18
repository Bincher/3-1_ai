# 목적함수   : Maximize 4x1 + 5x2
# 제약조건 1 : x1 + 2x2 <= 4
# 제약조건 2 : 4x1 + 3x2 <= 12
#            x1 >= 0
#            x2 >= 0
from docplex.mp.model import Model

model = Model("test")

x1 = model.continuous_var(lb = 0, name = "X1")
x2 = model.continuous_var(lb = 0, name = "X2")

model.maximize(4 * x1 + 5 * x2)
model.add_constraint(x1 + 2 * x2 <= 4)
model.add_constraint(4 * x1 + 3 * x2 <= 12)

msol = model.solve()
print(msol)

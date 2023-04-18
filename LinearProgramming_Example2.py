# 목적함수   : Minimize x1 - x2 + 2x3 - 3x4
# 제약조건 1 : 2x1 + 3x2 - 2x3 >= -1
# 제약조건 2 : x2 - 2x3 + 1.5x4 <= 8
# 제약조건 3 : -x1 + x2 + 3x3 + x4 <= 12
#            x1, x2, x3, x4 >= 0
from docplex.mp.model import Model

model = Model("test")

x1 = model.continuous_var(lb = 0, name = "X1")
x2 = model.continuous_var(lb = 0, name = "X2")
x3 = model.continuous_var(lb = 0, name = "X3")
x4 = model.continuous_var(lb = 0, name = "X4")

model.minimize(x1 - x2 + 2 * x3 - 3 * x4)
model.add_constraint(2 * x1 + 3 * x2 - 2 * x3 >= -1)
model.add_constraint(x2 - 2 * x3 + 1.5 * x4 <= 8)
model.add_constraint((-1) * x1 + x2 + 3 * x3 + x4 <= 12)

msol = model.solve()
print(msol)


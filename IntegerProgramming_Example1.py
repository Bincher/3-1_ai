from docplex.mp.model import Model

model = Model("test")

x1 = model.integer_var(lb = 0, name = "X1")
x2 = model.integer_var(lb = 0, name = "X2")

model.maximize(13 * x1 + 8 * x2)
model.add_constraint(x1 + 2 * x2 <= 10)
model.add_constraint(5 * x1 + 2 * x2 <= 20)

msol = model.solve()
print(msol)


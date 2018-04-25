from gurobipy import *

#----------- Gurobi model --------------------

m = Model("Giapetto")

N = m.addVar(3, name = "N")

FinishingHours = m.addVars([(1, 2), (2, 1), (3, 2)])

CarpentryHours = m.addVars([(1, 1), (2, 1), (3, 2)])

DemandToys = m.addVars([(1, 40), (2, 500), (3, 200)])

ProfitToys = m.addVars([(1, 3), (2, 2), (3, 5)])

TotalFinHours = m.addVar(100)

TotalCarpHours = m.addVar(80)

MaxLowerLimit = m.addVar(20)

CoolToys = m.addVars([(1, 20), (2, 10)])

x = m.addVar(0)

obj = quicksum()
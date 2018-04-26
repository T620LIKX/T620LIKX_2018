from gurobipy import *


#----------- Gurobi model --------------------

m = Model("Giapetto")

data = [0, 1, 2]

x = m.addVars((0,1,2), lb = 0, vtype = GRB.INTEGER)

FinishingHours = tuplelist([2,1,2])
CarpentryHours = tuplelist([1,1,2])
DemandToys = tuplelist([40, 500, 200])
ProfitToys = tuplelist([3, 2, 5])
TotalFinHours = 100
TotalCarpHours = 80
MaxLowerLimit = 20
CoolToys = [(0,20), (1,10)]

FinHours = m.addConstrs((x[i]*FinishingHours[i] <= TotalFinHours for i in range(3)), name = 'FinHours')
CarpHours = m.addConstrs((x[i]*CarpentryHours[i] <= TotalCarpHours for i in range(3)), name = 'CarpHours')
Demand = m.addConstrs((x[i] <= DemandToys[i] for i in range(3)), name = 'Demand')
LowerLimitOnCoolToys = m.addConstrs((x[ct[0]] >= ct[1] for ct in CoolToys), name = 'LowerLimitOnCoolToys')

goal = quicksum(ProfitToys[i]*x[i] for i in range(3))

obj = m.setObjective(goal, GRB.MAXIMIZE)

m.optimize()

m.write('solution.lp')

for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus

# Define the problem
model = LpProblem(name="multi-stage-resource-allocation", sense=LpMaximize)

# Define the decision variables for multiple products, shifts, and overtime
products = ['X', 'Y', 'Z']
shifts = ['Shift1', 'Shift2', 'Overtime']

# Create decision variables for each product in each shift
production_vars = {f'{product}_{shift}': LpVariable(name=f'{product}_{shift}', lowBound=0) for product in products for shift in shifts}

# Objective function: Maximize profit for each product in each shift
profits = {
    'X_Shift1': 50, 'X_Shift2': 55, 'X_Overtime': 45,
    'Y_Shift1': 40, 'Y_Shift2': 42, 'Y_Overtime': 38,
    'Z_Shift1': 60, 'Z_Shift2': 65, 'Z_Overtime': 58
}
model += lpSum([profits[var] * production_vars[var] for var in production_vars]), "Total_Profit"

# Constraints
# Labor hours constraints for each shift
labor_hours = {'Shift1': 300, 'Shift2': 350, 'Overtime': 150}
model += lpSum([3 * production_vars[f'X_Shift1'] + 4 * production_vars[f'Y_Shift1'] + 5 * production_vars[f'Z_Shift1']]) <= labor_hours['Shift1'], "Labor_Hours_Shift1"
model += lpSum([3 * production_vars[f'X_Shift2'] + 4 * production_vars[f'Y_Shift2'] + 5 * production_vars[f'Z_Shift2']]) <= labor_hours['Shift2'], "Labor_Hours_Shift2"
model += lpSum([4 * production_vars[f'X_Overtime'] + 5 * production_vars[f'Y_Overtime'] + 6 * production_vars[f'Z_Overtime']]) <= labor_hours['Overtime'], "Labor_Hours_Overtime"

# Raw material constraints (shared across shifts)
model += lpSum([
    2 * production_vars[f'X_Shift1'] + 2 * production_vars[f'X_Shift2'] + 2 * production_vars[f'X_Overtime'] +
    3 * production_vars[f'Y_Shift1'] + 3 * production_vars[f'Y_Shift2'] + 3 * production_vars[f'Y_Overtime'] +
    4 * production_vars[f'Z_Shift1'] + 4 * production_vars[f'Z_Shift2'] + 4 * production_vars[f'Z_Overtime']
]) <= 700, "Material_Constraint"

# Production capacity constraints for each product
model += lpSum([production_vars[f'X_Shift1'], production_vars[f'X_Shift2'], production_vars[f'X_Overtime']]) <= 120, "Max_Capacity_X"
model += lpSum([production_vars[f'Y_Shift1'], production_vars[f'Y_Shift2'], production_vars[f'Y_Overtime']]) <= 160, "Max_Capacity_Y"
model += lpSum([production_vars[f'Z_Shift1'], production_vars[f'Z_Shift2'], production_vars[f'Z_Overtime']]) <= 100, "Max_Capacity_Z"

# Demand satisfaction constraint (minimum required production)
demand = {'X': 80, 'Y': 100, 'Z': 60}
model += lpSum([production_vars[f'X_Shift1'], production_vars[f'X_Shift2'], production_vars[f'X_Overtime']]) >= demand['X'], "Min_Demand_X"
model += lpSum([production_vars[f'Y_Shift1'], production_vars[f'Y_Shift2'], production_vars[f'Y_Overtime']]) >= demand['Y'], "Min_Demand_Y"
model += lpSum([production_vars[f'Z_Shift1'], production_vars[f'Z_Shift2'], production_vars[f'Z_Overtime']]) >= demand['Z'], "Min_Demand_Z"

# Solve the problem
status = model.solve()

# Print results
print(f"Status: {LpStatus[model.status]}")
for var in production_vars.values():
    print(f"Optimal value for {var.name}: {var.varValue}")
print(f"Maximum profit: {model.objective.value()}")
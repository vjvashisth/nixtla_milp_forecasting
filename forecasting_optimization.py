import pandas as pd
import numpy as np
from neuralforecast import NeuralForecast
from neuralforecast.models import NHITS  
from gurobipy import Model, GRB, quicksum
import matplotlib.pyplot as plt

# Step 1: Generate Synthetic Demand Data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=180, freq='D')
demand = np.random.randint(50, 200, size=(180,)) + 10 * np.sin(np.linspace(0, 20, 180))

data = pd.DataFrame({'ds': dates, 'y': demand, 'unique_id': 'product_A'})

# Step 2: Train Nixtla's NHITS Forecasting Model
model = NeuralForecast(models=[NHITS(h=30, input_size=60, max_steps=100)], freq='D')
model.fit(data)
forecast = model.predict()

# Step 3: Prepare Forecast Output for Optimization
forecast_values = forecast['NHITS'].values[:30]  # Forecast next 30 days
demand_forecast = {i: forecast_values[i] for i in range(30)}

# Step 4: MILP Model for Inventory Optimization
sites = list(range(5))  # 5 Warehouses
inventory_capacity = {i: 500 for i in sites}  # Capacity per warehouse
holding_cost = {i: 2 for i in sites}  # Cost per unit stored
order_cost = {i: 10 for i in sites}  # Cost per order placed

days = list(range(30))  # Planning horizon

model = Model("Inventory Optimization")

# Decision Variables: Inventory levels and order quantities
x = model.addVars(sites, days, vtype=GRB.CONTINUOUS, name="inventory")
o = model.addVars(sites, days, vtype=GRB.BINARY, name="order")

# Objective Function: Minimize costs
model.setObjective(
    quicksum(holding_cost[i] * x[i, t] for i in sites for t in days) +
    quicksum(order_cost[i] * o[i, t] for i in sites for t in days),
    GRB.MINIMIZE
)

# Constraints
for t in days:
    for i in sites:
        if t == 0:
            model.addConstr(x[i, t] >= demand_forecast[t])  # Ensure enough stock initially
        else:
            model.addConstr(x[i, t] >= x[i, t-1] - demand_forecast[t] + o[i, t] * 100)  # Allow flexibility
        model.addConstr(x[i, t] <= inventory_capacity[i])  # Capacity Constraint

# Solve the Model
model.optimize()

# Check if model is feasible
if model.status == GRB.INFEASIBLE:
    print("Model is infeasible. Running feasibility analysis...")
    model.computeIIS()
    model.write("infeasible_model.ilp")
else:
    # Extract Results
    optimized_inventory = {t: sum(x[i, t].x for i in sites) for t in days}

    # Plot Forecast vs Optimized Inventory
    plt.figure(figsize=(10, 5))
    plt.plot(days, forecast_values, label='Forecasted Demand', linestyle='dashed', marker='o')
    plt.plot(days, [optimized_inventory[t] for t in days], label='Optimized Inventory', marker='s')
    plt.xlabel("Days")
    plt.ylabel("Units")
    plt.legend()
    plt.title("Nixtla Forecast vs MILP-Optimized Inventory")
    plt.show()

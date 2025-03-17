# Nixtla-Based Forecasting & MILP Optimization for Supply Chain Planning

## Overview
This repository implements an **AI-driven supply chain forecasting and optimization model** combining:
- **Nixtla's NeuralForecast** for multi-horizon demand forecasting.
- **Mixed-Integer Linear Programming (MILP) with Gurobi** for inventory optimization.
- **Hierarchical Forecasting** to improve SKU and warehouse-level decision-making.

## Features
- ✅ **Forecast future demand** using Nixtla's NHITS deep learning model.
- ✅ **Optimize inventory levels** using MILP to minimize costs.
- ✅ **Integrate forecasting & optimization** into a single pipeline.
- ✅ **Visualize forecast vs optimized inventory levels** to compare efficiency.
- ✅ **Feasibility analysis for MILP**—handles infeasible solutions dynamically.

## Installation
Before running the code, install the required dependencies:

```bash
pip install pandas numpy matplotlib gurobipy neuralforecast torch torchvision torchaudio
```

Ensure you have a **Gurobi license** (even a free academic license works). You can set it up using:

```bash
gurobi_cl --license
```

## How It Works
### 1️⃣ Demand Forecasting with Nixtla
- Uses NHITS (Neural Hierarchical Interpolation for Time Series) to predict future demand for 30 days.
- Trains on synthetic demand data with seasonal variations.

### 2️⃣ Inventory Optimization with MILP
- Defines a Mixed-Integer Linear Programming (MILP) model.
- **Decision variables:**
  - **Inventory levels** per warehouse.
  - **Order quantities** for stock replenishment.
- **Objective function minimizes:**
  - **Holding costs** (cost per unit stored).
  - **Order costs** (cost per stock replenishment).

### 3️⃣ Feasibility Check & Visualization
- If the model is infeasible, it runs `computeIIS()` to diagnose issues.
- Generates a **forecast vs optimized inventory plot** for comparison.

## Usage
Run the Python script:

```bash
python forecasting_optimization.py
```

## Expected Output
- Forecasted demand trends for the next 30 days.
- Optimized inventory decisions to minimize costs.
- A graph comparing forecast vs MILP-optimized inventory.

## Example Visualization
![image](https://github.com/user-attachments/assets/c55e6489-4bff-44f7-8347-751708987958)


## Next Steps & Enhancements
- 🔹 Extend the model to handle **multi-product forecasting & optimization**.
- 🔹 Use **real-world datasets** instead of synthetic demand data.
- 🔹 Experiment with **stochastic MILP** for uncertainty handling.
- 🔹 Deploy as an **API for real-time decision-making**.

## License
This project is for **non-commercial use only**, following Gurobi's free license restrictions.

## Author
👤 **Vijayendra Vashisth**  
📧 vijayendraaryan@gmail.com

---
### 🌟 *If you find this useful, give it a ⭐ on GitHub!*

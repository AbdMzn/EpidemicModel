import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import odeint

country = "France"
population = 67813000

document = pd.read_csv(f'worldometer_data/worldometer_data({country}).csv')
document['Date'] = pd.to_datetime(document['Date'])

start_date = pd.to_datetime('2020-02-15')
end_date = pd.to_datetime('2023-12-24')

quarters = pd.date_range(start=start_date, end=end_date, freq='Q') + pd.DateOffset(days=1)

for i in range(len(quarters)):
    quarter_start = quarters[i]
    if i == len(quarters) - 1:
        quarter_end = end_date
    else:
        quarter_end = quarters[i + 1] - pd.DateOffset(days=1)
    
    quarter_data = document[(document['Date'] >= quarter_start) & (document['Date'] <= quarter_end)]
    dates = quarter_data['Date'].values
    print(f"Q{i} start: {quarter_start}")
    diff = (quarter_end - quarter_start).days
    quarter_data = document[(document['Date'] >= quarter_start) & (document['Date'] <= quarter_end)]
    total_cases = quarter_data['Total Cases'].values
    active_cases = quarter_data['Active Cases'].values
    total_removed = quarter_data['Total Removed'].values
    total_susceptible = population - total_removed
    tspan = np.arange(0, diff+1)
    I = active_cases[0]
    N = population
    if i == 14:
        print(f"total removed: {total_removed[0]}")
        print(f"active_cases: {I}")
    def fitfuncRemoved(t, gamma):
        def Removed(R, t):
            return gamma * I
        
        R0 = total_removed[0]
        Rsol = odeint(Removed, R0, t)
        return Rsol[:,0]
    
    gamma, kcov = curve_fit(fitfuncRemoved, tspan, total_removed, p0=0.043)
    
    def fitfuncSusceptible(t, beta):
        def Susceptible(S, t):
            return - beta * I * S / N
        
        S0 = total_susceptible[0]
        Ssol = odeint(Susceptible, S0, t)
        return Ssol[:,0]

    beta, kcov = curve_fit(fitfuncSusceptible, tspan, total_susceptible, p0=0.05)

    print(f"Q{i} gamma: {gamma}, beta: {beta}")
print(f"{country}: found gamma/beta values")
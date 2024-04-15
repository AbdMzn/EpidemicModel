import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import odeint

def transmission_rate(country_input, population_input, document_name):
    country = country_input
    population = np.int64(population_input)
    
    try:
        document = pd.read_csv(f'worldometer_data/worldometer_data({country}).csv')
        document['Date'] = pd.to_datetime(document['Date'])

        start_date = pd.to_datetime('2020-02-15')
        end_date = pd.to_datetime('2023-12-24')

        quarters = pd.date_range(start=start_date, end=end_date, freq='Q') + pd.DateOffset(days=1)
        data = np.empty((len(quarters), 4), dtype=object)
        
        for i in range(len(quarters)):
            quarter_start = quarters[i]
            if i == len(quarters) - 1:
                quarter_end = end_date
            else:
                quarter_end = quarters[i + 1] - pd.DateOffset(days=1)
            
            quarter_data = document[(document['Date'] >= quarter_start) & (document['Date'] <= quarter_end)]
            dates = quarter_data['Date'].values
            #print(f"Q{i} start: {quarter_start}")
            diff = (quarter_end - quarter_start).days
            quarter_data = document[(document['Date'] >= quarter_start) & (document['Date'] <= quarter_end)]
            total_cases = quarter_data['Total Cases'].values
            active_cases = quarter_data['Active Cases'].values
            total_removed = quarter_data['Total Removed'].values
            total_susceptible = population - total_removed
            tspan = np.arange(0, diff+1)
            I = active_cases[0]
            N = population
            
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
            beta = beta[0]
            gamma = gamma[0]
            
            if I == 0:
                beta = 0
                gamma = 0
            
            data[i][0] = country
            data[i][1] = f"Q{i}"
            data[i][2] = beta
            data[i][3] = gamma
            #print(f"Q{i} gamma: {gamma}, beta: {beta}")
        print(f"{country}: found gamma/beta values")
        
        with open(f'{document_name}.csv', 'a', newline='') as file:
            writer = csv.writer(file)
        
            #writer.writerow(["Country", "Quarter", "Beta", "Gamma"])
            
            for entry in data:
                writer.writerow(entry)

    except Exception as e: 
        print(f"{country}: failed")
    
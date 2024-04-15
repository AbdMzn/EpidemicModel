import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import odeint
import math

days = 784
period_length = 7
period_number = np.uint64(math.ceil(days/period_length))
init_gamma = 0.043
population = 338289856
N = population
document = pd.read_csv(f'worldometer_data(us).csv')
total_cases = document['Total Cases'].values
active_cases = document['Active Cases'].values
total_removed = document['Total Removed'].values

tspan = np.arange(0, period_length)
gamma_values = np.zeros(period_number, dtype = np.float64)
beta_values_1 = np.zeros(period_number, dtype = np.float64)
beta_values_2 = np.zeros(period_number, dtype = np.float64)

for n in range(0, days, period_length):
    R_data = total_removed[n:period_length+n]
    I = active_cases[n]
    def fitfunc(t, gamma):
        def Removed(R, t):
            return gamma * I
        
        R0 = R_data[0]
        Rsol = odeint(Removed, R0, t)
        return Rsol[:,0]

    gamma, kcov = curve_fit(fitfunc, tspan, R_data, p0=0.043)
    m = np.uint64(n/period_length)
    gamma_values[m] = gamma


for n in range(0, days, period_length):
    I_data = active_cases[n:period_length+n]
    S = population - total_cases[n]
    m = np.uint64(n/period_length)
    gamma = gamma_values[m]
    
    def fitfunc(t, beta):
        def Infected(I, t):
            return beta * I * S / N - gamma * I
        
        I0 = I_data[0]
        Isol = odeint(Infected, I0, t)
        return Isol[:,0]

    beta, kcov = curve_fit(fitfunc, tspan, I_data, p0=0.05)
    beta_values_1[m] = beta

for n in range(0, days, period_length):
    S_data = population - total_cases[n:period_length+n]
    I = active_cases[n]
    m = np.uint64(n/period_length)
    
    def fitfunc(t, beta):
        def Susceptible(S, t):
            return - beta * I * S / N
        
        S0 = S_data[0]
        Ssol = odeint(Susceptible, S0, t)
        return Ssol[:,0]

    beta, kcov = curve_fit(fitfunc, tspan, S_data, p0=0.05)
    beta_values_2[m] = beta

time = np.arange(period_number)
plt.plot(time[10:], beta_values_1[10:], 'b-', label='beta (1)')
plt.plot(time[10:], beta_values_2[10:], 'r-', label='beta (2)')
plt.plot(time[10:], gamma_values[10:], 'b--', label='gamma')
plt.show()
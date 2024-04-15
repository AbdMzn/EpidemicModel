import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime, timedelta
from scipy.optimize import curve_fit, minimize
from scipy.integrate import odeint
import os


gamma = 0.043
days = 784
period_length = 7
period_number = np.uint64(days/period_length)
time = np.arange(0, days, 1)
init_gamma = 0.043
path_from = 'filtered_data'
with open('countries.txt', 'r') as file:
    countries = file.read().splitlines()
#beta_values = np.zeros((len(countries), period_number), dtype='float64')

country = 'Australia'
ihme_estimate = pd.read_csv(f'{path_from}/ihme_estimate.csv')
owid_data = pd.read_csv(f'{path_from}/owid-covid-data.csv')

criteria = ihme_estimate['Entity'] == country
ihme_estimate = ihme_estimate[criteria]
criteria = owid_data['location'] == country
owid_data = owid_data[criteria]

total_cases_per_million = np.nan_to_num(owid_data['total_cases_per_million'].values, nan=0)
total_cases = owid_data['total_cases_per_million'].values[0]
population  = owid_data['population'].values[0]
ihme_cases_mean = ihme_estimate['Daily new estimated infections of COVID-19 (IHME, mean)'].values
sus_f = 1 - (total_cases_per_million / 10**6)
beta_values = np.zeros(period_number)
#period_length = 7
tspan = np.linspace(0, period_length-1, period_length)

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    gamma = 0.043
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def objective(params, *args):
    beta, gamma = params
    y0, N, data_t, data_i = args

    ret = odeint(deriv, y0, data_t, args=(N, beta, gamma))
    error = np.sum((ret[:, 1] - data_i)**2)
    return error

i_0 = ihme_cases_mean[0] #infected start of period
i_1 = ihme_cases_mean[0 + period_length - 1] #infected end of period
ti_f =(total_cases_per_million[0] / 10**6) #total infected fraction
sus_f = 1 - (ti_f) #susceptible at start of period

beta_guess = ((i_1 - i_0)/period_length + gamma * i_0) / (i_0 * sus_f) if i_0 != 0 else 0
gamma_guess = 0.043
S0 = population - total_cases - i_0

for n in range(0, days, period_length):
    I_data = ihme_cases_mean[n:n+period_length]
    y0 = S0, I_data[0], population - I_data[0] - S0
    
    initial_guess = [beta_guess, gamma_guess]
    result = minimize(objective, initial_guess, args=(y0, population, tspan, I_data), method='L-BFGS-B')
    
    beta_opt, gamma_opt = result.x
    
    m = np.uint64(n/period_length)
    beta_values[m] = beta_opt
    beta_guess = beta_opt
    gamma_guess = gamma_opt
    
    solution = odeint(deriv, y0, tspan, args=(population, beta_opt, gamma_opt))
    S0 = solution[:,0][-1]

time = np.arange(period_number)
plt.plot(time, beta_values, 'b-', label='beta')
plt.show()


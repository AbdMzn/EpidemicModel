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
subset_size = period_length
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
total_deaths_per_million = np.nan_to_num(owid_data['total_deaths_per_million'].values, nan=0)
population  = owid_data['population'].values[0]
ihme_cases_mean = ihme_estimate['Daily new estimated infections of COVID-19 (IHME, mean)'].values
sus_f = 1 - (total_cases_per_million / 10**6)


period_length = 10
tspan = np.linspace(0, period_length, period_length)
n = 0
I_data = np.array(ihme_cases_mean[n:period_length+n])
N = population

def fitfunc(t, beta, gamma, S0):
    def odeeq(y, t, beta, gamma, S0):
        I, S = y
        dSdt = -beta * I
        dIdt = (beta * I * S / N) - (gamma * I)
        return [dIdt, dSdt]

    y0 = [I_data[0], S0]
    sol = odeint(odeeq, y0, t, args=(beta, gamma, S0))
    return sol[:, 0]

I0 = ihme_cases_mean[n]
I1 = ihme_cases_mean[n+period_length]
S0 = sus_f[n]
beta_0 = ((I0 - I1)/period_length + gamma * I0) / (I0 * S0)

bounds = ([-np.inf, -np.inf, 0], [np.inf, np.inf, N])

params, kcov = curve_fit(fitfunc, tspan, I_data, p0=[beta_0, gamma, S0,],bounds=bounds)
print(params)
fit = fitfunc(tspan, *params)
print("here")
plt.plot(tspan, I_data, 'ro', label='data')
plt.plot(tspan, fit, 'b-', label='fit')
plt.legend(loc='best')
plt.show()


""" tfit = np.linspace(0,period_length)
fit = fitfunc(tfit, k_fit)

import matplotlib.pyplot as plt
plt.plot(tspan, I_data, 'ro', label='data')
plt.plot(tfit, fit, 'b-', label='fit')
plt.legend(loc='best')
plt.savefig('images/ode-fit.png')
 """

#I_fit, beta_values, gamma_values = time_varying_sir_model(t_data, beta0_fit, beta_slope_fit, gamma_fit, N_fit, I0_fit, R0_fit)


""" start_date = datetime.strptime('02/04/2020', '%m/%d/%Y')
date_array = [start_date + timedelta(days=period_length * i) for i in range(period_number)]
formatted_date_array = [date.strftime('%m/%d/%Y') for date in date_array]
formatted_date_array

df = pd.DataFrame(beta_values.flatten())
df['Entity'] = np.repeat(countries, period_number)
df['Date'] = np.tile(formatted_date_array, len(countries))
df['Beta'] = beta_values.flatten()

csv_file_path = 'beta_values.csv'

df[['Entity', 'Date', 'Beta']].to_csv(csv_file_path, index=False, header=['Entity', 'Date', 'Beta']) """
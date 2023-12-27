import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta
from scipy.optimize import curve_fit
from scipy.integrate import odeint
import os

days = 784
period_length = 2
period_number = np.int64(days/period_length)
gamma = 0.043
path_from = 'filtered_data'
with open('countries.txt', 'r') as file:
    countries = file.read().splitlines()
#countries = ["Australia"]
beta_values = np.zeros((len(countries), period_number), dtype='float64')
sus_values = np.zeros((len(countries), period_number), dtype='float64')

for index, country in enumerate(countries):
    ihme_estimate = pd.read_csv(f'{path_from}/ihme_estimate.csv')
    owid_data = pd.read_csv(f'{path_from}/owid-covid-data.csv')
    
    criteria = ihme_estimate['Entity'] == country
    ihme_estimate = ihme_estimate[criteria]
    criteria = owid_data['location'] == country
    owid_data = owid_data[criteria]

    total_case_per_million = np.nan_to_num(owid_data['total_cases_per_million'].values, nan=0)
    total_deaths_per_million = np.nan_to_num(owid_data['total_deaths_per_million'].values, nan=0)
    population  = owid_data['population'].values[0]
    ihme_cases_mean = ihme_estimate['Daily new estimated infections of COVID-19 (IHME, mean)'].values
    
    for n in range(0, days, period_length):
        inf_0 = ihme_cases_mean[n] #infected start of period
        inf_1 = ihme_cases_mean[n + period_length - 1] #infected end of period
        total_inf_f =(total_case_per_million[n] / 10**6) #total infected fraction
        sus_f = 1 - (total_inf_f) #susceptible at start of period
        
        m = np.uint64(n/period_length)
        equation = ((inf_1 - inf_0)/period_length + gamma * inf_0) / (inf_0 * sus_f) if inf_0 != 0 else 0
        beta_values[index, m] = equation
        sus_values[index, m] = sus_f

start_date = datetime.strptime('10/02/2020', '%d/%m/%Y')
date_array = [start_date + timedelta(days=period_length * i) for i in range(period_number)]
formatted_date_array = [date.strftime('%d/%m/%Y') for date in date_array]

df = pd.DataFrame(beta_values.flatten())
df['Entity'] = np.repeat(countries, period_number)
df['Date'] = np.tile(formatted_date_array, len(countries))
df['Beta'] = beta_values.flatten()
df['Susceptible'] = sus_values.flatten()

csv_file_path = 'beta_values.csv'

df[['Entity', 'Date', 'Beta', 'Susceptible']].to_csv(csv_file_path, index=False, header=['Entity', 'Date', 'Beta', 'Susceptible'])
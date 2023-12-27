import numpy as np
import pandas as pd
import os

with open('countries.txt', 'r') as file:
    chosen_countries = file.read().splitlines()

path_from = 'raw_data'
path_to = 'filtered_data'
start_date = '02/10/2020'
end_date ='04/03/2022'

document = pd.read_csv(f'{path_from}/owid-covid-data.csv')
document['date'] = pd.to_datetime(document['date'])

condition_1 = document['location'].isin(chosen_countries)
condition_2 = document['date'].between(start_date, end_date)
criteria = condition_1 & condition_2 
filtered_document = document[criteria]
filtered_document.to_csv(os.path.join(path_to, 'owid-covid-data.csv'), index=False)

import pandas as pd
import os

path_from = 'raw_data/'
path_to = 'filtered_data'
start_date = '02/10/2020'
end_date ='04/03/2022'
document_names = os.listdir(path_from)

with open('countries.txt', 'r') as file:
    chosen_countries = file.read().splitlines()
    
for name in document_names:
    document = pd.read_csv(f'raw_data/{name}')
    if 'Entity' in document.columns:
        document['Day'] = pd.to_datetime(document['Day'])
        condition_1 = document['Entity'].isin(chosen_countries)
        condition_2 = document['Day'].between(start_date, end_date)
        criteria = condition_1 & condition_2
        filtered_document = document[criteria]
        filtered_document.to_csv(os.path.join(path_to, name), index=False)

    else:
        print(f'No column with the name Entity in {name}')
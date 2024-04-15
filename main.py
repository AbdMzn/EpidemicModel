import csv
from pull_worldometer_data import *
from transmission_rate import *

document_name = "data"

countries = open("countries.txt", "r").read().split("\n")
populations = open("population.txt", "r").read().split("\n")

for i in range(len(countries)):
    pull_worldometer_data(countries[i])

with open(f'{document_name}.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Quarter", "beta", "gamma"])

for i in range(len(countries)):
    transmission_rate(countries[i], populations[i], document_name)

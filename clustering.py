import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import csv

df = pd.read_csv('data.csv')
countries = df['Country'].values
quarters = df['Quarter'].values
beta_values = df['beta'].values
gamma_values = df['gamma'].values
country_names = set(countries.tolist())

arr = np.empty((15, 32), dtype= np.int32)
beta_values = beta_values.reshape(32, 15)
beta_values = beta_values.T

for i in range(15):
    data = beta_values[i]
    data = data.reshape(-1, 1)

    clusters_count = 4

    kmeans = KMeans(n_clusters = clusters_count, n_init=10)
    kmeans.fit(data)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    arr[i] = labels

with open('clusters.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["quarter", "country", "cluster", "beta"])
    
for i in range(15):
    cluster_array = np.array([f'Q{i}'] * 32)
    combined = list(zip(cluster_array, country_names, arr[i], beta_values[i]))
    sorted_combined = sorted(combined, key=lambda x: x[2])

    with open('clusters.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for entry in sorted_combined:
            writer.writerow(entry)
import csv
data = [
    ("USA", "Q1", 0.5, 0.6),
    ("Canada", "Q2", 0.6, 0.7),
    ("UK", "Q3", 0.7, 0.8),
    ("Germany", "Q4", 0.8, 0.9),
    # Add more data here
]

with open(f'data1.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Country", "Quarter", "Beta", "Gamma"])
    
    for entry in data:
        writer.writerow(entry)
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import ast

url = 'https://www.worldometers.info/coronavirus/country/us/'
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36'}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
scripts = soup.find_all('script')
for script in scripts:
    if "Highcharts.chart('coronavirus-cases-linear'" in str(script):
        jsonStr = str(script)
        total_cases = re.search(r"(name: 'Cases')[\s\S\W\w]*(data:[\s\S\W\w]*\d\])", jsonStr, re.IGNORECASE)
        total_cases = total_cases.group(2).split('data:')[-1].strip().replace('[','').replace(']','').split(',')
        
    elif "Highcharts.chart('graph-cases-daily'" in str(script):
        jsonStr = str(script)
        
        dates = re.search(r'(xAxis: {[\s\S\W\w]*)(categories: )(\[[\w\W\s\W]*\"\])', jsonStr)
        dates = dates.group(3).replace('[','').replace(']','')
        dates = ast.literal_eval(dates)
        dates = [ x for x in dates]
        
        new_cases_daily = re.search(r"(name: 'Daily Cases')[\s\S\W\w]*(data:[\s\S\W\w]*\d\])", jsonStr, re.IGNORECASE)
        new_cases_daily = new_cases_daily.group(2).split('data:')[-1].strip().replace('[','').replace(']','').split(',')
        new_cases_3_days = re.search(r"(name: '3-day moving average')[\s\S\W\w]*(data:[\s\S\W\w]*\d\])", jsonStr, re.IGNORECASE)
        new_cases_3_days = new_cases_3_days.group(2).split('data:')[-1].strip().replace('[','').replace(']','').split(',')
        new_cases_7_days = re.search(r"(name: '7-day moving average')[\s\S\W\w]*(data:[\s\S\W\w]*\d\])", jsonStr, re.IGNORECASE)
        new_cases_7_days = new_cases_7_days.group(2).split('data:')[-1].strip().replace('[','').replace(']','').split(',')
        
    elif "Highcharts.chart('graph-active-cases-total'" in str(script):
        jsonStr = str(script)
        active_cases = re.search(r"(name: 'Currently Infected')[\s\S\W\w]*(data:[\s\S\W\w]*\d\])", jsonStr, re.IGNORECASE)
        active_cases = active_cases.group(2).split('data:')[-1].strip().replace('[','').replace(']','').split(',')
    
    elif "Highcharts.chart('coronavirus-deaths-linear'" in str(script):
        jsonStr = str(script)
        total_deaths = re.search(r"(name: 'Deaths')[\s\S\W\w]*(data:[\s\S\W\w]*\d\])", jsonStr, re.IGNORECASE)
        total_deaths = total_deaths.group(2).split('data:')[-1].strip().replace('[','').replace(']','').split(',')

total_cases_int = [int(x) for x in total_cases]
active_cases_int = [int(x) for x in active_cases]
total_removed = [i - j for i, j in zip(total_cases_int, active_cases_int)]
df = pd.DataFrame({'Date':dates, 'Total Cases':total_cases, 'Active Cases':active_cases, 'Total Removed':total_removed , 'New Cases':new_cases_daily , 'Total Deaths':total_deaths})  
csv_file_path = 'worldometer_data(us).csv'

df[['Date', 'Total Cases', 'Active Cases', 'Total Removed', 'New Cases', 'Total Deaths']].to_csv(csv_file_path, index=False, header=['Date', 'Total Cases', 'Active Cases', 'Total Removed', 'New Cases', 'Total Deaths'])

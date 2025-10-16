import json
import requests
import os

# Get data for all years
data = {}
for filename in os.listdir('data/'):
    if '-' not in filename and '.json' in filename:
        print(filename)
        with open(f'data/{filename}', 'r') as file:
            data.update(json.load(file))

sum = 0
for date, value in data.items():
    sum += value

sum = round(sum / 1000, 1)
url = f'https://img.shields.io/badge/GitHub_Downloads-{sum}k-green?logo=github'

response = requests.get(url)

filename = 'badges/total.svg'
if response.status_code == 200:
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    print(f"Image downloaded successfully to {filename}")
else:
    print('Failed')
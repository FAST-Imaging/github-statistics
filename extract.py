import json
import os
from datetime import datetime
from github import Github

current_year = datetime.now().year
date_format = '%Y-%m-%d'
date_today = datetime.now().strftime(date_format)

# Check if today is already processed
if os.path.exists('data/last_updated'):
    with open('data/last_updated', 'r') as file:
        last_updated = file.readline().strip()
        if last_updated == date_today:
            print('Today has already been processed!')
            exit(0)

# =====================> Get downloads
github = Github()
repo = github.get_repo('FAST-Imaging/FAST')
releases = repo.get_releases()
downloads_total = 0
downloads_per_OS = {
    'Windows': 0,
    'Linux': 0,
    'macOS x86_64': 0,
    'macOS arm64': 0,
}
downloads_per_type = {
    'Archive': 0,
    'Python Wheel': 0,
    'Installer': 0,
}
for release in releases:
    assets = release.get_assets()
    for asset in assets:
        downloads_total += asset.download_count

        if 'win' in asset.name:
            downloads_per_OS['Windows'] += asset.download_count
        elif 'ubuntu' in asset.name or 'linux' in asset.name:
            downloads_per_OS['Linux'] += asset.download_count
        elif 'mac' in asset.name:
            if 'arm64' in asset.name:
                downloads_per_OS['macOS arm64'] += asset.download_count
            else:
                downloads_per_OS['macOS x86_64'] += asset.download_count
        else:
            print(f'Error parsing OS for {asset.name}')
            continue

        if asset.name.endswith('.tar.xz') or asset.name.endswith('.zip') or asset.name.endswith('.tar.gz'):
            downloads_per_type['Archive'] += asset.download_count
        elif asset.name.endswith('.exe') or asset.name.endswith('.deb'):
            downloads_per_type['Installer'] += asset.download_count
        elif asset.name.endswith('.whl'):
            downloads_per_type['Python Wheel'] += asset.download_count
        else:
            print(f'Error parsing file type for {asset.name}')
            continue

# ========================> Total downloads
sum = 0
for year in range(2025, current_year+1):
    if os.path.exists(f'data/{year}.json'):
        with open(f'data/{year}.json', 'r') as file:
            data = json.load(file)
        # Get sum of all
        for date, value in data.items():
            sum += value

    if year == current_year:
        if os.path.exists(f'data/{year}.json'):
            data[date_today] = downloads_total - sum
        else:
            data = {date_today: downloads_total}

        with open(f'data/{year}.json', 'w') as file:
            json.dump(data, file, indent=4)


# ========================> Per OS
sum = {}
for year in range(2025, current_year + 1):
    if os.path.exists(f'data/{year}-OS.json'):
        with open(f'data/{year}-OS.json', 'r') as file:
            data = json.load(file)
            for OS in data.keys():
                # Find sum for OS
                if OS not in sum:
                    sum[OS] = 0
                for date, value in data[OS].items():
                    sum[OS] += value
                data[OS][date_today] = downloads_per_OS[OS] - sum[OS]
    if year == current_year:
        if os.path.exists(f'data/{year}-OS.json'):
            for OS in downloads_per_OS.keys():
                if OS in data.keys():
                    data[OS][date_today] = downloads_per_OS[OS] - sum[OS]
                else:
                    data[OS] = {date_today: downloads_per_OS[OS] - sum[OS]}
        else:
            data = {}
            for OS in downloads_per_OS.keys():
                data[OS] = {date_today: downloads_per_OS[OS]}

        with open(f'data/{year}-OS.json', 'w') as file:
            json.dump(data, file, indent=4)

# ========================> Per file type
sum = {}
for year in range(2025, current_year + 1):
    if os.path.exists(f'data/{year}-file-type.json'):
        with open(f'data/{year}-file-type.json', 'r') as file:
            data = json.load(file)
            for type in data.keys():
                # Find sum for OS
                if type not in sum:
                    sum[type] = 0
                for date, value in data[type].items():
                    sum[type] += value
                data[type][date_today] = downloads_per_type[type] - sum[type]
    else:
        data = {}
        for type in downloads_per_type.keys():
            data[type] = {date_today: downloads_per_type[type]}

    if year == current_year:
        if os.path.exists(f'data/{year}-file-type.json'):
            for type in downloads_per_type.keys():
                if type in data.keys():
                    data[type][date_today] = downloads_per_type[type] - sum[type]
                else:
                    data[type] = {date_today: downloads_per_type[type] - sum[type]}
        else:
            data = {}
            for type in downloads_per_type.keys():
                data[type] = {date_today: downloads_per_type[type]}

        with open(f'data/{year}-file-type.json', 'w') as file:
            json.dump(data, file, indent=4)

# =====================> Update last_updated file
with open('data/last_updated', 'w') as file:
    file.write(date_today)
